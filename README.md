# DIWIS — District Integrated Weather Information System

DIWIS is a Streamlit dashboard that shows live district weather for Assam and the states around it: observed rainfall, 5-day rainfall and temperature forecasts, warnings, nowcasts, cyclone warnings and lightning strike coordinates. It has account roles, a primary Assam district, selectable neighbouring states and districts, source links and a PDF report.

**The core rule:** every reading comes from a live request and keeps its source and date. If a source is missing, stale, ambiguous or failed, the dashboard shows "not reported" (or "Expired" for an old nowcast). It never shows a missing value as zero, and never shows a missing warning as "no warning". Saved values are never substituted.

---

## Files and what each does

| File | What it does |
|---|---|
| `app.py` | The whole dashboard: login, pages, all live data fetching, district-name matching, PDF report. Run with `streamlit run app.py`. |
| `db_manager.py` | The SQLite database: user accounts (salted scrypt passwords, roles), and the daily history table `live_daily_snapshots`. Several older tables in it belong to the earlier DHARA scraper and are not used by DIWIS. |
| `requirements.txt` | Python packages. Streamlit 1.50 or newer is required. |
| `config.toml` | Streamlit settings and colours. Put it in a `.streamlit` folder next to `app.py`. |
| `audit_districts.py` | Audit tool. Runs the app's own fetch functions for every district and writes `district_audit_<date-time>.csv` with flags (rain missing, forecast incomplete, nowcast expired, grid estimate and so on). It reads only and changes nothing. |
| `check_district_sources.py` | Diagnostic. Shows how many districts each IMD layer (boundary, warnings, nowcast) lists per state, and optionally which official LGD districts a layer lacks. |
| `check_pdf_text.py` | Diagnostic. Shows how a Met Centre forecast PDF reads for one district (used to find the Saiha problem). |
| `check_lightning.py` | Diagnostic. Fetches the last six hours of the Bhuvan lightning feed and prints point counts, coordinate ranges and how many fall in the north-east box, so you can check that zero strikes is real. |
| `daily_snapshot.py` | Scheduled collector. Fetches live data and forecasts for every district offered by DIWIS and appends the results to SQLite. |
| `setup_windows_scheduler.ps1` | Registers the daily Windows Scheduled Task for `daily_snapshot.py` at 09:00 local machine time. |
| `data/diwis_historical.db` | Created at first run. Holds accounts and daily snapshots. Never include it in a source handover. |

---

## Dashboard pages

- **Dashboard:** live conditions for the primary district and any selected secondary districts, the 5-day forecast tables, and the PDF download.
- **User administration:** district admins and superadmins create accounts.
- **Data sources:** where each reading comes from, with links.
- **My account:** shows your role and district, and signs you out.

---

## How each reading is fetched

All requests are made when you load or refresh the dashboard. Names are matched exactly or by close spelling, and a match is accepted only when it is unambiguous (see "District names" below).

### Districts and boundaries
- State and district boundaries come from IMD's public GeoServer (`imd:India_State`, `imd:india_districts`).
- The district list is then completed from IMD's nowcast layer (`imd:NowcastWarningDistrict`), which follows the newest district revision, when that layer lists at least as many districts as the boundary layer.
- Neighbouring states are the ones whose boundary touches Assam.
- Names are tidied after loading: IMD's split polygon "Lawngtlai2" is merged into Lawngtlai, "Karbi Analog" is shown as Karbi Anglong, Karimganj is shown as Sribhumi, and IMD's "Kamrup" is shown as Kamrup Metropolitan (Guwahati) while "Kamrup Rural" stays as it is.
- Boundaries are cached in memory for 6 hours.

### Observed rainfall (previous day, 0830 IST report)
Tried in this order, using the first that works. **An IMD page value is always preferred.**
1. IMD's public district rainfall page.
2. Assam only: RMC Guwahati's today's-weather station table, then RMC Guwahati's daily report PDF. These are station readings, not district averages, and are labelled that way. "NIL" counts as 0; a blank stays missing.
3. IMD's real-time 0.25° rainfall grid, as an area-weighted district average. **Used only for districts with no IMD page value.** It is accepted only if the grid covers at least 90% of the district. Below 100% it is labelled "PARTIAL grid estimate" with the exact coverage. Below 90%, nothing is shown.

