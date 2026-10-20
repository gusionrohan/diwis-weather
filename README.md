# District Integrated Weather Information System (DIWIS)

A specialized meteorological & hydrological intelligence platform integrating direct feeds from the India Meteorological Department ([mausam.imd.gov.in](https://mausam.imd.gov.in)), RMC Guwahati, and IITM-ILDN (DAMINI Lightning Network), backed by a centralized relational SQLite database (WAL mode) for historical trend analysis.

---

## 📊 Core Capabilities

1. **Target District & Predictor Engine**: Dynamic primary district monitoring with upstream river catchment inflow tracking across neighbouring states and districts.
2. **5-Day District-Wise Spatial Rainfall Forecast**: Intensity (*Scattered, Isolated, Widespread*) and spatial station coverage percentages (*26–50%, 1–25%*).
3. **5-Day Severe Weather Hazard Warnings**: Official IMD hazard categories (*Thunderstorms, Lightning, Squalls*) and color alert levels (*🟡 Yellow Watch*, *🟢 Green No Warning*, *🟠 Orange Alert*, *🔴 Red Warning*).
4. **Past 24h Observed Rainfall**: Actual rainfall received in mm, normal benchmark, and percentage departure.
5. **Real-Time 3-Hour District Nowcast**: Immediate short-range convective storm warnings and safety directives from RMC Guwahati.
6. **IITM-ILDN / DAMINI Ground Lightning Coordinates**: Live ground lightning strike sensor fixes filtered strictly within target district boundaries.
7. **🏛️ Central SQL Historical Database & Trends Engine**: Multi-process persistence to `data/diwis_historical.db` with SQLite Write-Ahead Logging (WAL), connection pooling, and interactive SQL query workbench.
8. **🔐 Salted Scrypt Authentication & District Locking**: Role-based access control (Super Administrator, District Administrator, District Staff) protected with NIST-approved Salted Scrypt key derivation and strict district isolation.
9. **👥 District Admin Staff Management**: In every district login, District Admins can provision staff accounts, manage passwords, and oversee operators within their designated district.
10. **Government Standard Reports (PDF & Markdown)**: Official Assam DDMA daily meteorological intelligence reports with full source attribution.

---

## 🔐 Authentication & Role-Based Access Control (RBAC)

| Role | Default Username Format | Initial Password | Permissions |
| :--- | :--- | :--- | :--- |
| **State Super Admin** | `admin` | `admin123` | Universal access across all 35 Assam districts, manage all users |
| **District DDMA Admin** | `admin_<district>` *(e.g. `admin_hailakandi`)* | `admin123` | Locked to selected district, manage & create district staff |
| **District Staff** | Created by District Admin | Assigned by Admin | Locked to district, view dashboard & trigger IMD/SQL synchronizations |

> **Password Security**: All user passwords are encrypted using **Salted Scrypt hashing** (`hashlib.scrypt`). Users can change their own passwords anytime via the profile ribbon with verification of their current password.

---

## 🖥️ Interactive Web Dashboard

Launch the visual dashboard locally:

```powershell
python -m streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## ⏰ Automated Scheduling & SQL Database Sync

### 1. Windows Task Scheduler
The scraper can be registered in Windows Task Scheduler under task name `DHARA_Weather_SQL_Sync` to run **twice daily at 08:45 AM and 04:45 PM IST**:

```powershell
powershell -ExecutionPolicy Bypass -File setup_windows_scheduler.ps1
```

### 2. Python Standalone Background Scheduler
Run continuously across all configured target districts:
```powershell
python scheduler.py
```
To synchronize all 35 Assam districts in batch:
```powershell
python scheduler.py --all-districts
```

---

## 📁 File Structure

```text
d:/WebScrap/
├── app.py                             # DIWIS Streamlit Application
├── weather_scraper.py                 # Dynamic IMD/ILDN scraper engine
├── db_manager.py                      # SQLite database manager & query engine (WAL Mode, Scrypt)
├── geo_registry.py                    # Northeast districts & river basin registry
├── generate_daily_report.py           # Government standard PDF & MD report generator
├── scheduler.py                       # Automated background sync scheduler
├── run_sync.bat                       # Batch runner for automated execution
├── setup_windows_scheduler.ps1        # Windows Task Scheduler registration script
├── README.md                          # Documentation
├── data/                              # Centralized database directory
│   └── diwis_historical.db            # Central SQLite relational database (WAL mode)
└── output/                            # District-partitioned generated data & dossiers
    ├── hailakandi/
    │   ├── hailakandi_weather_forecast.json
    │   ├── hailakandi_forecast_summary.csv
    │   ├── DDMA_hailakandi_Daily_Weather_Report.pdf
    │   └── DDMA_hailakandi_Daily_Weather_Report.md
    └── ... (partitioned per district)
```
