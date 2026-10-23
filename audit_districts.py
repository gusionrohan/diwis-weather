#!/usr/bin/env python3
"""District-by-district integrity audit for DIWIS (uses the app's own live-fetch functions).

Run on a machine that can reach IMD/RMC/Open-Meteo, from the folder holding app.py:

    python audit_districts.py                  # Assam + neighbouring states
    python audit_districts.py --states Assam   # only some states
    python audit_districts.py --limit 5        # quick trial on 5 districts

Writes district_audit_<IST date-time>.csv and prints a summary of flagged districts.
It reads data only; it does not change the app or its database.
"""
import argparse
import ast
import csv
import sys
import types
from datetime import datetime
from zoneinfo import ZoneInfo

APP = "app.py"


class _AttrDict(dict):
    __getattr__ = dict.get

    def __setattr__(self, key, value):
        self[key] = value


class _FakeStreamlit(types.SimpleNamespace):
    """Just enough of streamlit for the app's fetch functions to run outside the web app."""

    def __init__(self):
        super().__init__(session_state=_AttrDict())

    @staticmethod
    def _decorator(*args, **_kwargs):
        if len(args) == 1 and callable(args[0]):
            return args[0]
        return lambda func: func

    cache_data = cache_resource = fragment = _decorator

    def progress(self, *_a, **_k):
        return types.SimpleNamespace(progress=lambda *_x, **_y: None, empty=lambda: None)

    def __getattr__(self, name):  # any other st.* call is a harmless no-op
        return lambda *_a, **_k: types.SimpleNamespace(
            __enter__=lambda s: s, __exit__=lambda *a: False)


