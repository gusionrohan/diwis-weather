#!/usr/bin/env python3
"""Diagnostic: which live government layer actually lists the current districts?

Run on a machine that can reach IMD:  python check_district_sources.py [lgd_districts.csv]
It does not change DIWIS. It prints, per state, how many districts each IMD layer returns,
and (optionally) which official LGD districts each layer is missing. Download the LGD file
manually from https://lgdirectory.gov.in/downloadDirectory.do (Districts, CSV).
"""
import csv
import re
import sys
import requests

WFS = "https://reactjs.imd.gov.in/geoserver/ows"
LAYERS = {
    "boundary (imd:india_districts)": ("imd:india_districts", ("stname", "state", "NAME_1"), ("district", "shapeName", "NAME_2", "name")),
    "warnings (imd:district_warnings_india)": ("imd:district_warnings_india", ("State_Name", "State"), ("District",)),
    "nowcast (imd:NowcastWarningDistrict)": ("imd:NowcastWarningDistrict", ("State",), ("District", "State_District")),
}
STATES = {"ASSAM", "ARUNACHAL PRADESH", "MANIPUR", "MEGHALAYA", "MIZORAM", "NAGALAND", "TRIPURA", "WEST BENGAL"}


def norm(value):
    return " ".join(re.sub(r"[\W_]+", " ", str(value or "").casefold()).split())


def fetch(layer):
    r = requests.get(WFS, params={"service": "WFS", "version": "1.1.0", "request": "GetFeature",
                                  "typename": layer, "srsname": "EPSG:4326",
                                  "outputFormat": "application/json"}, timeout=60)
    r.raise_for_status()
    return r.json().get("features", [])


def districts_by_state(features, state_keys, name_keys):
    out = {}
    for feat in features:
        props = feat.get("properties") or {}
        state = next((str(props[k]).strip().upper() for k in state_keys if props.get(k)), "")
        name = next((str(props[k]).strip() for k in name_keys if props.get(k)), "")
        if state in STATES and name:
            out.setdefault(state, set()).add(norm(name))
    return out


def load_lgd(path):
    out = {}
    with open(path, encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            state = next((v for k, v in row.items() if k and "state" in k.lower() and "name" in k.lower()), "")
            name = next((v for k, v in row.items() if k and "district" in k.lower() and "name" in k.lower()), "")
            if state.strip().upper() in STATES and name.strip():
                out.setdefault(state.strip().upper(), set()).add(norm(name))
    return out


def main():
    lgd = None
    if len(sys.argv) > 1:
        try:
            lgd = load_lgd(sys.argv[1])
        except FileNotFoundError:
            print(f"LGD file '{sys.argv[1]}' not found; showing IMD layer counts only.")
    for label, (layer, state_keys, name_keys) in LAYERS.items():
        print(f"\n=== {label}")
        try:
            found = districts_by_state(fetch(layer), state_keys, name_keys)
        except Exception as exc:
            print("  could not read layer:", exc)
            continue
        for state in sorted(STATES):
            have = found.get(state, set())
            line = f"  {state:18} {len(have):3} districts"
            if lgd:
                official = lgd.get(state, set())
                line += f" | LGD lists {len(official):3} | missing from layer: {sorted(official - have)}"
            print(line)


if __name__ == "__main__":
    main()