A report dated today is current; yesterday's stays current until 08:30 IST on the next day, when the new report is due.

### Rainfall forecast (5 days)
1. IMD's five-day district rainfall feed, one request per state per day.
2. For any missing day, the matching Met Centre's district forecast PDF (Guwahati, Itanagar, Shillong, Aizawl, Imphal, Kohima, Agartala, and Kolkata North and South Bengal), read table-row by table-row.

Days are joined by exact date, never by position. A district with no exact current row stays "Not reported".

### Temperature forecast (5 days)
Open-Meteo only, at one reference point inside the district boundary. This is a model forecast, not an observed or IMD figure, and it is labelled as such.

### Warnings
IMD's district warning layer (`imd:district_warnings_india`), days 1 to 5. For Assam, RMC Guwahati's warning page is the fallback. A day the feed leaves blank is shown as not reported, not as an all-clear. DIWIS displays its fetch age and source issue date when available; the matched warning records do not expose a reliable issue time, so a successful fetch is not proof that the source content changed.

### Nowcast
IMD's district nowcast layer (`imd:NowcastWarningDistrict`); RMC Guwahati's district nowcast page is the fallback for Assam. Nowcasts are re-checked about every 15 minutes while the dashboard is open. An entry past its stated validity is shown as **"Expired · date time IST"** and is never presented as current or as an all-clear. If a recheck fails, the last verified entry is marked **STALE**; if its validity has passed, it remains **Expired**. The old warning is never shown as a current warning or current all-clear.

### Cyclone
Taken from the warning feed only: it is shown when a district warning names a cyclone. Otherwise the dashboard says none is listed.

### Lightning strike coordinates
The NRSC–ISRO Bhuvan hourly point data for the last six completed hours (UTC). The dashboard shows the point count for all 35 Assam districts and lists the available coordinates, Bhuvan source timestamp, feed ID, and `current` value for returned points. Point counts use the current IMD district polygons. A zero means Bhuvan returned no point inside that polygon in the queried window; it does not prove lightning did not occur. The source timestamp is displayed as supplied by Bhuvan, without assuming its timezone. The dashboard also shows the DIWIS fetch age and query window; if the displayed fetch is over 12 hours old, it is marked **STALE**.

### Data freshness labels
The dashboard and generated PDF distinguish **DIWIS fetch time** from the source's observation or issue date. The current rainfall date, warning issue date, nowcast issue/validity, and lightning source window are shown where the feed provides them. A fetch older than 12 hours is labeled **STALE**; that label describes DIWIS's cached session result, not an independent claim that the source's data is stale. A source that provides no reliable update time is explicitly identified as such. A failed nowcast recheck retains the last verified message only with a **STALE** or **Expired** status. Refreshing requests fresh source responses, but cannot prove that an external feed has updated its underlying content.

### District names
- Exact match first, then close spelling (similarity 0.88 or higher), and only when exactly one label qualifies. If two labels are equally close, nothing is matched.
- A small alias list covers real naming differences: Kamrup Metropolitan / Kamrup Metro / Guwahati, Karimganj / Sribhumi, Saiha / Siaha, Karbi Anglong / Karbi Analog. A bare "Kamrup" label is accepted for Kamrup Metropolitan only as a weak alias, when no stronger label (its own name, Kamrup Metro, Guwahati) exists. Aliases affect matching only. The source's own label is still shown.
- Warnings and nowcast may also match by near-identical boundary shape when IMD uses an old name.

---

## Changes made in this review

1. **Saiha forecast fixed.** The Aizawl PDF spells it "SIAHA", which scored too low against "Saiha". An alias now covers both.
2. **District names corrected.** "Karbi Analog" shows as Karbi Anglong, "Lawngtlai2" is merged into Lawngtlai, Karimganj shows as Sribhumi, and IMD's "Kamrup" shows as Kamrup Metropolitan (Kamrup Rural is unchanged). Accounts locked to "Karimganj" or "Kamrup" must be re-created under the new names.
3. **Page value first, grid only as fallback.** Districts such as Mamit, Aizawl, Dima Hasao, North Tripura, Kohima and Kolasib use their IMD page value even where the grid differs. Grid values are shown, and labelled, only for districts with no page value.
4. **Data sources moved to its own menu page** instead of a long sidebar list.
5. **Expired nowcast text shortened** to "Expired · date time IST", on the dashboard and in the PDF.
6. **Table error fixed.** The forecast table mixed numbers and "Not reported" text in the temperature columns, which caused Streamlit's Arrow conversion error. Those cells are now always text.
7. **`use_container_width` replaced** with `width="stretch"` throughout, so the deprecation warning is gone. This needs Streamlit 1.50 or newer.
8. **Wording updated** so the sidebar, PDF footer and this README no longer say the grid is used only for fully covered districts.

