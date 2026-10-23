"""
DIWIS Database Manager (SQLite / SQL Engine)
District Integrated Weather Information System
Stores daily weather observations, 5-day forecasts, lightning strike sensor records,
and upstream catchment inflows into structured relational SQL tables for historical analysis.
Features:
- Cryptographically secure password hashing (Salted Scrypt) with auto-upgrade from legacy MD5.
- Multi-process connection safety with SQLite Write-Ahead Logging (WAL) and connection timeouts.
- Scientific data integrity with NULL-preserving numeric parsing (no 0.0 pollution).
- Forecast cycle preservation (Morning vs Evening bulletin collision protection).
"""

import os
import sqlite3
import json
import hashlib
import hmac
import secrets
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DEFAULT_DB_PATH = os.path.join(DATA_DIR, "diwis_historical.db")
LEGACY_DB_PATH = os.path.join(BASE_DIR, "output_hailakandi", "dhara_historical.db")


def resolve_db_path(db_path: str = None) -> str:
    """Resolves the active database path, seamlessly migrating legacy database if needed."""
    if db_path:
        return db_path
    if not os.path.exists(DEFAULT_DB_PATH) and os.path.exists(LEGACY_DB_PATH):
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            import shutil
            shutil.copy2(LEGACY_DB_PATH, DEFAULT_DB_PATH)
        except Exception:
            return LEGACY_DB_PATH
    return DEFAULT_DB_PATH


