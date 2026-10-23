#!/usr/bin/env python3
"""Collect and append live snapshots for every district offered by DIWIS."""

import argparse
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from audit_districts import load_app_functions
from db_manager import DEFAULT_DB_PATH, save_live_daily_snapshot


def configure_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    handler = RotatingFileHandler(
        os.path.join(log_dir, "daily_snapshot.log"),
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[handler, logging.StreamHandler()],
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, help="collect only the first N districts (for testing)")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH, help="SQLite database path")
    args = parser.parse_args()
    configure_logging()

    app = load_app_functions()
    st = app["st"]
    logging.info("Loading the current district list from IMD.")
    neighbors, _district_state, geometries, _options = app["live_administrative_geography"]()
    app["district_geometries"] = geometries
    app["district_state"] = _district_state
    app["neighbor_candidates"] = neighbors
    places = [
        ("Scheduled", state, district)
        for (state, district) in sorted(geometries)
        if state.casefold() in {name.casefold() for name in neighbors}
    ]
    if args.limit is not None:
        if args.limit < 1:
            parser.error("--limit must be greater than zero")
        places = places[:args.limit]
    if not places:
        raise RuntimeError("The live district service returned no districts to collect.")

    logging.info("Fetching live data for %d districts.", len(places))
    app["fetch_selected_live_data"](places)
    live_results = st.session_state.get("live_results") or []

    forecast_error = None
    try:
        forecast_results = app["fetch_live_district_forecasts"](places, geometries)
    except Exception as exc:
        forecast_results = []
        forecast_error = exc
        logging.exception("District forecast collection failed; saving live data without forecasts.")

    saved = save_live_daily_snapshot(live_results, forecast_results, db_path=args.db_path)
    errors = sum(bool(item.get("error")) for item in live_results)
    logging.info(
        "Saved %d district snapshots at %s; %d live-data rows have errors.",
        saved,
        datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(timespec="seconds"),
        errors,
    )
    if forecast_error:
        raise RuntimeError("Snapshots saved with live data, but forecast collection failed.") from forecast_error
    if errors:
        raise RuntimeError(f"Snapshots saved, but {errors} districts had live-data errors.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Scheduled DIWIS history collection failed.")
        sys.exit(1)