---

## Known open items (not verified or not resolved)

- **Lightning is unverified.** The feed could not be reached from the review environment. Run `check_lightning.py` on a stormy evening and compare with the Bhuvan portal.
- **Purba Bardhaman** has no rain forecast in the IMD feed or the Kolkata South Bengal PDF. Run `check_pdf_text.py` against `south_bengal.pdf` to see how it is spelled.
- **Longding and Kamjong** have no rainfall value, because the grid covers under 90% of them.
- **Nowcasts** for Mizoram and West Bengal were expired overnight. Recheck in daytime.
- **Temperature** is an Open-Meteo model forecast. The department should confirm this is acceptable.
- **Account lock-out.** Accounts have no failed-login lockout, and passwords need only 6 characters.
- The older audit report `district_integrity_audit_2026-10-24` used an out-of-date district list. Use `audit_districts.py` output instead.

---

## Running the audit and diagnostics

Run these from the folder holding `app.py`, on a machine that can reach IMD, RMC, Open-Meteo and Bhuvan.

```powershell
python audit_districts.py                    # Assam and neighbouring states
python audit_districts.py --states Assam     # only some states
python audit_districts.py --limit 5          # quick trial
python check_district_sources.py             # districts per IMD layer
python check_pdf_text.py                     # how a forecast PDF reads
python check_lightning.py                    # lightning feed check
```

Run the audit after 08:30 IST so the day's reports exist, and keep the CSV with the handover paperwork.

---

## Daily SQLite history

When a live load or refresh completes, DIWIS appends the selected districts' live response and forecast JSON in `data/diwis_historical.db`, table `live_daily_snapshots`. Each refresh is retained as a separate row, including multiple refreshes of the same district on the same local day. Existing databases are migrated without discarding their saved snapshots. Missing numbers stay SQL `NULL`.

For daily history independent of dashboard activity, run `.\setup_windows_scheduler.ps1` from an elevated PowerShell session. It registers `DIWIS_Daily_History_Collection` to collect every district currently offered by the app at 09:00 in the Windows system time zone. The task uses the current Windows account and runs while that account is logged in; missed runs are started when possible. The collector writes rotating logs to `logs/daily_snapshot.log`. It can also be run manually with `python daily_snapshot.py`; use `--limit 1 --db-path <temporary-db-path>` for a one-district test.

Keep the SQLite file on persistent storage and back it up under the department's retention policy. It holds accounts as well as weather history, so never include a populated database in a source-code handover.

---

## First-time setup

Python 3.10 or newer is recommended.

```powershell
python -m pip install -r requirements.txt
$env:DIWIS_ADMIN_PASSWORD = "use-a-unique-initial-secret"
streamlit run app.py
```

For deployment, set `ADMIN_PASSWORD` (and optionally `ADMIN_USERNAME`) in the hosting platform's secret store before first start. There is no default `admin/admin123` account and no shared district accounts. The superadmin creates individual accounts under **User administration**. On a local machine, `DIWIS_ADMIN_PASSWORD` is used only to create the first superadmin.

Use a persistent volume for `data/diwis_historical.db`. If the host runs several app instances, use a shared database service or a single-writer deployment instead of separate local SQLite files.

---

## Handover notes

- Start the app with `streamlit run app.py`.
- Keep `.streamlit/secrets.toml`, environment files and database files out of source control and handover archives.
- Confirm the hosting secret, persistent database path, backups and account set-up with the receiving department before launch.
- Before calling DIWIS an official service, validate the open items above and compare a sample of districts by hand against the IMD pages.
- The dashboard presents data only. Operators must keep following the department's official warning and response procedures.