def get_connection(db_path: str = None) -> sqlite3.Connection:
    """Returns a SQLite database connection with row factory, WAL mode, and connection timeout."""
    target_path = resolve_db_path(db_path)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    conn = sqlite3.connect(target_path, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def init_db(db_path: str = None):
    """Initializes all relational SQL tables, indexes, and initial configurations if not present."""
    target_path = resolve_db_path(db_path)
    conn = get_connection(target_path)
    cursor = conn.cursor()

    # 1. Daily Observations (Actual Recorded Rainfall, Temperature, Humidity)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        district TEXT NOT NULL,
        state TEXT NOT NULL DEFAULT 'Assam',
        recorded_date TEXT NOT NULL,
        scraped_at TEXT NOT NULL,
        actual_rainfall_mm REAL,
        normal_rainfall_mm REAL,
        departure_pct REAL,
        departure_category TEXT,
        ambient_temp_c REAL,
        today_max_c REAL,
        today_min_c REAL,
        relative_humidity_pct REAL,
        wind_speed_kmh REAL,
        data_source TEXT DEFAULT 'IMD',
        telemetry_status TEXT DEFAULT 'OK',
        UNIQUE(district, recorded_date)
    )
    """)

    # 2. 5-Day Forecasts (Spatial Rainfall, Station Coverage, Severe Weather Warnings)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forecast_5days (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        district TEXT NOT NULL,
        forecast_issued_at TEXT NOT NULL,
        day_index INTEGER NOT NULL,
        target_date TEXT NOT NULL,
        rainfall_category TEXT,
        station_coverage TEXT,
        max_temp_c REAL,
        min_temp_c REAL,
        temp_departure_c REAL,
        alert_color TEXT DEFAULT 'Green',
        alert_level TEXT DEFAULT 'No Warning',
        warning_summary TEXT DEFAULT 'No Warning',
        UNIQUE(district, forecast_issued_at, day_index)
    )
    """)

    # 3. Lightning Strike Events (IITM-ILDN / DAMINI Sensor Coordinates)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lightning_sensor_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        district TEXT NOT NULL,
        detection_time_ist TEXT,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        nearest_locality TEXT,
        age_minutes REAL,
        inside_district_flag INTEGER DEFAULT 1,
        logged_at TEXT NOT NULL,
        sensor_source TEXT DEFAULT 'IITM-ILDN/DAMINI',
        UNIQUE(district, detection_time_ist, latitude, longitude)
    )
    """)

    # 4. Upstream Catchment & Inflow Predictor Tracker
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS upstream_catchment_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_district TEXT NOT NULL,
        upstream_district TEXT NOT NULL,
        upstream_state TEXT NOT NULL,
        record_date TEXT NOT NULL,
        river_link TEXT,
        past_24h_rainfall_mm REAL,
        departure_pct REAL,
        day1_rainfall_forecast TEXT,
        day1_station_coverage TEXT,
        imd_alert_color TEXT DEFAULT 'Green',
        imd_alert_level TEXT DEFAULT 'No Warning',
        imd_warning_summary TEXT DEFAULT 'No Warning',
        scraped_at TEXT NOT NULL,
        UNIQUE(target_district, upstream_district, record_date)
    )
    """)

    # 5. Short-Range 3-Hour Nowcast Bulletins
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nowcast_bulletins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        district TEXT NOT NULL,
        issued_at TEXT NOT NULL,
        alert_color TEXT DEFAULT 'Green',
        alert_level TEXT,
        warning_message TEXT,
        action_suggested TEXT,
        validity_window TEXT DEFAULT '0-3 Hours',
        agency TEXT DEFAULT 'RMC Guwahati / IMD'
    )
    """)

    # 6. Raw Snapshots Archive (Full JSON Blob storage for complete audit replay)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_snapshots_archive (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        district TEXT NOT NULL,
        snapshot_time TEXT NOT NULL,
        full_json TEXT NOT NULL
    )
    """)

    # 7. Live DIWIS district snapshots: every verified feed response per selected
    # district and local calendar day, with raw JSON retained for analysis.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS live_daily_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        snapshot_date TEXT NOT NULL,
        synced_at TEXT NOT NULL,
        kind TEXT NOT NULL,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        observed_rainfall_mm REAL,
        observed_rainfall_date TEXT,
        rainfall_source TEXT,
        rainfall_status TEXT,
        live_json TEXT NOT NULL,
        forecast_json TEXT NOT NULL
    )
    """)
    unique_snapshot_index = None
    for index in cursor.execute("PRAGMA index_list(live_daily_snapshots)").fetchall():
        if not index["unique"]:
            continue
        columns = {row["name"] for row in cursor.execute(
            f"PRAGMA index_info('{index['name']}')"
        ).fetchall()}
        if columns == {"snapshot_date", "kind", "state", "district"}:
            unique_snapshot_index = index["name"]
            break
    if unique_snapshot_index:
        cursor.execute("""
            CREATE TABLE live_daily_snapshots_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_date TEXT NOT NULL,
                synced_at TEXT NOT NULL,
                kind TEXT NOT NULL,
                state TEXT NOT NULL,
                district TEXT NOT NULL,
                observed_rainfall_mm REAL,
                observed_rainfall_date TEXT,
                rainfall_source TEXT,
                rainfall_status TEXT,
                live_json TEXT NOT NULL,
                forecast_json TEXT NOT NULL
            )
        """)
        cursor.execute("""
            INSERT INTO live_daily_snapshots_history (
                id, snapshot_date, synced_at, kind, state, district,
                observed_rainfall_mm, observed_rainfall_date, rainfall_source,
                rainfall_status, live_json, forecast_json
            )
            SELECT id, snapshot_date, synced_at, kind, state, district,
                   observed_rainfall_mm, observed_rainfall_date, rainfall_source,
                   rainfall_status, live_json, forecast_json
            FROM live_daily_snapshots
        """)
        cursor.execute("DROP TABLE live_daily_snapshots")
        cursor.execute("ALTER TABLE live_daily_snapshots_history RENAME TO live_daily_snapshots")

    # 8. Users and Authentication (Salted Scrypt Passwords & RBAC)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        full_name TEXT,
        role TEXT NOT NULL DEFAULT 'staff',
        district TEXT NOT NULL,
        created_at TEXT NOT NULL,
        created_by TEXT DEFAULT 'system',
        must_change_password INTEGER DEFAULT 0
    )
    """)

    # Automated schema migrations for existing legacy databases
    try:
        cursor.execute("ALTER TABLE daily_observations ADD COLUMN telemetry_status TEXT DEFAULT 'OK'")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN must_change_password INTEGER DEFAULT 0")
    except Exception:
        pass

    # Create Indexes for fast querying
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_obs_district_date ON daily_observations(district, recorded_date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fc_district_date ON forecast_5days(district, target_date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_lt_district_time ON lightning_sensor_events(district, detection_time_ist);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_up_target_date ON upstream_catchment_records(target_district, record_date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_district ON users(district);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_live_daily_location_date ON live_daily_snapshots(state, district, snapshot_date);")

    # Bootstrap only from an explicitly configured secret. Never ship a known
    # default password or pre-create district accounts with a shared credential.
    cursor.execute("SELECT COUNT(*) FROM users")
    bootstrap_pwd = os.environ.get("DIWIS_ADMIN_PASSWORD", "").strip()
    if cursor.fetchone()[0] == 0 and bootstrap_pwd:
        now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p_bootstrap = hash_password(bootstrap_pwd)
        must_change = 1
        
        # Master Super Administrator
        cursor.execute("""
        INSERT INTO users (username, password_hash, full_name, role, district, created_at, created_by, must_change_password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ('admin', p_bootstrap, 'State Super Administrator', 'superadmin', 'ALL', now_ts, 'system', must_change))

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    """Computes a cryptographically secure salted scrypt hash."""
    clean = str(password).strip().encode('utf-8')
    salt = secrets.token_hex(16)
    derived = hashlib.scrypt(clean, salt=salt.encode('utf-8'), n=16384, r=8, p=1)
    return f"scrypt${salt}${derived.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verifies password against salted scrypt (with legacy MD5 auto-upgrade support)."""
    if not password or not stored_hash:
        return False
    clean = str(password).strip().encode('utf-8')
    
    if stored_hash.startswith("scrypt$"):
        try:
            parts = stored_hash.split("$")
            if len(parts) == 3:
                _, salt_hex, key_hex = parts
                derived = hashlib.scrypt(clean, salt=salt_hex.encode('utf-8'), n=16384, r=8, p=1)
                return hmac.compare_digest(derived.hex(), key_hex)
        except Exception:
            return False
            
    # Legacy MD5 fallback for seamless backward-compatibility
    try:
        md5_hash = hashlib.md5(clean).hexdigest()
        return hmac.compare_digest(md5_hash, stored_hash)
    except Exception:
        return False


def hash_password_md5(password: str) -> str:
    """Deprecated: Retained for backward compatibility with external imports."""
    return hashlib.md5(str(password).strip().encode('utf-8')).hexdigest()


def authenticate_user(username: str, password: str, selected_district: str, db_path: str = None) -> tuple[bool, str, dict]:
    """
    Authenticates a user against SQLite users table with salted Scrypt password hashing.
    Transparently upgrades legacy MD5 passwords to Scrypt upon verified login.
    Enforces district locking for non-superadmin accounts.
    """
    target_path = resolve_db_path(db_path)
    init_db(target_path)
    conn = get_connection(target_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username.strip(),))
        user = cursor.fetchone()
        if not user:
            return False, "Invalid user ID or password.", None
        
        user_dict = dict(user)
        stored_hash = user_dict.get("password_hash", "")
        if not verify_password(password, stored_hash):
            return False, "Invalid user ID or password.", None
        
        # Transparent upgrade to Scrypt if old hash was MD5
        if not stored_hash.startswith("scrypt$"):
            upgraded_hash = hash_password(password)
            cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (upgraded_hash, user_dict["id"]))
            conn.commit()
            user_dict["password_hash"] = upgraded_hash
        
        role = user_dict.get("role", "staff")
        assigned_district = user_dict.get("district", "")
        
        # Superadmin can access any district
        if role == "superadmin":
            user_dict["active_district"] = selected_district
            return True, "Login successful as Super Administrator.", user_dict
        
        # District Admin and Staff must match the selected district
        if assigned_district.strip().lower() != selected_district.strip().lower():
            return False, f"Unauthorized: Account is locked to {assigned_district}.", None
        
        user_dict["active_district"] = assigned_district
        return True, f"Login successful as {role.replace('_', ' ').title()}.", user_dict
    except Exception as e:
        return False, f"Authentication error: {e}", None
    finally:
        conn.close()


def create_user(username: str, password: str, full_name: str, role: str, district: str, created_by: str = "system", db_path: str = None) -> tuple[bool, str]:
    """Creates a new user record with salted Scrypt password hashing."""
    target_path = resolve_db_path(db_path)
    init_db(target_path)
    conn = get_connection(target_path)
    cursor = conn.cursor()
    try:
        u_clean = username.strip().lower()
        if not u_clean:
            return False, "Username cannot be empty."
        if not password or len(password.strip()) < 6:
            return False, "Password must be at least 6 characters long."
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE LOWER(username) = ?", (u_clean,))
        if cursor.fetchone()[0] > 0:
            return False, f"Username '{u_clean}' already exists."
        
        pwd_hash = hash_password(password)
        now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
        INSERT INTO users (username, password_hash, full_name, role, district, created_at, created_by, must_change_password)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """, (u_clean, pwd_hash, full_name.strip(), role, district, now_ts, created_by))
        conn.commit()
        return True, f"User '{u_clean}' created successfully with role '{role}' for district '{district}'."
    except Exception as e:
        return False, f"Database error creating user: {e}"
    finally:
        conn.close()


def delete_user_by_admin(target_username: str, requester_user: dict, db_path: str = None) -> tuple[bool, str]:
    """
    Deletes a user account with RBAC enforcement:
    - Superadmin can delete any account except themselves.
    - District Admin can only delete staff accounts belonging to their assigned district.
    """
    target_path = resolve_db_path(db_path)
    init_db(target_path)
    conn = get_connection(target_path)
    cursor = conn.cursor()
    try:
        target_clean = target_username.strip().lower()
        req_username = requester_user.get("username", "").strip().lower()
        req_role = requester_user.get("role", "staff")
        req_district = requester_user.get("district", "")
        
        if target_clean == req_username:
            return False, "You cannot delete your own account."
        
        cursor.execute("SELECT * FROM users WHERE LOWER(username) = ?", (target_clean,))
        target = cursor.fetchone()
        if not target:
            return False, f"User '{target_clean}' not found."
        
        target_dict = dict(target)
        target_role = target_dict.get("role", "staff")
        target_dist = target_dict.get("district", "")
        
        if req_role == "superadmin":
            cursor.execute("DELETE FROM users WHERE LOWER(username) = ?", (target_clean,))
            conn.commit()
            return True, f"User '{target_clean}' deleted successfully."
        
        if req_role == "district_admin":
            if target_dist.lower() != req_district.lower():
                return False, f"Unauthorized: You can only delete users in your assigned district ({req_district})."
            if target_role != "staff":
                return False, "Unauthorized: District Admins can only delete staff accounts."
            
            cursor.execute("DELETE FROM users WHERE LOWER(username) = ?", (target_clean,))
            conn.commit()
            return True, f"Staff account '{target_clean}' deleted successfully."
        
        return False, "Unauthorized: Staff accounts cannot delete users."
    except Exception as e:
        return False, f"Database error: {e}"
    finally:
        conn.close()


def get_district_users(district_name: str = None, requester_role: str = "district_admin", db_path: str = None) -> list:
    """Fetches user accounts scoped by district and requester permissions."""
    target_path = resolve_db_path(db_path)
    init_db(target_path)
    conn = get_connection(target_path)
    cursor = conn.cursor()
    try:
        if requester_role == "superadmin" and (not district_name or district_name == "ALL"):
            cursor.execute("SELECT id, username, full_name, role, district, created_at, created_by FROM users ORDER BY district, role DESC, username ASC")
        elif requester_role == "superadmin" and district_name:
            cursor.execute("""
            SELECT id, username, full_name, role, district, created_at, created_by 
            FROM users 
            WHERE LOWER(district) = LOWER(?) 
            ORDER BY role DESC, username ASC
            """, (district_name,))
        else:
            cursor.execute("""
            SELECT id, username, full_name, role, district, created_at, created_by 
            FROM users 
            WHERE LOWER(district) = LOWER(?) AND role != 'superadmin'
            ORDER BY role DESC, username ASC
            """, (district_name,))
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"[SQL Error] get_district_users failed: {e}")
        return []
    finally:
        conn.close()


def update_user_password(
    username: str, 
    new_password: str, 
    current_password: str = None, 
    requester_role: str = None, 
    db_path: str = None
) -> tuple[bool, str]:
    """
    Updates user password with salted Scrypt hash.
    Enforces authorization:
    - Superadmin can reset any user's password directly (current_password not required).
    - Other users MUST provide valid current_password to authenticate the change.
    """
    if not new_password or len(new_password.strip()) < 6:
        return False, "Password must be at least 6 characters long."
    target_path = resolve_db_path(db_path)
    init_db(target_path)
    conn = get_connection(target_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, password_hash FROM users WHERE LOWER(username) = LOWER(?)", (username.strip(),))
        user = cursor.fetchone()
        if not user:
            return False, "User not found."
            
        stored_hash = user["password_hash"]
        if requester_role != "superadmin":
            if not current_password or not verify_password(current_password, stored_hash):
                return False, "Current password verification failed. Password was not changed."
                
        new_hash = hash_password(new_password)
        cursor.execute("UPDATE users SET password_hash = ?, must_change_password = 0 WHERE LOWER(username) = LOWER(?)", (new_hash, username.strip()))
        conn.commit()
        return True, f"Password for '{username}' updated successfully with secure encryption."
    except Exception as e:
        return False, f"Failed to update password: {e}"
    finally:
        conn.close()


def sync_admin_from_secrets(custom_password: str, custom_username: str = "admin", db_path: str = None) -> bool:
    """
    Dynamically configures or updates the Superadmin account using credentials provided
    via Streamlit Cloud Secrets (st.secrets['ADMIN_PASSWORD']) or environment variables.
    Ensures production passwords are never exposed in source code or public repositories.
    """
    if not custom_password or len(str(custom_password).strip()) < 6:
        return False
    target_path = resolve_db_path(db_path)
    init_db(target_path)
    conn = get_connection(target_path)
    cursor = conn.cursor()
    try:
        u_clean = str(custom_username).strip().lower()
        pwd_hash = hash_password(str(custom_password).strip())
        now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("SELECT id FROM users WHERE LOWER(username) = ?", (u_clean,))
        row = cursor.fetchone()
        if row:
            cursor.execute("UPDATE users SET password_hash = ?, must_change_password = 0 WHERE id = ?", (pwd_hash, row[0]))
        else:
            cursor.execute("""
            INSERT INTO users (username, password_hash, full_name, role, district, created_at, created_by, must_change_password)
            VALUES (?, ?, ?, 'superadmin', 'ALL', ?, 'secrets', 0)
            """, (u_clean, pwd_hash, "State Super Administrator", now_ts))
        conn.commit()
        return True
    except Exception as e:
        print(f"[!] sync_admin_from_secrets error: {e}")
        return False
    finally:
        conn.close()


def save_snapshot_to_db(data: dict, db_path: str = None):
    """Saves a scraped weather data payload into all corresponding SQL relational tables."""
    if not data:
        return

    target_path = resolve_db_path(db_path)
    init_db(target_path)
    conn = get_connection(target_path)
    cursor = conn.cursor()

    try:
        target = data.get("metadata", {}).get("target_location", {})
        district = target.get("district", "Unknown")
        state = target.get("state", "Assam")
        scraped_at = data.get("metadata", {}).get("scraped_at_local", datetime.now().isoformat())

        # 1. Save Daily Observations (NULL-preserving)
        obs = data.get("observed_rainfall_past24h", {})
        temp_obs = data.get("temperature_data", {}).get("current_observation") or {}
        
        rec_date = obs.get("recorded_date", datetime.now().strftime("%Y-%m-%d"))
        actual_rf = _parse_float(obs.get("actual_rainfall_mm"))
        norm_rf = _parse_float(obs.get("normal_rainfall_mm"))
        dep_pct = _parse_float(obs.get("departure_percentage"))
        dep_cat = obs.get("departure_category", "Data Unavailable")
        telemetry_st = obs.get("status", "UNAVAILABLE")
        
        amb_temp = _parse_float(temp_obs.get("temperature_c"))
        max_temp = _parse_float(temp_obs.get("today_max_c"))
        min_temp = _parse_float(temp_obs.get("today_min_c"))
        humidity = _parse_float(temp_obs.get("relative_humidity_pct"))
        wind_spd = _parse_float(temp_obs.get("wind_speed_kmh"))

        cursor.execute("""
        INSERT INTO daily_observations (
            district, state, recorded_date, scraped_at,
            actual_rainfall_mm, normal_rainfall_mm, departure_pct, departure_category,
            ambient_temp_c, today_max_c, today_min_c, relative_humidity_pct, wind_speed_kmh,
            telemetry_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(district, recorded_date) DO UPDATE SET
            scraped_at=excluded.scraped_at,
            actual_rainfall_mm=excluded.actual_rainfall_mm,
            normal_rainfall_mm=excluded.normal_rainfall_mm,
            departure_pct=excluded.departure_pct,
            departure_category=excluded.departure_category,
            ambient_temp_c=excluded.ambient_temp_c,
            today_max_c=excluded.today_max_c,
            today_min_c=excluded.today_min_c,
            relative_humidity_pct=excluded.relative_humidity_pct,
            wind_speed_kmh=excluded.wind_speed_kmh,
            telemetry_status=excluded.telemetry_status
        """, (
            district, state, rec_date, scraped_at,
            actual_rf, norm_rf, dep_pct, dep_cat,
            amb_temp, max_temp, min_temp, humidity, wind_spd,
            telemetry_st
        ))

        # 2. Save 5-Day Forecasts (Morning vs. Evening cycle preserved)
        rainfall_fc = data.get("rainfall_forecast_5days", [])
        warnings_fc = data.get("severe_weather_warnings_5days", {}).get("daily_warnings", [])
        temp_fc = data.get("temperature_data", {}).get("daily_temperature_forecast_5days", [])
        
        # Distinguish Morning vs Evening forecast cycle to prevent mutual collision
        hour = datetime.now().hour
        cycle = "Morning" if hour < 14 else "Evening"
        issue_time = f"{scraped_at[:10]} {cycle}"

        for idx, rf in enumerate(rainfall_fc):
            day_idx = rf.get("day_index", idx + 1)
            t_date = rf.get("date", "")
            rf_cat = rf.get("rainfall_category", "N/A")
            st_cov = rf.get("station_coverage", "N/A")

            w = warnings_fc[idx] if idx < len(warnings_fc) else {}
            t = temp_fc[idx] if idx < len(temp_fc) else {}

            w_col = w.get("alert_color")
            w_lvl = w.get("alert_level", "Warning status unavailable")
            w_sum = w.get("warning_summary", "Data Unavailable")

            t_max = _parse_float(t.get("max_temp_c"))
            t_min = _parse_float(t.get("min_temp_c"))
            t_dep = _parse_float(t.get("departure_c"))

            cursor.execute("""
            INSERT INTO forecast_5days (
                district, forecast_issued_at, day_index, target_date,
                rainfall_category, station_coverage, max_temp_c, min_temp_c, temp_departure_c,
                alert_color, alert_level, warning_summary
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(district, forecast_issued_at, day_index) DO UPDATE SET
                target_date=excluded.target_date,
                rainfall_category=excluded.rainfall_category,
                station_coverage=excluded.station_coverage,
                max_temp_c=excluded.max_temp_c,
                min_temp_c=excluded.min_temp_c,
                temp_departure_c=excluded.temp_departure_c,
                alert_color=excluded.alert_color,
                alert_level=excluded.alert_level,
                warning_summary=excluded.warning_summary
            """, (
                district, issue_time, day_idx, t_date,
                rf_cat, st_cov, t_max, t_min, t_dep,
                w_col, w_lvl, w_sum
            ))

        # 3. Save Lightning Strike Sensor Events
        damini = data.get("damini_sensor_lightning", {})
        strikes_inside = damini.get("strikes_inside_district", [])
        for st_item in strikes_inside:
            cursor.execute("""
            INSERT INTO lightning_sensor_events (
                district, detection_time_ist, latitude, longitude,
                nearest_locality, age_minutes, inside_district_flag, logged_at
            ) VALUES (?, ?, ?, ?, ?, ?, 1, ?)
            ON CONFLICT(district, detection_time_ist, latitude, longitude) DO NOTHING
            """, (
                district,
                st_item.get("timestamp_ist"),
                _parse_float(st_item.get("latitude")),
                _parse_float(st_item.get("longitude")),
                st_item.get("nearest_locality"),
                _parse_float(st_item.get("age_minutes")),
                scraped_at
            ))

        # 4. Save Upstream Catchment Inflow Predictors
        upstream = data.get("upstream_catchment_rainfall") or data.get("upstream_mizoram_rainfall", [])
        for u in upstream:
            up_dist = u.get("upstream_district", "Unknown")
            up_state = u.get("state", "Northeast")
            r_link = u.get("river_link", u.get("river_link_to_hailakandi", ""))
            past_rf = _parse_float(u.get("past_24h_actual_rainfall"))
            dep_val = _parse_float(u.get("past_24h_departure"))
            
            f1 = u.get("forecast_5days", [{}])[0]
            f1_c = f1.get("rainfall_category", "N/A")
            f1_cov = f1.get("station_coverage", "N/A")
            
            w_c = u.get("imd_alert_color")
            w_l = u.get("imd_alert_level", "Warning status unavailable")
            w_s = u.get("imd_warning_summary", "Data Unavailable")

            cursor.execute("""
            INSERT INTO upstream_catchment_records (
                target_district, upstream_district, upstream_state, record_date,
                river_link, past_24h_rainfall_mm, departure_pct,
                day1_rainfall_forecast, day1_station_coverage,
                imd_alert_color, imd_alert_level, imd_warning_summary, scraped_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(target_district, upstream_district, record_date) DO UPDATE SET
                river_link=excluded.river_link,
                past_24h_rainfall_mm=excluded.past_24h_rainfall_mm,
                departure_pct=excluded.departure_pct,
                day1_rainfall_forecast=excluded.day1_rainfall_forecast,
                day1_station_coverage=excluded.day1_station_coverage,
                imd_alert_color=excluded.imd_alert_color,
                imd_alert_level=excluded.imd_alert_level,
                imd_warning_summary=excluded.imd_warning_summary,
                scraped_at=excluded.scraped_at
            """, (
                district, up_dist, up_state, rec_date,
                r_link, past_rf, dep_val,
                f1_c, f1_cov, w_c, w_l, w_s, scraped_at
            ))

        # 5. Save Short-Range Nowcast Bulletin (with deduplication)
        nowcast = data.get("current_nowcast_warning", {})
        if nowcast and nowcast.get("message"):
            msg_txt = nowcast.get("message", "")
            cursor.execute("""
            SELECT id FROM nowcast_bulletins 
            WHERE district = ? AND alert_color = ? AND warning_message = ? 
            ORDER BY id DESC LIMIT 1
            """, (district, nowcast.get("alert_color"), msg_txt))
            if not cursor.fetchone():
                cursor.execute("""
                INSERT INTO nowcast_bulletins (
                    district, issued_at, alert_color, alert_level, warning_message, action_suggested
                ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    district,
                    scraped_at,
                    nowcast.get("alert_color"),
                    nowcast.get("alert_level", "Nowcast status unavailable"),
                    msg_txt,
                    nowcast.get("action_suggested", "")
                ))

        # 6. Archive Raw JSON Snapshot
        cursor.execute("""
        INSERT INTO raw_snapshots_archive (district, snapshot_time, full_json)
        VALUES (?, ?, ?)
        """, (district, scraped_at, json.dumps(data, ensure_ascii=False)))

        conn.commit()
        print(f"[SQL] Successfully saved daily snapshot to SQLite database ({target_path}) for {district}!")

    except Exception as e:
        print(f"[SQL Error] Failed to write data to SQLite database: {e}")
    finally:
        conn.close()


def save_live_daily_snapshot(live_results: list, forecast_results: list,
                             db_path: str = None) -> int:
    """Append live app responses to history for the selected districts.

    Values and source statuses are stored as returned by the live feeds. Missing
    measurements remain SQL NULL and are never converted to zero or inferred.
    """
    live_by_key = {
        (item.get("kind"), item.get("state"), item.get("district")): item
        for item in (live_results or []) if isinstance(item, dict)
    }
    forecast_by_key = {
        (item.get("kind"), item.get("state"), item.get("district")): item
        for item in (forecast_results or []) if isinstance(item, dict)
    }
    keys = list(live_by_key)
    keys.extend(key for key in forecast_by_key if key not in live_by_key)
    if not keys:
        return 0

    synced_at = datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(timespec="seconds")
    snapshot_date = synced_at[:10]
    target_path = resolve_db_path(db_path)
    init_db(target_path)
    conn = get_connection(target_path)
    try:
        for kind, state, district in keys:
            live = live_by_key.get((kind, state, district), {})
            forecast = forecast_by_key.get((kind, state, district), {})
            rainfall = live.get("rainfall") or {}
            rainfall_value = rainfall.get("value_mm") if rainfall.get("status") == "OK" else None
            rainfall_value = _parse_float(rainfall_value)
            live_json = json.dumps(live, ensure_ascii=False, default=str)
            forecast_json = json.dumps(forecast, ensure_ascii=False, default=str)
            conn.execute("""
                INSERT INTO live_daily_snapshots (
                    snapshot_date, synced_at, kind, state, district,
                    observed_rainfall_mm, observed_rainfall_date, rainfall_source,
                    rainfall_status, live_json, forecast_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                snapshot_date, synced_at, kind or "", state or "", district or "",
                rainfall_value, rainfall.get("date"), rainfall.get("source"),
                rainfall.get("status") or ("ERROR" if live.get("error") else "NOT_REPORTED"),
                live_json, forecast_json,
            ))
        conn.commit()
        return len(keys)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def query_dataframe(query: str, params: tuple = (), db_path: str = None) -> pd.DataFrame:
    """Executes a SQL query and returns results directly as a Pandas DataFrame."""
    target_path = resolve_db_path(db_path)
    init_db(target_path)
    conn = get_connection(target_path)
    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        print(f"[SQL Error] Query execution failed: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def get_all_tables_stats(db_path: str = None) -> dict:
    """Returns row counts and metadata for all SQL tables in the database."""
    target_path = resolve_db_path(db_path)
    init_db(target_path)
    conn = get_connection(target_path)
    cursor = conn.cursor()
    tables = [
        "daily_observations",
        "forecast_5days",
        "lightning_sensor_events",
        "upstream_catchment_records",
        "nowcast_bulletins",
        "raw_snapshots_archive"
    ]
    stats = {}
    for tbl in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tbl}")
            stats[tbl] = cursor.fetchone()[0]
        except Exception:
            stats[tbl] = 0
    conn.close()
    return stats


def get_district_tables_stats(district_name: str, db_path: str = None) -> dict:
    """Returns row counts specifically for the selected primary target district."""
    target_path = resolve_db_path(db_path)
    init_db(target_path)
    conn = get_connection(target_path)
    cursor = conn.cursor()
    stats = {
        "daily_observations": 0,
        "forecast_5days": 0,
        "lightning_sensor_events": 0,
        "upstream_catchment_records": 0
    }
    try:
        cursor.execute("SELECT COUNT(*) FROM daily_observations WHERE district = ?", (district_name,))
        stats["daily_observations"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM forecast_5days WHERE district = ?", (district_name,))
        stats["forecast_5days"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM lightning_sensor_events WHERE district = ?", (district_name,))
        stats["lightning_sensor_events"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM upstream_catchment_records WHERE target_district = ?", (district_name,))
        stats["upstream_catchment_records"] = cursor.fetchone()[0]
    except Exception as e:
        print(f"[SQL Error] District stats failed: {e}")
    finally:
        conn.close()
    return stats


def _parse_float(val) -> float | None:
    """Helper to safely parse numeric float values. Returns None for missing/invalid data (preserving SQL NULL)."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        import math
        return None if math.isnan(val) else float(val)
    try:
        clean = str(val).replace("mm", "").replace("%", "").replace("°C", "").replace("+", "").strip()
        if not clean or clean.lower() in ("n/a", "none", "null", "-", "--", "nan"):
            return None
        return float(clean)
    except Exception:
        return None
