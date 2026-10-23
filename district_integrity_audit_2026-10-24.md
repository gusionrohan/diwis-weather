# DIWIS district data integrity audit

**Snapshot checked:** 24 October 2026 (India Standard Time)  
**Coverage:** 113 districts in the eight states currently offered by DIWIS: Arunachal Pradesh, Assam, Manipur, Meghalaya, Mizoram, Nagaland, Tripura, and West Bengal.

## Result

**Not ready for unqualified official operational handover.** The audit confirms broad live-feed coverage, but it also found missing live values and cases where a feed entry is stale and correctly rejected. The app should continue to show these as unavailable rather than claim a zero or invent a reading.

| Data check | District coverage | Notes |
|---|---:|---|
| Observed rainfall | 109/113 | Four West Bengal districts had no report and no complete-coverage grid value. |
| Five-day rainfall forecast | 111/113 | No current dated rows for Saiha (Mizoram) or Purba Bardhaman (West Bengal). |
| Five-day temperature max/min | 113/113 | Open-Meteo live forecast, district reference point; this is a point forecast, not a district-wide observation. |
| District warning feed | 113/113 | A source record matched each district in this snapshot. |
| Valid nowcast | 105/113 | Eight Mizoram district entries were outside their stated validity and were rejected. |
| Lightning coordinates | 113/113 evaluated | The live feed contained 1,920 records; none fell within the 113 district polygons in the six-hour query window. This means no in-boundary coordinates were returned for this snapshot, not that lightning is impossible or that the feed is complete. |

## Missing or restricted values

- **Observed rainfall:** Cooch Behar, East Midnapore, North Dinajpur, and South Dinajpur (West Bengal). IMD district matching did not return a usable value; the 0.25° IMD grid fallback did not have complete valid coverage for these district boundaries, so no whole-district figure was published.
- **Rainfall forecast:** Saiha (Mizoram) and Purba Bardhaman (West Bengal). Neither had five current dated district values in the checked IMD/Met Centre sources. Historical or ambiguous district-name matches were not accepted.
- **Nowcast:** All eight Mizoram districts had matching IMD entries outside their stated validity. They must be shown as unavailable until a fresh valid bulletin is returned.
- **Assam rainfall exception:** One district value came from an RMC Guwahati station report mapped by station/district name; it is a station observation and must not be presented as a district-wide aggregate. Other usable observed-rain rows were 101 IMD district-page values and 7 area-weighted IMD-grid values with complete boundary coverage.

## Validation performed

- Queried current IMD district boundary, rainfall, forecast, warning, and nowcast feeds; Open-Meteo temperature; Assam RMC report fallback; and the live ISRO/NESDIS lightning feed used by the app.
- Checked district matching, dated forecast rows, bulletin validity, observation date, and grid coverage. Grid-derived rainfall is explicitly labeled as an area-weighted district estimate.
- The 109 accepted observed-rainfall values were dated **23 October 2026**, the latest daily observation returned in this 24 October audit.
- The live fetch functions were run for each district and the row-level results are in the accompanying CSV.
- `app.py` passed Python syntax compilation after the IMD state-code matching correction. This was a live-source/function audit, not a manual browser/UI test, production security review, or long-duration reliability test.

## Handover conditions

Before representing DIWIS as a complete official district service, resolve or explicitly accept the missing cases above, clearly label station and grid-derived values, and conduct a departmental validation against source bulletins for representative districts. The app must preserve source names, observation/issue times, and stale/unavailable status. A source returning no row is not proof of zero rain or no warning.

## Official source links

- [India Meteorological Department](https://mausam.imd.gov.in/)
- [IMD real-time rainfall grid](https://www.imdpune.gov.in/cmpg/Realtimedata/Rainfall/Rain_Download.html)
- [Regional Meteorological Centre Guwahati](https://mausam.imd.gov.in/guwahati/)
- [Open-Meteo](https://open-meteo.com/) (temperature forecast)
