#!/usr/bin/env python3
"""Diagnostic: is the NRSC-ISRO Bhuvan lightning feed returning real strikes, and where?

Run on a machine that can reach Bhuvan:  python check_lightning.py
It does not change DIWIS. For each of the last 6 completed UTC hours (the same window the app uses)
it prints how many points came back, the coordinate range, the property names, a sample record,
and how many points fall in a box around Assam and its neighbours (NE India + West Bengal).

How to judge the result:
  * Total points > 0 and spread across India  -> the feed works.
  * Longitudes ~68-98 and latitudes ~6-38     -> [longitude, latitude] order is right (as the app assumes).
  * NE-box count > 0 on a stormy evening but the dashboard shows none -> report it, that is a bug.
  * Compare one hour with https://bhuvan-app1.nrsc.gov.in/lightning/ in your browser.
  * If a record has its own time field, check it matches the UTC hour used here (a mismatch means the
    'timestamp' parameter may be an IST hour, not UTC).
"""
import json
from datetime import datetime, timedelta, timezone

import requests

URL = "https://bhuvan-app1.nrsc.gov.in/lightning/usrtasks/heatwave/get/geojson.php"
HEADERS = {"User-Agent": "DIWIS-diagnostic"}
NE_BOX = (87.5, 21.5, 97.5, 29.5)  # min_lon, min_lat, max_lon, max_lat

now_utc = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
now_ist = datetime.now(timezone(timedelta(hours=5, minutes=30)))
print(f"Now: {now_utc:%Y-%m-%d %H:00} UTC  ({now_ist:%Y-%m-%d %H:%M} IST)\n")

grand_total = grand_ne = 0
for offset in range(1, 7):
    hour = now_utc - timedelta(hours=offset)
    label = f"{hour:%Y-%m-%d %H}:00-{(hour + timedelta(hours=1)):%H}:00 UTC"
    try:
        r = requests.get(URL, headers=HEADERS, timeout=(5, 25),
                         params={"date": hour.date().isoformat(), "timestamp": f"{hour.hour:02d}"})
        r.raise_for_status()
        payload = r.json()
    except Exception as exc:
        print(f"{label}: request failed: {exc}")
        continue
    features = payload.get("features") or []
    points = []
    for f in features:
        g = f.get("geometry") or {}
        c = g.get("coordinates") or []
        if g.get("type") == "Point" and len(c) >= 2 and all(isinstance(v, (int, float)) for v in c[:2]):
            points.append((c[0], c[1], f.get("properties") or {}))
    ne = [p for p in points if NE_BOX[0] <= p[0] <= NE_BOX[2] and NE_BOX[1] <= p[1] <= NE_BOX[3]]
    grand_total += len(points)
    grand_ne += len(ne)
    if points:
        lons, lats = [p[0] for p in points], [p[1] for p in points]
        print(f"{label}: {len(points)} points | lon {min(lons):.2f}..{max(lons):.2f} | "
              f"lat {min(lats):.2f}..{max(lats):.2f} | in NE box: {len(ne)}")
        print(f"    property names: {sorted(points[0][2])}")
        print(f"    sample: lon={points[0][0]}, lat={points[0][1]}, props={json.dumps(points[0][2], default=str)[:200]}")
    else:
        print(f"{label}: 0 points (feed type: {payload.get('type')})")

print(f"\nTotal points in 6 hours: {grand_total} | inside the NE/West Bengal box: {grand_ne}")