def load_app_functions():
    """Execute only the app's imports, constants and functions (never its screen code)."""
    with open(APP, encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    keep = (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef, ast.Assign, ast.AnnAssign)
    namespace = {"__name__": "diwis_app", "st": _FakeStreamlit()}
    for node in tree.body:
        if not isinstance(node, keep):
            continue
        if isinstance(node, ast.ImportFrom) and node.module == "db_manager":
            continue  # accounts/database are not needed for an audit
        if isinstance(node, ast.Import) and any(a.name == "streamlit" for a in node.names):
            continue
        try:
            exec(compile(ast.Module([node], []), APP, "exec"), namespace)
        except Exception:  # screen-only assignments (sidebar widgets etc.) are not needed
            pass
    return namespace


def flags_for(row):
    flags = []
    if row["rain_status"] != "OK":
        flags.append("RAIN_MISSING")
    if "station" in (row["rain_note"] or "").lower():
        flags.append("RAIN_STATION_ONLY")
    if "grid" in (row["rain_source"] or "").lower():
        flags.append("RAIN_GRID_ESTIMATE")
    if "partial" in (row["rain_note"] or "").lower():
        flags.append("RAIN_GRID_PARTIAL")
    if row["rain_vs_grid_flag"]:
        flags.append("RAIN_PAGE_VS_GRID_DIFFERS")
    if row["warning_status"] != "OK":
        flags.append("WARNING_MISSING")
    elif row["warning_blank_days"]:
        flags.append("WARNING_DAYS_BLANK")
    if row["nowcast_status"] == "EXPIRED":
        flags.append("NOWCAST_EXPIRED")
    elif row["nowcast_status"] != "OK":
        flags.append("NOWCAST_MISSING")
    if row["rain_forecast_days"] < 5:
        flags.append("RAIN_FORECAST_INCOMPLETE")
    if row["temp_forecast_days"] < 5:
        flags.append("TEMP_FORECAST_INCOMPLETE")
    if row["lightning_status"] != "OK":
        flags.append("LIGHTNING_FEED_MISSING")
    if row["error"]:
        flags.append("FETCH_ERROR")
    return flags


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--states", nargs="*", help="limit to these states (default: Assam + neighbours)")
    parser.add_argument("--limit", type=int, help="audit only the first N districts")
    args = parser.parse_args()

    app = load_app_functions()
    st = app["st"]
    print("Loading live district geography ...")
    neighbours, district_state, geometries, _options = app["live_administrative_geography"]()
    # The app's fetch functions read these module-level names, which the web app sets at sign-in.
    app["district_geometries"], app["district_state"], app["neighbor_candidates"] = geometries, district_state, neighbours
    wanted = {s.casefold() for s in (args.states or neighbours)}
    places = [("Audit", state, district) for (state, district) in sorted(geometries)
              if state.casefold() in wanted]
    if args.limit:
        places = places[:args.limit]
    print(f"Auditing {len(places)} districts (this can take several minutes) ...")

    app["fetch_selected_live_data"](places)
    live = {(r["state"], r["district"]): r for r in st.session_state.get("live_results", [])}
    forecasts = {(f["state"], f["district"]): f
                 for f in app["fetch_live_district_forecasts"](places, geometries)}

    rows = []
    for _kind, state, district in places:
        r = live.get((state, district), {})
        f = forecasts.get((state, district), {})
        rain = r.get("rainfall") or {}
        warn = r.get("warnings") or {}
        now = r.get("nowcast") or {}
        light = r.get("lightning") or {}
        rain_days = [d for d in (f.get("rainfall_days") or []) if d.get("rainfall") is not None]
        row = {
            "state": state, "district": district,
            "rain_status": rain.get("status"), "rain_mm": rain.get("value_mm"),
            "rain_date": rain.get("date"), "rain_source": rain.get("source"),
            "rain_note": rain.get("coverage_note") or rain.get("reason") or "",
            "rain_vs_grid_mm": "", "rain_vs_grid_flag": "",
            "warning_status": warn.get("status"), "warning_issue_date": warn.get("issue_date"),
            "warning_blank_days": ",".join(map(str, warn.get("missing_days") or [])),
            "warning_hazard_days": ",".join(str(i.get("day")) for i in warn.get("items") or []),
            "nowcast_status": now.get("status"), "nowcast_issued": f"{now.get('issue_date') or ''} {now.get('issue_time') or ''}".strip(),
            "nowcast_valid_until": now.get("valid_until") or "", "nowcast_detail": now.get("message") or now.get("reason") or "",
            "lightning_status": light.get("status"), "lightning_points_6h": len(light.get("coordinates") or []),
            "rain_forecast_days": len(rain_days), "temp_forecast_days": len(f.get("temperature_days") or []),
            "error": r.get("error") or "",
        }
        # Cross-check: IMD page value vs IMD grid average for the same date.
        if rain.get("status") == "OK" and "district rainfall page" in (rain.get("source") or ""):
            try:
                grid = app["live_imd_grid_district_rainfall"](geometries[(state, district)])
                if grid.get("date") == rain.get("date"):
                    page_mm, grid_mm = float(rain["value_mm"]), float(grid["value_mm"])
                    row["rain_vs_grid_mm"] = grid_mm
                    big = abs(page_mm - grid_mm) >= 10 and max(page_mm, grid_mm) >= 2 * max(min(page_mm, grid_mm), 0.1)
                    row["rain_vs_grid_flag"] = "YES" if big else ""
            except Exception:
                pass
        row["flags"] = " ".join(flags_for(row))
        rows.append(row)

    stamp = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y%m%d_%H%M")
    path = f"district_audit_{stamp}.csv"
    with open(path, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["state"])
        writer.writeheader()
        writer.writerows(rows)

    flagged = [r for r in rows if r["flags"]]
    print(f"\n{len(rows)} districts audited, {len(flagged)} with at least one flag. Saved: {path}\n")
    counts = {}
    for r in rows:
        for flag in r["flags"].split():
            counts[flag] = counts.get(flag, 0) + 1
    for flag, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {flag:28} {n}")
    print("\nFlagged districts:")
    for r in flagged:
        print(f"  {r['state']} / {r['district']}: {r['flags']}")


if __name__ == "__main__":
    main()
