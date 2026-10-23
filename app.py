"""Live district weather dashboard. Geography and weather are fetched on demand; no readings are persisted."""

from __future__ import annotations

import requests
import streamlit as st
import os
import re
import json
import html
import io
import math
import struct
from difflib import SequenceMatcher
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from shapely.geometry import shape, box
from shapely.ops import unary_union
from pypdf import PdfReader
from db_manager import (DEFAULT_DB_PATH, authenticate_user, update_user_password,
                        get_district_users, create_user, save_live_daily_snapshot,
                        sync_admin_from_secrets)


def format_clock_ampm(value):
    """Format visible 24-hour clock values as 12-hour time without changing their date/zone."""
    if value in (None, ""):
        return value
    text = str(value)
    def replace_clock(match):
        hour, minute, second = match.group(1), match.group(2), match.group(3)
        hour_num = int(hour)
        suffix = "AM" if hour_num < 12 else "PM"
        hour_12 = hour_num % 12 or 12
        return f"{hour_12:02d}:{minute}" + (f":{second}" if second else "") + f" {suffix}"
    text = re.sub(r"(?<!\d)([01]?\d|2[0-3]):([0-5]\d)(?::([0-5]\d))?(?!\d)", replace_clock, text)
    return text


def format_feed_clock(value):
    """Format a feed clock such as 0830 or 08:30 as 08:30 AM."""
    if value in (None, ""):
        return value
    raw = str(value).strip()
    for pattern in ("%H%M", "%H:%M", "%H:%M:%S"):
        try:
            return datetime.strptime(raw, pattern).strftime("%I:%M %p")
        except ValueError:
            pass
    return format_clock_ampm(raw)


def temperature_cell(value):
    """Temperature table cell as text: '30.2' or 'Not reported'."""
    if value in ("", "-", "--", None):
        return "Not reported"
    try:
        return f"{float(value):g}"
    except (TypeError, ValueError):
        return "Not reported"


def freshness_label(fetched_at, stale_after_minutes=12 * 60):
    """Describe DIWIS fetch age without implying the source itself is current."""
    if not fetched_at:
        return "Fetch time not recorded"
    try:
        fetched = datetime.fromisoformat(str(fetched_at))
        if fetched.tzinfo is None:
            fetched = fetched.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
        age_seconds = (datetime.now(ZoneInfo("Asia/Kolkata")) - fetched).total_seconds()
    except (ValueError, TypeError):
        return "Fetch time unreadable"
    if age_seconds < -60:
        return "Fetch time is in the future; check the system clock"
    age_minutes = max(0, int(age_seconds // 60))
    if age_minutes < 1:
        age = "less than 1 minute ago"
    elif age_minutes < 60:
        age = f"{age_minutes} minutes ago"
    else:
        hours, minutes = divmod(age_minutes, 60)
        age = f"{hours}h {minutes}m ago" if minutes else f"{hours}h ago"
    if age_minutes > stale_after_minutes:
        return f"STALE · fetched {age} (refresh overdue)"
    return f"Fetched {age}"


def warning_mentions_cyclone(warning):
    """Return whether a warning's coded hazards or source text mentions cyclone activity."""
    hazards = warning.get("hazards") or []
    text = " ".join(str(value) for value in hazards) + " " + str(warning.get("text") or "")
    return bool(re.search(r"\b(?:cyclone|cyclonic|depression)\b", text, re.I))


def nowcast_expiry_label(nowcast):
    """Short 'DD-MM-YYYY HH:MM AM/PM IST' text for when a nowcast entry stopped being valid."""
    try:
        return datetime.fromisoformat(str(nowcast.get("valid_until_at"))).strftime("%d-%m-%Y %I:%M %p IST")
    except (ValueError, TypeError):
        clock = format_feed_clock(nowcast.get("valid_until"))
        return f"{clock} IST" if clock else "time not reported"


st.set_page_config(
    page_title="DIWIS · District Integrated Weather Information System",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    :root { color-scheme: light; }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background: #f4f7f8 !important; color: #20313b !important;
    }
    [data-testid="stHeader"] { background: #f4f7f8 !important; }
    .block-container { max-width: 100% !important; min-height:100vh; background:#fff;
        padding: 1.4rem 3.2rem 3rem !important; }
    [data-testid="stSidebar"] {
        min-width: 320px !important; width: 320px !important;
        background: linear-gradient(180deg, #173b49 0%, #102d3a 100%) !important;
        border-right: 1px solid #244c5a;
    }
    [data-testid="stSidebar"] > div:first-child { padding: 0 1rem 1rem; }
    [data-testid="stSidebarUserContent"], [data-testid="stSidebarContent"] {
        padding-top:0 !important; margin-top:0 !important;
    }
    [data-testid="stSidebarHeader"] { display:none !important; height:0 !important; padding:0 !important; margin:0 !important; }
    [data-testid="stSidebar"] .block-container { padding-top:.15rem !important; }
    [data-testid="stSidebarCollapseButton"], [data-testid="stSidebarExpandButton"] { display:none !important; }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: .75rem; }
    .sidebar-brand { display:flex; align-items:center; gap:12px; padding:4px 12px 10px;
        margin:0 0 2px; border-bottom:1px solid rgba(255,255,255,.14); }
    .sidebar-brand-mark { width:42px; height:42px; display:grid; place-items:center;
        border-radius:12px; background:rgba(255,255,255,.13); color:#d9f2ec; font-size:21px; }
    .sidebar-brand-name { color:#fff; font-size:17px; font-weight:750; letter-spacing:-.02em; }
    .sidebar-brand-caption { color:#bdd0d6; font-size:11px; margin-top:2px; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color:#d3e0e4 !important; }
    [data-testid="stSidebar"] a { color:#9ee6d2 !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label { color:#e8f0f2 !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] > div { gap:5px; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding:9px 11px; border-radius:9px; transition:background .15s ease;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:#edf5f2; }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        border:1px solid #cbd8dc !important; border-radius:9px; min-height:43px;
        background:#fff !important; color:#20313b !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] input,
    [data-testid="stSidebar"] [data-baseweb="select"] [data-testid="stMarkdownContainer"] {
        color:#20313b !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] svg { fill:#36515d !important; }
    [data-testid="stSidebar"] [data-baseweb="popover"],
    [data-testid="stSidebar"] [data-baseweb="popover"] ul {
        background:#fff !important; color:#20313b !important;
    }
    [data-testid="stSidebar"] [data-baseweb="popover"] li {
        color:#20313b !important; background:#fff !important;
    }
    [data-testid="stSidebar"] [data-baseweb="popover"] li:hover {
        background:#edf5f2 !important;
    }
    h1, h2, h3 { color: #193b4a !important; }
    .login-shell { max-width:1060px; margin:8vh auto 0; padding:12px; border-radius:24px;
        background:linear-gradient(135deg,#287a68 0%,#255f78 58%,#6a83a4 100%);
        box-shadow:0 24px 70px rgba(29,68,82,.18); }
    div[data-testid="stHorizontalBlock"]:has(.login-welcome) {
        max-width:1060px; margin:8vh auto 0; padding:12px; gap:0 !important;
        border-radius:24px; background:linear-gradient(135deg,#287a68 0%,#255f78 58%,#6a83a4 100%);
        box-shadow:0 24px 70px rgba(29,68,82,.18); }
    .login-welcome { min-height:430px; height:100%; box-sizing:border-box; padding:54px 38px;
        border-radius:16px 0 0 16px; color:#fff;
        background:radial-gradient(circle at 85% 18%,rgba(255,255,255,.18),transparent 29%),
                   linear-gradient(150deg,#287a68 0%,#25677a 58%,#527d96 100%);
        display:flex; flex-direction:column; justify-content:center; }
    .login-welcome-mark { width:54px; height:54px; border-radius:15px; display:grid; place-items:center;
        background:rgba(255,255,255,.16); font-size:27px; margin-bottom:25px; }
    .login-welcome h1 { color:#fff !important; font-size:32px; line-height:1.18; margin:0 0 14px; }
    .login-welcome p { color:#e4f0f1; font-size:15px; line-height:1.65; margin:0; max-width:390px; }
    .login-welcome .login-caption { color:#d3e5e7; font-size:12px; margin-top:30px; letter-spacing:.04em; }
    .st-key-login_form_col { min-height:430px; height:100%; background:rgba(255,255,255,.97);
        border-radius:0 16px 16px 0; padding:28px 34px; box-sizing:border-box; }
    .login-form-title { color:#193b4a; font-size:22px; font-weight:700; margin:0 0 4px; }
    .login-form-hint { color:#71818a; font-size:13px; margin:0 0 22px; }
    .st-key-login_form_col [data-testid="stForm"] { background:transparent; border:0; padding:0; box-shadow:none; backdrop-filter:none; }
    .st-key-login_form_col [data-testid="stForm"] label { color:#304c59 !important; }
    [data-testid="stForm"] { background:rgba(255,255,255,.82); border:1px solid rgba(255,255,255,.9);
        border-radius:14px; padding:22px; box-shadow:0 16px 42px rgba(31,65,77,.12);
        backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px); }
    [data-testid="stExpander"] { background:#fff; border:1px solid #dbe5e8; border-radius:8px; }
    div.stButton > button[kind="primary"] { background:#287a68; border-color:#287a68; }
    div.stButton > button[kind="primary"]:hover { background:#1d6253; border-color:#1d6253; }
    [data-testid="stMetric"] { background:#fff; border:1px solid #dbe5e8; border-radius:8px; padding:16px; }
    [data-testid="stAlert"] { border-radius:7px; }
    div[data-baseweb="select"] > div { background:#fff; }
    a { color:#176b5b !important; }
    @media (max-width: 700px) {
        .block-container { padding:1rem !important; }
        [data-testid="stSidebar"] { min-width:290px !important; width:290px !important; }
        div[data-testid="stHorizontalBlock"]:has(.login-welcome) { margin:1rem auto 0; padding:8px; }
        .login-welcome { min-height:250px; border-radius:14px 14px 0 0; padding:30px 24px; }
        .login-welcome h1 { font-size:26px; }
        .st-key-login_form_col { min-height:unset; border-radius:0 0 14px 14px; padding:24px; }
    }
</style>
""", unsafe_allow_html=True)

IMD_WFS = "https://reactjs.imd.gov.in/geoserver/wfs"
HEADERS = {"User-Agent": "AssamDistrictWeather/1.0 (live public data dashboard)"}
DB_PATH = DEFAULT_DB_PATH  # User accounts and daily live weather snapshots.
DATA_PIPELINE_VERSION = "public-imd-district-wfs-feeds-21"
try:
    admin_password = st.secrets.get("ADMIN_PASSWORD") or __import__("os").environ.get("DIWIS_ADMIN_PASSWORD")
    if admin_password:
        admin_username = st.secrets.get("ADMIN_USERNAME") or __import__("os").environ.get("DIWIS_ADMIN_USERNAME") or "admin"
        sync_admin_from_secrets(str(admin_password).strip(), str(admin_username).strip(), db_path=DB_PATH)
except Exception:
    pass


def fetch_json(url: str, timeout: int = 20, headers=None, params=None):
    response = requests.get(url, headers=headers or HEADERS, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


# Administrative polygons are geography, not weather observations. Keep the live WFS
# response in Streamlit's in-memory cache so sign-in and selector reruns are immediate.
@st.cache_data(ttl=6 * 60 * 60, show_spinner=False)
def boundary(level: str):
    layer = {"ADM1": "imd:India_State", "ADM2": "imd:india_districts"}.get(level)
    if not layer:
        raise ValueError("Unsupported IMD boundary level.")
    return fetch_json(IMD_WFS, timeout=25, params={
        "service": "WFS", "version": "1.1.0", "request": "GetFeature",
        "typename": layer, "srsname": "EPSG:4326", "outputFormat": "application/json",
    })


def current_district_revision(features, state_names):
    """Group IMD nowcast-layer district polygons by state.

    IMD's nowcast layer follows the current district revision (the older boundary layer
    still lacks newer districts such as Majuli or Hojai), so it can complete the list.
    Returns {state: {district_name: geometry}}; pieces sharing a name are merged.
    """
    state_lookup = {normalized(name): name for name in state_names}
    grouped = {}
    for feature in features or []:
        props = feature.get("properties") or {}
        parent = state_lookup.get(normalized(props.get("State")))
        geom_data = feature.get("geometry")
        raw_name = str(props.get("State_District") or props.get("District") or "").strip()
        if not parent or not geom_data or not raw_name:
            continue
        prefixed = re.match(rf"^{re.escape(parent)}\s*[-_:/,]\s*(.+)$", raw_name, re.I)
        name = prefixed.group(1).strip() if prefixed else raw_name
        if name.isupper():
            name = name.title()
        try:
            geom = shape(geom_data)
            if not geom.is_valid:
                geom = geom.buffer(0)
        except Exception:
            continue
        if geom.is_empty:
            continue
        grouped.setdefault(parent, {}).setdefault(normalized(name), [name, []])[1].append(geom)
    # IMD labels a district's second polygon with a trailing digit (e.g. "Lawngtlai2"); fold
    # it into the base district when that base name exists in the same state.
    for items in grouped.values():
        for key in [k for k in items if re.search(r"[a-z]\d$", k)]:
            base_key = key[:-1].strip()
            if base_key in items and base_key != key:
                items[base_key][1].extend(items.pop(key)[1])
    return {parent: {name: (parts[0] if len(parts) == 1 else unary_union(parts))
                     for name, parts in items.values()}
            for parent, items in grouped.items()}


# Names IMD's layers print wrongly or out of date. Keys are normalized source labels; values
# are the names shown in DIWIS. Feed matching still accepts both spellings (see DISTRICT_LABEL_ALIASES).
DISTRICT_DISPLAY_FIXES = {
    "karbi analog": "Karbi Anglong",   # IMD typo
    "karimganj": "Sribhumi",           # renamed district
}


def tidy_district_names(district_state, district_geometries):
    """Merge IMD's split polygons ('Lawngtlai2' into 'Lawngtlai') and fix known wrong names, in place."""
    for key in list(district_geometries):
        parent, name = key
        match = re.match(r"^(.*\D)\s*\d+$", name)
        if not match:
            continue
        base_key = (parent, match.group(1).strip())
        if base_key in district_geometries and base_key != key:
            district_geometries[base_key] = unary_union([district_geometries[base_key], district_geometries[key]])
            district_geometries.pop(key, None)
            district_state.pop(key, None)
    # In IMD's maps "Kamrup" is Kamrup Metropolitan (Guwahati) and "Kamrup Rural" is Kamrup Rural
    # (confirmed by the department). Show the Metropolitan name when IMD does not use it itself.
    assam = next((p for p, _n in district_geometries if normalized(p) == "assam"), None)
    if assam:
        by_name = {normalized(n): (p, n) for (p, n) in district_geometries if p == assam}
        kamrup, rural = by_name.get("kamrup"), by_name.get("kamrup rural")
        has_metro = "kamrup metropolitan" in by_name or "kamrup metro" in by_name
        if kamrup and rural and not has_metro:
            metro_key = (assam, "Kamrup Metropolitan")
            district_geometries[metro_key] = district_geometries.pop(kamrup)
            district_state.pop(kamrup, None)
            district_state[metro_key] = assam
    for key in list(district_geometries):
        parent, name = key
        fixed = DISTRICT_DISPLAY_FIXES.get(normalized(name))
        if fixed and (parent, fixed) not in district_geometries:
            district_geometries[(parent, fixed)] = district_geometries.pop(key)
            district_state.pop(key, None)
            district_state[(parent, fixed)] = parent


@st.cache_resource(ttl=6 * 60 * 60, show_spinner=False)
def live_administrative_geography():
    """Load live IMD boundaries and build selector geometry once per process."""
    # The state and district services are independent; fetch them together so a cold
    # login does not wait for two sequential network timeouts.
    with ThreadPoolExecutor(max_workers=3) as pool:
        nowcast_future = pool.submit(live_imd_district_feed, IMD_DISTRICT_NOWCAST_LAYER)
        states_geo, districts_geo = pool.map(boundary, ("ADM1", "ADM2"))
        try:
            nowcast_layer = nowcast_future.result()
        except Exception:
            nowcast_layer = None  # keep the boundary-layer list if the nowcast layer is unreachable
    states = states_geo.get("features", [])
    districts = districts_geo.get("features", [])
    assam = next((f for f in states if feature_name(f).casefold() == "assam"), None)
    if assam is None:
        raise ValueError("Assam was not returned by the live administrative-boundary service.")
    assam_shape = shape(assam["geometry"])
    state_shapes = [(feature_name(f), shape(f["geometry"])) for f in states
                    if feature_name(f) and f.get("geometry")]
    neighbor_candidates = sorted(
        [name for name, _geom in state_shapes if name.casefold() == "assam"]
        + [name for name, geom in state_shapes
           if name.casefold() != "assam" and assam_shape.boundary.intersects(geom.boundary)],
        key=normalized,
    )
    district_state = {}
    district_geometries = {}
    for feature in districts:
        geom_data = feature.get("geometry")
        name = feature_name(feature)
        if not geom_data or not name:
            continue
        district_shape = shape(geom_data)
        center = district_shape.representative_point()
        parent = next((state for state, state_geom in state_shapes if state_geom.covers(center)), None)
        if parent:
            key = (parent, name)
            district_state[key] = parent
            district_geometries[key] = district_shape
    # Complete each relevant state from IMD's current district revision, but only when that
    # layer lists at least as many districts as the boundary layer (it never shrinks a list).
    if nowcast_layer:
        relevant = set(neighbor_candidates)
        revised = current_district_revision(nowcast_layer, relevant)
        for parent, districts_now in revised.items():
            existing = [key for key in district_state if key[0] == parent]
            if len(districts_now) >= len(existing):
                for key in existing:
                    district_state.pop(key, None)
                    district_geometries.pop(key, None)
                for name, geom in districts_now.items():
                    district_state[(parent, name)] = parent
                    district_geometries[(parent, name)] = geom
    tidy_district_names(district_state, district_geometries)
    district_options = sorted(name for parent, name in district_state
                              if parent.casefold() == "assam")
    if not district_options:
        raise ValueError("No Assam district names were returned by the live geography services.")
    return neighbor_candidates, district_state, district_geometries, district_options


def feature_name(feature):
    props = feature.get("properties") or {}
    for key in ("stname", "district", "shapeName", "name", "NAME_1", "NAME_2", "district", "state"):
        if props.get(key):
            return str(props[key]).strip()
    return ""


def normalized(value):
    value = str(value or "").casefold().replace("&", " and ")
    return " ".join(re.sub(r"[\W_]+", " ", value, flags=re.UNICODE).split())


def district_label_key(value):
    """Normalize bilingual/annotated live labels without using a stored alias list."""
    label = str(value or "").split("/", 1)[0]
    label = re.sub(r"\s*\([^)]*\)\s*$", "", label)
    return normalized(label)


# Explicit district-name equivalences requested for the live feeds. These affect
# name matching only; the returned source label/station remains visible to users.
DISTRICT_LABEL_ALIASES = {
    "kamrup metropolitan": {"kamrup metropolitan", "kamrup metro", "guwahati"},
    "kamrup metro": {"kamrup metropolitan", "kamrup metro", "guwahati"},
    "guwahati": {"kamrup metropolitan", "kamrup metro", "guwahati"},
    "karimganj": {"karimganj", "sribhumi", "sribhumi district"},
    "sribhumi": {"karimganj", "sribhumi", "sribhumi district"},
    "sribhumi district": {"karimganj", "sribhumi", "sribhumi district"},
    # IMD's own pages spell Mizoram's southernmost district both ways (Saiha / Siaha).
    "saiha": {"saiha", "siaha"},
    "siaha": {"saiha", "siaha"},
    "karbi anglong": {"karbi anglong", "karbi analog"},
    "karbi analog": {"karbi anglong", "karbi analog"},
}
# IMD's maps label Kamrup Metropolitan (Guwahati) just "Kamrup"; the other district is "Kamrup Rural". Treat "kamrup" as a weak alias for Metropolitan: used only when no stronger label exists.
WEAK_DISTRICT_ALIASES = {"kamrup"}
DISTRICT_LABEL_ALIASES.update({
    "kamrup metropolitan": {"kamrup metropolitan", "kamrup metro", "guwahati", "kamrup"},
    "kamrup metro": {"kamrup metropolitan", "kamrup metro", "guwahati", "kamrup"},
    "guwahati": {"kamrup metropolitan", "kamrup metro", "guwahati", "kamrup"},
})


def unique_district_label_match(target, labels, threshold=0.88):
    """Match exact or small spelling variants only when the live labels are unambiguous."""
    keyed = [(label, district_label_key(label)) for label in labels]
    keyed = [(label, key) for label, key in keyed if key]
    target_key = district_label_key(target)
    if not target_key:
        return None
    target_keys = DISTRICT_LABEL_ALIASES.get(target_key, {target_key})
    exact = [label for label, key in keyed if key in target_keys]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        # Several labels fit through aliases: prefer the district's own name, then drop weak
        # (shorter, ambiguous) aliases. Still ambiguous after that means no match.
        own = [label for label in exact if district_label_key(label) == target_key]
        if len(own) == 1:
            return own[0]
        strong = [label for label in exact if district_label_key(label) not in WEAK_DISTRICT_ALIASES]
        if len(strong) == 1:
            return strong[0]
    if exact:
        return None
    scored = sorted(
        ((max(SequenceMatcher(None, alias, key).ratio() for alias in target_keys), label)
         for label, key in keyed), reverse=True,
    )
    if not scored or scored[0][0] < threshold:
        return None
    if len(scored) > 1 and scored[0][0] - scored[1][0] < 0.04:
        return None
    return scored[0][1]


def source_date_is_today(value):
    raw = str(value or "").strip()
    from zoneinfo import ZoneInfo
    today = datetime.now(ZoneInfo("Asia/Kolkata")).date()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(raw[:10], fmt).date() == today
        except ValueError:
            continue
    return False


def source_date_is_latest_observation(value):
    """Accept today's or yesterday's dated daily observation as the latest published report."""
    raw = str(value or "").strip()
    from zoneinfo import ZoneInfo
    today = datetime.now(ZoneInfo("Asia/Kolkata")).date()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(raw[:10], fmt).date() in {today, today - timedelta(days=1)}
        except ValueError:
            continue
    return False


def source_date_is_current_daily_observation(value):
    """Daily 0830 IST reports remain current until that day's report is published."""
    raw = str(value or "").strip()
    from zoneinfo import ZoneInfo
    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            report_date = datetime.strptime(raw[:10], fmt).date()
            return report_date == now.date() or (
                report_date == now.date() - timedelta(days=1)
                and (now.hour, now.minute) < (8, 30)
            )
        except ValueError:
            continue
    return False


def live_imd_public_rainfall_records():
    """Parse IMD's public, no-key all-India district rainfall map for its current daily view."""
    url = "https://mausam.imd.gov.in/responsive/rainfallinformation.php"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    page = response.text
    # The IMD page includes the observation time and the word "of" in its
    # current heading; older page versions omitted both.
    period = re.search(
        r"Rainfall Recorded from(?:\s+\d{4}\s+hrs)?\s+(?:of\s+)?"
        r"(\d{2}-\d{2}-\d{4})\s+to(?:\s+\d{4}\s+hrs)?\s+(?:of\s+)?"
        r"(\d{2}-\d{2}-\d{4})",
        page, re.I,
    )
    if not period:
        raise RuntimeError("IMD's public district rainfall page did not show a report period.")
    if not source_date_is_current_daily_observation(period.group(2)):
        latest = datetime.strptime(period.group(2), "%d-%m-%Y").date().isoformat()
        raise RuntimeError(f"IMD's latest public district rainfall report ends {latest}, not today.")
    records = []
    # The IMD map embeds district features as JavaScript objects; balloonText is the
    # page's own observation text. Do not infer state from coordinates or a local list.
    for match in re.finditer(r"\{[^{}]*\}", page):
        raw = match.group(0)
        balloon_match = re.search(r'\"balloonText\"\s*:\s*\"((?:\\.|[^\"\\])*)\"', raw, re.S)
        if not balloon_match:
            continue
        try:
            balloon = json.loads('"' + balloon_match.group(1) + '"')
        except (ValueError, TypeError):
            balloon = html.unescape(balloon_match.group(1))
        text = html.unescape(re.sub(r"<br\s*/?>", " | ", balloon, flags=re.I))
        title_match = re.search(r'\"title\"\s*:\s*\"((?:\\.|[^\"\\])*)\"', raw, re.S)
        title = ""
        if title_match:
            try:
                title = json.loads('"' + title_match.group(1) + '"')
            except ValueError:
                title = title_match.group(1)
        district_field = re.search(r"\bDistrict\s*:\s*([^|<\r\n]+)", html.unescape(balloon), re.I)
        state_field = re.search(r"\bState\s*:\s*([^|<\r\n]+)", html.unescape(balloon), re.I)
        district_label = district_field.group(1).strip() if district_field else title.strip()
        date_match = re.search(r"\bDate\s*:\s*([^|<\r\n]+)", text, re.I)
        actual_match = re.search(r"\bActual\s*:\s*([-+]?\d+(?:\.\d+)?)\s*mm\b", text, re.I)
        if not district_label or not date_match or not actual_match:
            continue
        if not source_date_is_current_daily_observation(date_match.group(1).strip()):
            continue
        records.append({"district": district_label,
                        "state": state_field.group(1).strip() if state_field else None,
                        "value_mm": actual_match.group(1),
                        "date": date_match.group(1).strip(), "detail": text})
    if not records:
        raise RuntimeError("IMD's public rainfall page did not expose parseable current district observations.")
    return records


def live_imd_public_rainfall(state: str, district: str, records):
    matches = records
    state_matches = [row for row in matches if row.get("state")
                     and normalized(row["state"]) == normalized(state)]
    if state_matches:
        matches = state_matches
    match_label = unique_district_label_match(district, [row["district"] for row in matches])
    matches = [row for row in matches if row["district"] == match_label] if match_label else []
    if len(matches) != 1:
        raise RuntimeError("No unique exact district/state match on IMD's live rainfall page.")
    row = matches[0]
    # The page's district map may omit state identity. Accept only a globally unique,
    # exact district label; ambiguous labels are deliberately left not reported.
    matched_label = row["district"]
    result = {"value_mm": row["value_mm"], "date": row["date"],
              "source": "IMD public district rainfall page"}
    if district_label_key(matched_label) != district_label_key(district):
        result["matched_source_label"] = matched_label
    return result


@st.cache_data(ttl=12 * 60 * 60, show_spinner=False)
def live_imd_realtime_rainfall_grid(report_date):
    """Download IMD's dated 0.25-degree real-time rainfall grid in memory."""
    page_url = "https://www.imdpune.gov.in/cmpg/Realtimedata/Rainfall/Rain_Download.html"
    download_url = "https://www.imdpune.gov.in/cmpg/Realtimedata/Rainfall/rain.php"
    session = requests.Session()
    page = session.get(page_url, headers=HEADERS, timeout=20)
    page.raise_for_status()
    response = session.post(
        download_url,
        data={"rain": report_date.strftime("%d%m%Y")},
        headers={**HEADERS, "Referer": page_url},
        timeout=30,
    )
    response.raise_for_status()
    expected_bytes = 135 * 129 * 4
    if len(response.content) != expected_bytes:
        raise RuntimeError(
            f"IMD real-time grid for {report_date.isoformat()} was not published or had an unexpected size."
        )
    values = struct.unpack("<" + "f" * (135 * 129), response.content)
    if not any(math.isfinite(value) and value >= 0 for value in values):
        raise RuntimeError("IMD real-time grid contained no valid rainfall cells.")
    return values


def live_imd_grid_district_rainfall(district_geometry):
    """Calculate the area-weighted district mean from the freshest available IMD grid."""
    from zoneinfo import ZoneInfo

    today = datetime.now(ZoneInfo("Asia/Kolkata")).date()
    errors = []
    for report_date in (today, today - timedelta(days=1)):
        try:
            values = live_imd_realtime_rainfall_grid(report_date)
            domain = box(66.375, 6.375, 100.125, 38.875)
            if not domain.buffer(1e-9).covers(district_geometry):
                raise RuntimeError("The IMD grid does not cover the complete district boundary.")

            min_lon, min_lat, max_lon, max_lat = district_geometry.bounds
            first_x = max(0, math.floor((min_lon - 66.5) / 0.25) - 1)
            last_x = min(134, math.ceil((max_lon - 66.5) / 0.25) + 1)
            first_y = max(0, math.floor((min_lat - 6.5) / 0.25) - 1)
            last_y = min(128, math.ceil((max_lat - 6.5) / 0.25) + 1)
            weighted_sum = 0.0
            valid_area = 0.0
            domain_area = 0.0
            for y_index in range(first_y, last_y + 1):
                latitude = 6.5 + 0.25 * y_index
                for x_index in range(first_x, last_x + 1):
                    longitude = 66.5 + 0.25 * x_index
                    cell = box(longitude - 0.125, latitude - 0.125,
                               longitude + 0.125, latitude + 0.125)
                    overlap = district_geometry.intersection(cell)
                    if overlap.is_empty or overlap.area <= 0:
                        continue
                    area_weight = overlap.area * math.cos(math.radians(overlap.centroid.y))
                    domain_area += area_weight
                    value = values[y_index * 135 + x_index]
                    if math.isfinite(value) and value >= 0:
                        valid_area += area_weight
                        weighted_sum += value * area_weight

            coverage = valid_area / domain_area if domain_area else 0.0
            # Border districts can extend slightly past the grid's valid (land) cells; accept 90%+
            # coverage, and state the exact covered share in the note shown to operators.
            if coverage < 0.90:
                raise RuntimeError(
                    f"IMD grid has only {coverage * 100:.2f}% valid coverage inside the district boundary."
                )
            return {
                "value_mm": round(weighted_sum / valid_area, 2),
                "date": report_date.isoformat(),
                "source": "IMD real-time 0.25° rainfall grid (area-weighted district average)",
                "coverage_note": (f"Valid grid coverage: {coverage * 100:.1f}% of district boundary"
                                  if coverage >= 0.999999 else
                                  f"PARTIAL grid estimate: the grid covers {coverage * 100:.1f}% of the district boundary; "
                                  "the rest has no grid value."),
                "source_url": "https://www.imdpune.gov.in/cmpg/Realtimedata/Rainfall/Rain_Download.html",
            }
        except Exception as exc:
            errors.append(f"{report_date.isoformat()}: {exc}")
    raise RuntimeError("; ".join(errors))


def live_rmc_assam_today_report():
    """Fetch current observations from RMC Guwahati's public no-key HTML station table."""
    url = "https://mausam.imd.gov.in/imd_latest/contents/Todaysweather_mc.php?id=24"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    page = response.text
    date_match = re.search(r"\bDate\s*:\s*(\d{4}-\d{2}-\d{2})\b", page, re.I)
    if not date_match or not source_date_is_current_daily_observation(date_match.group(1)):
        raise RuntimeError("RMC Guwahati's public station report is not the current daily report.")
    from html.parser import HTMLParser

    class TableRows(HTMLParser):
        def __init__(self):
            super().__init__()
            self.rows, self.row, self.cell = [], None, None
        def handle_starttag(self, tag, attrs):
            if tag == "tr": self.row = []
            elif tag in ("td", "th") and self.row is not None: self.cell = []
        def handle_data(self, data):
            if self.cell is not None: self.cell.append(data)
        def handle_endtag(self, tag):
            if tag in ("td", "th") and self.cell is not None and self.row is not None:
                self.row.append(" ".join("".join(self.cell).split())); self.cell = None
            elif tag == "tr" and self.row is not None:
                if self.row: self.rows.append(self.row)
                self.row = None

    parser = TableRows()
    parser.feed(page)
    stations = {}
    for row in parser.rows:
        if len(row) < 8 or normalized(row[0]) in ("station", ""):
            continue
        # Official header order: Station, Max Temp, dep, Min Temp, dep, RH, RH, Rainfall.
        clean = lambda value: value.strip() if value.strip() not in ("--", "-") else None
        rainfall_text = clean(row[7])
        # RMC's station table uses the literal NIL to report no measured rain.
        # Treat only that explicit source value as 0; blanks and '--' stay missing.
        rainfall_value = 0.0 if (row[7] or "").strip().casefold() == "nil" else rainfall_text
        stations[normalized(row[0])] = {
            "station": row[0], "rainfall": rainfall_value, "date": date_match.group(1),
            "source": "RMC Guwahati today's weather report",
        }
    if not stations:
        raise RuntimeError("RMC Guwahati's public station table could not be parsed.")
    return {"date": date_match.group(1), "stations": stations}


def live_rmc_today_station_value(report, district):
    station_label = unique_district_label_match(
        district, [value.get("station", "") for value in report["stations"].values()], threshold=0.80,
    )
    row = next((value for value in report["stations"].values()
                if value.get("station") == station_label), None)
    if row is None:
        source_names = ", ".join(sorted(value.get("station", "") for value in report["stations"].values()))
        raise RuntimeError(
            f"RMC Guwahati has no exact current station-name match for {district}. "
            f"Live station labels returned: {source_names or 'none'}. No approximate district match was assumed."
        )
    result = dict(row)
    if district_label_key(station_label) != district_label_key(district):
        result["matched_source_label"] = station_label
        result["coverage_note"] = "Guwahati station reading mapped by district-name equivalence; it is not a district-wide aggregate."
    return result


def live_rmc_assam_station_observations():
    """Read current-day observed values from the official RMC Guwahati daily report."""
    url = "https://mausam.imd.gov.in/guwahati/mcdata/dwr.pdf"
    response = requests.get(url, headers=HEADERS, timeout=40)
    response.raise_for_status()
    if not response.content.startswith(b"%PDF"):
        raise RuntimeError("RMC Guwahati did not return its daily weather report PDF.")
    pdf = PdfReader(io.BytesIO(response.content))
    all_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    date_match = re.search(
        r"Observed Weather parameters for Assam recorded at 0830 hours IST of\s*(\d{1,2})-\s*([A-Za-z]+)-\s*(\d{4})",
        all_text, re.I,
    )
    if not date_match:
        raise RuntimeError("RMC daily report did not provide a recognizable observation date.")
    report_date = datetime.strptime(" ".join(date_match.groups()), "%d %B %Y").date()
    from zoneinfo import ZoneInfo
    if not source_date_is_current_daily_observation(report_date.isoformat()):
        raise RuntimeError("RMC Guwahati's daily station observations are not the current daily report.")
    table = pdf.pages[-1].extract_text(extraction_mode="layout") or ""
    station_rows = {}
    numeric_pattern = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)$")
    for line in table.splitlines():
        match = re.match(r"^\s*(.*?)\s{2,}(.+?)\s*$", line)
        if not match:
            continue
        station = match.group(1).strip()
        fields = match.group(2).split()
        if not station or len(fields) < 9:
            continue
        if not numeric_pattern.fullmatch(fields[8]):
            continue
        station_rows[normalized(station)] = {
            "station": station,
            "rain_mm": float(fields[8]),
        }
    return {"date": report_date.isoformat(), "stations": station_rows}


def live_rmc_assam_station_value(report, district):
    station_label = unique_district_label_match(
        district, [row.get("station", "") for row in report["stations"].values()], threshold=0.80,
    )
    row = next((value for value in report["stations"].values()
                if value.get("station") == station_label), None)
    if row is None:
        names = ", ".join(sorted(row.get("station", "") for row in report["stations"].values()))
        raise RuntimeError(
            f"RMC Guwahati has no observation from a station named exactly for {district}. "
            f"Live station labels returned: {names or 'none'}. No approximate district match was assumed."
        )
    result = {**row, "date": report["date"], "source": "RMC Guwahati daily station report"}
    if district_label_key(station_label) != district_label_key(district):
        result["matched_source_label"] = station_label
        result["coverage_note"] = "Guwahati station reading mapped by district-name equivalence; it is not a district-wide aggregate."
    return result


NRSC_LIGHTNING_GEOJSON_URL = (
    "https://bhuvan-app1.nrsc.gov.in/lightning/usrtasks/heatwave/get/geojson.php"
)


def live_nrsc_lightning_hourly_records():
    """Fetch the latest six completed hourly point datasets from NRSC-ISRO Bhuvan."""
    from datetime import timezone, timedelta
    from concurrent.futures import ThreadPoolExecutor

    now_utc = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    windows = [now_utc - timedelta(hours=offset) for offset in range(1, 7)]

    def fetch_hour(hour_start):
        response = requests.get(
            NRSC_LIGHTNING_GEOJSON_URL, headers=HEADERS,
            params={"date": hour_start.date().isoformat(), "timestamp": f"{hour_start.hour:02d}"},
            timeout=(5, 20),
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("type") != "FeatureCollection" or not isinstance(payload.get("features"), list):
            raise RuntimeError("NRSC lightning feed returned an unexpected GeoJSON response.")
        return hour_start, payload["features"]

    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(fetch_hour, windows))
    records = []
    for hour_start, features in results:
        for feature in features:
            geometry = feature.get("geometry") or {}
            if geometry.get("type") != "Point":
                continue
            coordinates = geometry.get("coordinates") or []
            if len(coordinates) < 2:
                continue
            longitude, latitude = coordinates[:2]
            if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
                continue
            properties = feature.get("properties") or {}
            records.append({
                "latitude": latitude, "longitude": longitude,
                "hour_utc": hour_start.strftime("%Y-%m-%d %H:00 UTC"),
                "source_time": properties.get("time"),
                "feed_id": properties.get("gid"),
                "current": properties.get("current"),
                "properties": properties,
            })
    return {"records": records, "window_start": windows[-1], "window_end": windows[0] + timedelta(hours=1)}


def live_nrsc_lightning_coordinates(feed, district_geometry):
    """Return only live NRSC strike points contained by the exact live district polygon."""
    from shapely.geometry import Point
    matches = []
    for record in feed["records"]:
        point = Point(record["longitude"], record["latitude"])
        if district_geometry.covers(point):
            matches.append({
                "latitude": record["latitude"], "longitude": record["longitude"],
                "hour_utc": record["hour_utc"],
                "source_time": record.get("source_time"),
                "feed_id": record.get("feed_id"),
                "current": record.get("current"),
            })
    return {
        "status": "OK", "coordinates": matches,
        "window_start": feed["window_start"].strftime("%Y-%m-%d %H:%M UTC"),
        "window_end": feed["window_end"].strftime("%Y-%m-%d %H:%M UTC"),
        "source": "NRSC–ISRO Bhuvan hourly lightning data",
    }


def live_rmc_assam_warning_features():
    """Read RMC Guwahati's current-day district warning entries from its official page."""
    response = requests.get(
        "https://mausam.imd.gov.in/imd_latest/contents/districtwise-warning_mc.php",
        params={"id": "24", "day": "Day_1"}, headers=HEADERS, timeout=30,
    )
    response.raise_for_status()
    pattern = re.compile(
        r'\{\s*"title"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"\s*,\s*'
        r'"id"\s*:\s*"([^"\\]*)"\s*,\s*"color"\s*:\s*"([^"\\]*)"\s*,\s*'
        r'"balloonText"\s*:\s*"((?:\\.|[^"\\])*)"\s*\}', re.S,
    )
    entries = []
    for match in pattern.finditer(response.text):
        try:
            entries.append({
                "District": json.loads('"' + match.group(1) + '"'),
                "Obj_id": match.group(2),
                "Color": match.group(3),
                "Text": html.unescape(json.loads('"' + match.group(4) + '"')),
            })
        except (ValueError, json.JSONDecodeError):
            continue
    if not entries:
        raise RuntimeError("RMC Guwahati's live warning page did not contain district warning records.")
    return entries


def live_rmc_assam_district_warning(entries, district):
    matched_name = unique_district_label_match(
        district, [entry.get("District", "") for entry in entries], threshold=0.84,
    )
    matches = [entry for entry in entries if entry.get("District") == matched_name] if matched_name else []
    if len(matches) != 1:
        return {"status": "UNAVAILABLE", "items": [],
                "reason": "RMC Guwahati did not return one unambiguous record for this district."}
    entry = matches[0]
    updated = re.search(r"Updated on:\s*(\d{4}-\d{2}-\d{2})", entry.get("Text", ""), re.I)
    if not updated or not source_date_is_today(updated.group(1)):
        return {"status": "UNAVAILABLE", "items": [],
                "reason": "RMC Guwahati's matching district warning is not dated today."}
    plain_text = " ".join(re.sub(r"<[^>]*>", " ", entry.get("Text", "")).split())
    lowered = plain_text.casefold()
    if "no warning" in lowered:
        return {"status": "OK", "items": [], "no_warning_days": [1],
                "issue_date": updated.group(1), "source": "RMC Guwahati"}
    hazards = []
    if any(word in lowered for word in ("heavy rain", "very heavy rain", "extremely heavy rain")):
        hazards.append("Heavy rain")
    if "thunderstorm" in lowered or "lightning" in lowered:
        hazards.append("Thunderstorm / lightning")
    if any(word in lowered for word in ("cyclone", "cyclonic", "depression")):
        hazards.append("Cyclone-related wording in RMC warning")
    items = ([{"day": 1, "date": updated.group(1), "hazards": hazards,
               "text": plain_text, "color": entry.get("Color")}] if hazards else [])
    return {"status": "OK", "items": items, "no_warning_days": [],
            "issue_date": updated.group(1), "source": "RMC Guwahati"}


RMC_DAILY_REPORT_URL = "https://mausam.imd.gov.in/guwahati/mcdata/dwr.pdf"
RMC_NOWCAST_URL = "https://mausam.imd.gov.in/imd_latest/contents/districtwisewarnings_mc.php?id=24"

IMD_WARNING_MAP_URL = "https://mausam.imd.gov.in/responsive/districtWiseWarningGIS.php"
IMD_NOWCAST_MAP_URL = "https://mausam.imd.gov.in/responsive/districtWiseNowcastGIS.php"
IMD_DISTRICT_WARNING_LAYER = "imd:district_warnings_india"
IMD_DISTRICT_NOWCAST_LAYER = "imd:NowcastWarningDistrict"


def live_imd_district_feed(layer):
    """Fetch the public district feature layer used by IMD's own warning/nowcast map."""
    if layer not in {IMD_DISTRICT_WARNING_LAYER, IMD_DISTRICT_NOWCAST_LAYER}:
        raise ValueError("Unsupported IMD district warning layer.")
    response = requests.get(
        "https://reactjs.imd.gov.in/geoserver/ows", headers=HEADERS,
        params={"service": "WFS", "version": "1.1.0", "request": "GetFeature",
                "typename": layer, "srsname": "EPSG:4326", "outputFormat": "application/json"},
        timeout=(5, 35),
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("type") != "FeatureCollection" or not isinstance(payload.get("features"), list):
        raise RuntimeError("IMD district feed returned an unexpected feature collection.")
    if not payload["features"]:
        raise RuntimeError("IMD district feed returned no district records.")
    return payload["features"]


def _district_feed_match(features, state, district, district_geometry, name_fields, state_fields=()):
    """Resolve a live feed record by state, district label, and spatial overlap."""
    from shapely.geometry import shape
    target_key = district_label_key(district)
    scored = []
    named = []
    for feature in features:
        props = feature.get("properties") or {}
        row_state = next((str(props.get(key) or "").strip() for key in state_fields
                          if props.get(key)), "")
        if row_state and normalized(row_state) != normalized(state):
            continue
        name = next((str(props.get(key) or "").strip() for key in name_fields
                     if props.get(key)), "")
        if name:
            named.append((feature, name))
        similarity = SequenceMatcher(None, target_key, district_label_key(name)).ratio()
        if similarity < 0.80:
            continue
        geometry_data = feature.get("geometry")
        if not name or not geometry_data:
            continue
        try:
            candidate_geometry = shape(geometry_data)
            district_bounds = district_geometry.bounds
            candidate_bounds = candidate_geometry.bounds
            if (candidate_bounds[2] < district_bounds[0] or candidate_bounds[0] > district_bounds[2]
                    or candidate_bounds[3] < district_bounds[1] or candidate_bounds[1] > district_bounds[3]):
                continue
            denominator = district_geometry.area or 1
            overlap = district_geometry.intersection(candidate_geometry).area / denominator
        except Exception:
            continue
        if overlap < 0.5:
            continue
        scored.append((overlap, similarity, feature))
    exact = [row for row in scored if row[1] == 1]
    ranked = sorted(exact or [row for row in scored if row[1] >= 0.80],
                    key=lambda row: (row[0], row[1]), reverse=True)
    if not ranked:
        spatial = []
        for feature, _name in named:
            geometry_data = feature.get("geometry")
            if not geometry_data:
                continue
            try:
                candidate_geometry = shape(geometry_data)
                district_bounds = district_geometry.bounds
                candidate_bounds = candidate_geometry.bounds
                if (candidate_bounds[2] < district_bounds[0] or candidate_bounds[0] > district_bounds[2]
                        or candidate_bounds[3] < district_bounds[1] or candidate_bounds[1] > district_bounds[3]):
                    continue
                intersection_area = district_geometry.intersection(candidate_geometry).area
                coverage = intersection_area / (district_geometry.area or 1)
                iou = intersection_area / (
                    district_geometry.area + candidate_geometry.area - intersection_area or 1
                )
                spatial.append((iou, coverage, feature))
            except Exception:
                continue
        spatial.sort(key=lambda row: (row[0], row[1]), reverse=True)
        # Legacy IMD district labels (e.g. East Midnapore/Purba Medinipur) are
        # accepted only when the live source polygon is an almost exact match.
        if (spatial and spatial[0][0] >= 0.90 and spatial[0][1] >= 0.95
                and (len(spatial) == 1 or spatial[0][0] - spatial[1][0] >= 0.50)):
            return spatial[0][2]
        # Some IMD warning polygons do not spatially overlap the current IMD
        # administrative polygon revision. Permit a name-only fallback only
        # when the official feed label resolves uniquely within this feed/state.
        matched_name = unique_district_label_match(district, [name for _feature, name in named], threshold=0.80)
        exact_named = [(feature, name) for feature, name in named
                       if matched_name and district_label_key(name) == district_label_key(matched_name)]
        return exact_named[0][0] if len(exact_named) == 1 else None
    if len(ranked) > 1 and (ranked[0][0], ranked[0][1]) == (ranked[1][0], ranked[1][1]):
        return None
    return ranked[0][2]


IMD_WARNING_CATEGORIES = {
    "2": "Heavy rain", "3": "Heavy snow", "4": "Thunderstorms and lightning",
    "5": "Hailstorm", "6": "Dust storm", "7": "Dust raising winds",
    "8": "Strong surface winds", "9": "Heat wave", "10": "Hot day",
    "11": "Warm night", "12": "Cold wave", "13": "Cold day",
    "14": "Ground frost", "15": "Fog", "16": "Very heavy rain",
    "17": "Extremely heavy rain",
}


def live_imd_district_warning(features, state, district, district_geometry):
    feature = _district_feed_match(features, state, district, district_geometry,
                                   ("District", "State_District"))
    if feature is None:
        return {"status": "UNAVAILABLE", "items": [],
                "reason": "No unambiguous matching district record in IMD's live warning map."}
    props = feature.get("properties") or {}
    report_date = props.get("Date")
    if not source_date_is_current_daily_observation(report_date):
        return {"status": "UNAVAILABLE", "items": [],
                "reason": "IMD's district warning record is outside its current daily validity."}
    issue_date = _forecast_date_key(report_date)
    if not issue_date:
        return {"status": "UNAVAILABLE", "items": [],
                "reason": "IMD's district warning record has no readable issue date."}
    # Day 1 is the record's own issue date (not the server clock), so a report dated
    # yesterday is never shifted forward by a day.
    base_date = datetime.strptime(issue_date, "%Y-%m-%d").date()
    items, no_warning_days = [], []
    for day in range(1, 6):
        raw_codes = str(props.get(f"Day_{day}") or "").strip()
        if not raw_codes:
            continue
        codes = [code.strip() for code in raw_codes.split(",") if code.strip()]
        if not codes:
            continue
        if all(code == "1" for code in codes):
            no_warning_days.append(day)
            continue
        hazards = [IMD_WARNING_CATEGORIES[code] for code in codes if code in IMD_WARNING_CATEGORIES]
        extra = str(props.get(f"Day{day}_text") or "").strip()
        if hazards or extra:
            valid_date = (base_date + timedelta(days=day - 1)).isoformat()
            items.append({"day": day, "date": valid_date, "hazards": hazards,
                          "text": extra, "color": props.get(f"Day{day}_Color")})
    if not items and not no_warning_days:
        return {"status": "UNAVAILABLE", "items": [],
                "reason": "IMD's matching district warning record had no explicit warning or no-warning entry for any day."}
    missing_days = [day for day in range(1, 6)
                    if day not in no_warning_days and day not in {item["day"] for item in items}]
    result = {"status": "OK", "items": items, "no_warning_days": no_warning_days,
              "issue_date": issue_date, "source": "IMD district warning map"}
    if missing_days:
        result["missing_days"] = missing_days  # days the feed left blank: not an all-clear
    return result


IMD_NOWCAST_CATEGORIES = {
    2: "Light rain", 3: "Light snow", 4: "Light thunderstorm",
    5: "Slight dust storm", 6: "Low lightning probability", 7: "Moderate rain",
    8: "Moderate snow", 9: "Moderate thunderstorm", 10: "Moderate dust storm",
    11: "Moderate lightning probability", 12: "Heavy rain", 13: "Heavy snow",
    14: "Severe thunderstorm", 15: "Very severe thunderstorm", 17: "Thunderstorm with hail",
    18: "Severe dust storm", 19: "High lightning probability",
}


def live_imd_district_nowcast(features, state, district, district_geometry):
    feature = _district_feed_match(features, state, district, district_geometry,
                                   ("State_District", "District"), ("State",))
    if feature is None:
        return {"status": "UNAVAILABLE", "reason": "No unambiguous matching district record in IMD's live nowcast map."}
    props = feature.get("properties") or {}
    issue_date_raw = str(props.get("Date") or "").strip()
    issue_time = str(props.get("toi") or "").strip().zfill(4)
    valid_time = str(props.get("vupto") or "").strip().zfill(4)
    try:
        from zoneinfo import ZoneInfo
        issue_date = datetime.strptime(issue_date_raw[:10], "%Y-%m-%d").date()
        issued_at = datetime.combine(issue_date, datetime.strptime(issue_time, "%H%M").time(),
                                     tzinfo=ZoneInfo("Asia/Kolkata"))
        valid_until = datetime.combine(issue_date, datetime.strptime(valid_time, "%H%M").time(),
                                       tzinfo=ZoneInfo("Asia/Kolkata"))
        if valid_until <= issued_at:
            valid_until += timedelta(days=1)
        now = datetime.now(ZoneInfo("Asia/Kolkata"))
    except (ValueError, TypeError):
        return {"status": "UNAVAILABLE", "reason": "IMD nowcast did not provide valid issue and expiry times."}
    if now < issued_at - timedelta(minutes=5):
        return {"status": "UNAVAILABLE", "reason": "IMD's matching nowcast entry has an issue time in the future."}
    # An entry past its stated validity is still returned, clearly marked EXPIRED with its own
    # issue date/time and validity, so operators see what IMD last published (never as current).
    expired = now > valid_until
    message = str(props.get("message") or "").strip()
    active = []
    for number, label in IMD_NOWCAST_CATEGORIES.items():
        if props.get(f"cat{number}") not in (None, "", 0, "0", False):
            active.append(label)
    if message:
        active.append(message)
    no_warning = (not active and str(props.get("cat1") or "") in {"1", "1.0"})
    if not no_warning and not active:
        return {"status": "UNAVAILABLE", "reason": "IMD nowcast row had no explicit warning or no-warning code."}
    result = {"status": "EXPIRED" if expired else "OK",
              "district": props.get("State_District") or props.get("District"),
              "message": "; ".join(active), "no_warning": no_warning,
              "issue_date": issue_date.isoformat(), "issue_time": issue_time,
              "valid_until": valid_time, "valid_until_at": valid_until.isoformat(timespec="minutes"),
              "source": "IMD district nowcast map"}
    if expired:
        result["reason"] = (f"Last IMD entry expired {valid_until.strftime('%d-%m-%Y %I:%M %p')} IST; "
                            "no newer entry has been published yet.")
    return result


def compute_nowcast(state, district, geometry, features, feed_error, rmc_loader):
    """Resolve one district's nowcast: IMD map first, RMC Guwahati page as the Assam fallback."""
    if features is not None:
        nowcast = live_imd_district_nowcast(features, state, district, geometry)
    else:
        nowcast = {"status": "UNAVAILABLE", "reason": feed_error}
    if nowcast.get("status") != "OK" and normalized(state) == "assam":
        imd_reason = feed_error or nowcast.get("reason")
        try:
            rmc = live_rmc_assam_nowcast(rmc_loader(), district)
            if rmc.get("status") == "OK":
                return rmc
            rmc_reason = rmc.get("reason")
        except Exception as exc:
            rmc_reason = str(exc)
        nowcast = dict(nowcast)
        nowcast["reason"] = f"IMD district feed: {imd_reason}; RMC Guwahati: {rmc_reason}"
    return nowcast


def refresh_live_nowcasts(places, district_geometries):
    """Re-read only the nowcast sources and update stored results; returns names whose entry changed."""
    from zoneinfo import ZoneInfo
    results = st.session_state.get("live_results") or []
    features, feed_error = None, None
    try:
        features = live_imd_district_feed(IMD_DISTRICT_NOWCAST_LAYER)
    except Exception as exc:
        feed_error = str(exc)
    rmc_cache = {}

    def rmc_loader():
        if "records" not in rmc_cache and "error" not in rmc_cache:
            try:
                rmc_cache["records"] = live_rmc_assam_nowcast_records()
            except Exception as exc:
                rmc_cache["error"] = str(exc)
        if "error" in rmc_cache:
            raise RuntimeError(rmc_cache["error"])
        return rmc_cache["records"]

    def signature(entry):
        return (entry.get("status"), entry.get("issue_date"), entry.get("issue_time"),
                entry.get("valid_until"), entry.get("message"), entry.get("no_warning"))

    changed = []
    for item in results:
        if not isinstance(item, dict) or item.get("error"):
            continue
        geometry = next((g for (s, d), g in district_geometries.items()
                         if normalized(s) == normalized(item["state"])
                         and normalized(d) == normalized(item["district"])), None)
        if geometry is None:
            continue
        new_nowcast = compute_nowcast(item["state"], item["district"], geometry,
                                      features, feed_error, rmc_loader)
        previous_nowcast = item.get("nowcast") or {}
        checked_at = datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(timespec="seconds")
        if new_nowcast.get("status") != "OK" and previous_nowcast.get("status") in {"OK", "EXPIRED", "STALE"}:
            new_nowcast = dict(previous_nowcast)
            new_nowcast["last_checked_at"] = checked_at
            new_nowcast["recheck_error"] = (
                new_nowcast.get("reason")
                or feed_error
                or "No current nowcast could be verified from IMD or the Assam fallback."
            )
            valid_until_at = new_nowcast.get("valid_until_at")
            try:
                valid_until = datetime.fromisoformat(str(valid_until_at))
                if valid_until.tzinfo is None:
                    valid_until = valid_until.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
            except (ValueError, TypeError):
                valid_until = None
            if previous_nowcast.get("status") == "EXPIRED" or (
                valid_until and datetime.now(ZoneInfo("Asia/Kolkata")) > valid_until
            ):
                new_nowcast["status"] = "EXPIRED"
            else:
                new_nowcast["status"] = "STALE"
        elif new_nowcast.get("status") in {"OK", "EXPIRED"}:
            new_nowcast["last_verified_at"] = checked_at
            new_nowcast["last_checked_at"] = checked_at
        if signature(new_nowcast) != signature(item.get("nowcast") or {}):
            changed.append(item["district"])
        item["nowcast"] = new_nowcast
    st.session_state.nowcast_checked_at = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d-%m-%Y %I:%M %p IST")
    return changed


def live_rmc_assam_nowcast_records():
    """Scrape current district nowcast entries, including explicit No Warning and validity times."""
    response = requests.get(RMC_NOWCAST_URL, headers=HEADERS, timeout=(5, 25))
    response.raise_for_status()
    records = []
    for match in re.finditer(r"\{[^{}]*\"title\"\s*:\s*\"[^\"]*\"[^{}]*\}", response.text, re.S):
        try:
            entry = json.loads(match.group(0))
        except (ValueError, TypeError):
            continue
        name = entry.get("title")
        raw = entry.get("balloonText") or entry.get("info")
        if not name or not raw:
            continue
        plain = " ".join(html.unescape(re.sub(r"<[^>]*>", " ", raw)).split())
        issued = re.search(r"Time of issue:\s*(\d{4}-\d{2}-\d{2})\s*(\d{3,4})\s*Hrs", plain, re.I)
        valid = re.search(r"Valid upto:\s*(\d{3,4})\s*Hrs", plain, re.I)
        records.append({
            "district": name, "message": plain, "color": entry.get("color"),
            "no_warning": bool(re.search(r"\bNo Warning\b", plain, re.I)),
            "issue_date": issued.group(1) if issued else None,
            "issue_time": issued.group(2) if issued else None,
            "valid_until": valid.group(1) if valid else None,
            "source": "RMC Guwahati district-wise nowcast",
        })
    if not records:
        raise RuntimeError("RMC Guwahati's live district nowcast page returned no parseable district records.")
    return records


def live_rmc_assam_nowcast(records, district):
    matched_name = unique_district_label_match(
        district, [row.get("district", "") for row in records], threshold=0.84,
    )
    matches = [row for row in records if row.get("district") == matched_name] if matched_name else []
    if len(matches) != 1:
        return {"status": "UNAVAILABLE", "reason":
                "RMC Guwahati did not return one exact, unambiguous nowcast entry for this district."}
    row = matches[0]
    if row.get("issue_date") and not source_date_is_today(row["issue_date"]):
        return {"status": "UNAVAILABLE", "reason": "RMC Guwahati's matching nowcast entry is not dated today."}
    return {"status": "OK", **row}


def live_rmc_assam_forecast_report():
    """Read the live RMC PDF's Assam district forecast and seven-day Guwahati forecast sections."""
    response = requests.get(RMC_DAILY_REPORT_URL, headers=HEADERS, timeout=(5, 30))
    response.raise_for_status()
    if not response.content.startswith(b"%PDF"):
        raise RuntimeError("RMC Guwahati did not return its daily weather report PDF.")
    pdf = PdfReader(io.BytesIO(response.content))
    text = "\n".join(page.extract_text(extraction_mode="layout") or "" for page in pdf.pages)
    date_match = re.search(
        r"Observed Weather parameters for Assam recorded at 0830 hours IST of\s*(\d{1,2})-\s*([A-Za-z]+)-\s*(\d{4})",
        text, re.I,
    )
    if not date_match:
        raise RuntimeError("RMC daily report did not provide a recognizable observation date.")
    report_date = datetime.strptime(" ".join(date_match.groups()), "%d %B %Y").date()
    from zoneinfo import ZoneInfo
    if report_date != datetime.now(ZoneInfo("Asia/Kolkata")).date():
        raise RuntimeError(f"RMC daily report is dated {report_date.isoformat()}, not today.")

    def extract_days(section, limit):
        starts = list(re.finditer(
            r"(?ims)^\s*Day\s*(\d+)\s*\(Valid\s+upto\s+.*?\)", section
        ))
        output = []
        for index, start in enumerate(starts):
            day = int(start.group(1))
            if day > limit:
                continue
            end = starts[index + 1].start() if index + 1 < len(starts) else len(section)
            block = " ".join(section[start.start():end].split())
            warning = "No Warning" if re.search(r"\bNo Warning\b", block, re.I) else None
            output.append({"day": day, "official_text": block, "warning": warning,
                           "source": "RMC Guwahati daily weather report PDF"})
        return output

    district_heading = re.search(r"WEATHER FORECAST AND WARNING FOR DISTRICTS OF ASSAM", text, re.I)
    local_heading = re.search(r"Local forecast for Guwahati\s*&\s*neighbourhood", text, re.I)
    if not district_heading or not local_heading or local_heading.start() <= district_heading.start():
        raise RuntimeError("RMC daily report did not contain its expected district and Guwahati forecast sections.")
    district_days = extract_days(text[district_heading.end():local_heading.start()], 5)
    local_end = date_match.start()
    guwahati_days = extract_days(text[local_heading.end():local_end], 7)
    return {"date": report_date.isoformat(), "district_days": district_days,
            "guwahati_days": guwahati_days, "source": RMC_DAILY_REPORT_URL}


IMD_DISTRICT_RAIN_FORECAST_URL = "https://mausam.imd.gov.in/responsive/rainfallinformation/district_rain.php"
IMD_DISTRICT_RAIN_FORECAST_PAGE = "https://mausam.imd.gov.in/responsive/5d_statewisedistricts_rf_forecast.php"

# Current district products linked from the relevant IMD Meteorological Centre
# sites. West Bengal needs separate North and South Bengal reports.
MC_DISTRICT_FORECAST_PDFS = {
    "assam": [("https://mausam.imd.gov.in/guwahati/mcdata/distlevel.pdf", "RMC Guwahati")],
    "arunachal pradesh": [("https://mausam.imd.gov.in/itanagar/mcdata/AP_forecast.pdf", "IMD Met Centre Itanagar")],
    "meghalaya": [("https://mausam.imd.gov.in/shillong/mcdata/forecast.pdf", "IMD Met Centre Shillong")],
    "mizoram": [("https://mausam.imd.gov.in/aizawl/mcdata/AP_forecast.pdf", "IMD Met Centre Aizawl")],
    "manipur": [("https://mausam.imd.gov.in/imphal/mcdata/imp_forecast.pdf", "IMD Met Centre Imphal")],
    "nagaland": [("https://mausam.imd.gov.in/kohima/mcdata/NGL_Forecast.pdf", "IMD Met Centre Kohima")],
    "tripura": [("https://mausam.imd.gov.in/agartala/mcdata/District%20Forecast.pdf", "IMD Met Centre Agartala")],
    "west bengal": [
        ("https://mausam.imd.gov.in/kolkata/mcdata/north_bengal.pdf", "RMC Kolkata · North Bengal"),
        ("https://mausam.imd.gov.in/kolkata/mcdata/south_bengal.pdf", "RMC Kolkata · South Bengal"),
    ],
}


def _imd_forecast_text(value):
    return html.unescape(re.sub(r"<[^>]+>", " ", str(value or ""))).replace("\xa0", " ").strip()


def _is_current_or_future_forecast_date(value):
    from zoneinfo import ZoneInfo
    raw = re.sub(r"\b(\d{1,2})(st|nd|rd|th)\b", r"\1", str(value or "").strip(), flags=re.I)
    raw = re.sub(r"^(date|forecast date)\s*:\s*", "", raw, flags=re.I)
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d-%b-%Y",
                "%d-%B-%Y", "%d %b %Y", "%d %B %Y", "%d %b, %Y", "%d %B, %Y",
                "%d-%b", "%d %b"):
        try:
            parsed = datetime.strptime(raw[:20].strip(), fmt)
            if fmt in ("%d-%b", "%d %b"):
                parsed = parsed.replace(year=datetime.now(ZoneInfo("Asia/Kolkata")).year)
            forecast_date = parsed.date()
            now = datetime.now(ZoneInfo("Asia/Kolkata"))
            if forecast_date >= now.date():
                return True
            # IMD's standard district forecast day runs through 0830 IST of
            # the following date. Keep yesterday's Day 1 until that validity
            # window closes after midnight.
            return (forecast_date == now.date() - timedelta(days=1)
                    and now.time() < datetime.strptime("08:30", "%H:%M").time())
        except ValueError:
            continue
    return False


def _forecast_date_key(value):
    """Normalize an official source date for exact-date joins; never align by row position."""
    raw = re.sub(r"\b(\d{1,2})(st|nd|rd|th)\b", r"\1", str(value or "").strip(), flags=re.I)
    raw = re.sub(r"^(date|forecast date)\s*:\s*", "", raw, flags=re.I)
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d-%b-%Y", "%d-%B-%Y",
                "%d %b %Y", "%d %B %Y", "%d %b, %Y", "%d %B, %Y", "%d-%b", "%d %b"):
        try:
            parsed = datetime.strptime(raw[:20].strip(), fmt)
            if fmt in ("%d-%b", "%d %b"):
                from zoneinfo import ZoneInfo
                parsed = parsed.replace(year=datetime.now(ZoneInfo("Asia/Kolkata")).year)
            return parsed.date().isoformat()
        except ValueError:
            continue
    return None


def live_imd_district_rain_forecast(state_value, day_index):
    """Scrape one day of district rainfall categories from IMD's public live map."""
    response = requests.get(
        IMD_DISTRICT_RAIN_FORECAST_URL, headers=HEADERS,
        params={"id": state_value, "day": f"Day_{day_index}"}, timeout=(5, 20),
    )
    response.raise_for_status()
    records = {}
    for match in re.finditer(r"\{[^{}]*\}", response.text):
        raw = match.group(0)
        title_match = re.search(r'"title"\s*:\s*"((?:\\.|[^"\\])*)"', raw, re.S)
        balloon_match = re.search(r'"balloonText"\s*:\s*"((?:\\.|[^"\\])*)"', raw, re.S)
        if not title_match or not balloon_match:
            continue
        try:
            title = json.loads('"' + title_match.group(1) + '"')
            balloon = json.loads('"' + balloon_match.group(1) + '"')
        except (ValueError, TypeError):
            continue
        parts = [part.strip() for part in re.split(r"</?br\s*/?>", balloon, flags=re.I)
                 if part.strip()]
        if len(parts) < 3:
            continue
        source_date = _imd_forecast_text(parts[-1])
        if not _is_current_or_future_forecast_date(source_date):
            continue
        records[district_label_key(title)] = {
            "district": title,
            "date": source_date,
            "rainfall": _imd_forecast_text(parts[1]),
            "coverage": _imd_forecast_text(parts[2]) if len(parts) > 3 else "",
            "source": "IMD five-day district rainfall forecast",
        }
    if not records:
        raise RuntimeError("IMD's public rainfall forecast page returned no district records.")
    return records


def _imd_rainfall_map_state_labels(page):
    """Read the live state labels used by IMD's interactive rainfall map."""
    area_start = re.search(r"areas\s*:\s*\[", page, re.I)
    if not area_start:
        raise RuntimeError("IMD rainfall page did not expose its live map state list.")
    area_end = page.find("]", area_start.end())
    areas = page[area_start.end():area_end if area_end >= 0 else None]
    labels = []
    for match in re.finditer(r"\{([^{}]+)\}", areas, re.S):
        item = match.group(1)
        # IMD currently quotes JavaScript object keys ("ajaxUrl"). Accept both
        # quoted and unquoted keys so the live state list is not discarded.
        if not re.search(r"[\"']?ajaxUrl[\"']?\s*:\s*[\"'](?:rainfallinformation/)?district_rain\.php[\"']", item, re.I):
            continue
        label = re.search(r"[\"']label[\"']\s*:\s*[\"']([^\"']+)[\"']", item, re.I)
        state_id = re.search(r"[\"']id[\"']\s*:\s*[\"']([^\"']+)[\"']", item, re.I)
        if label and state_id:
            value = html.unescape(label.group(1)).strip()
            labels.append((state_id.group(1).strip(), value))
    if not labels:
        raise RuntimeError("IMD rainfall map did not publish any district-feed state labels.")
    return labels


OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def live_open_meteo_temperature_forecast(district_geometry):
    """Fetch a live model forecast at a point derived from the live district boundary."""
    point = district_geometry.representative_point()
    response = requests.get(
        OPEN_METEO_FORECAST_URL, headers=HEADERS,
        params={
            "latitude": point.y, "longitude": point.x,
            "daily": "temperature_2m_max,temperature_2m_min",
            "forecast_days": 5, "timezone": "Asia/Kolkata",
        }, timeout=(5, 20),
    )
    response.raise_for_status()
    payload = response.json()
    daily = payload.get("daily") or {}
    dates = daily.get("time") or []
    maxima = daily.get("temperature_2m_max") or []
    minima = daily.get("temperature_2m_min") or []
    if not dates or len(dates) != len(maxima) or len(dates) != len(minima):
        raise RuntimeError("Open-Meteo returned no complete dated maximum/minimum forecast.")
    model_lat = payload.get("latitude")
    model_lon = payload.get("longitude")
    if model_lat is None or model_lon is None:
        raise RuntimeError("Open-Meteo did not identify the forecast grid coordinates.")
    source = "Open-Meteo live model · district reference point"
    return [{
        "date": date, "maximum_c": maximum, "minimum_c": minimum,
        "source": source, "source_url": "https://open-meteo.com/",
        "reference_latitude": point.y, "reference_longitude": point.x,
        "grid_latitude": model_lat, "grid_longitude": model_lon,
    } for date, maximum, minimum in zip(dates[:5], maxima[:5], minima[:5])
        if maximum is not None and minimum is not None]


def live_met_centre_district_forecast(state, district, pdf_content=None, source_config=None):
    """Parse a current district row from a live IMD/RMC Met Centre PDF table."""
    configured = source_config or MC_DISTRICT_FORECAST_PDFS.get(normalized(state))
    if isinstance(configured, list):
        configured = configured[0] if configured else None
    if not configured:
        raise RuntimeError("No district forecast PDF is connected for this Meteorological Centre.")
    url, centre = configured
    if pdf_content is None:
        response = requests.get(url, headers=HEADERS, timeout=(5, 30))
        response.raise_for_status()
        pdf_content = response.content
    if not pdf_content.startswith(b"%PDF"):
        raise RuntimeError(f"{centre} did not return its district forecast PDF.")

    pdf = PdfReader(io.BytesIO(pdf_content))
    text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    date_pattern = re.compile(
        r"\b\d{1,2}(?:[-/. ]+[A-Za-z]{3,9}|[-/. ]+\d{1,2})[-/. ]+\d{2,4}\b"
        r"|\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\b"
    )
    date_formats = (
        "%d-%b-%Y", "%d-%b-%y", "%d/%b/%Y", "%d/%b/%y", "%d.%b.%Y", "%d.%b.%y",
        "%d-%B-%Y", "%d/%B/%Y", "%d %B %Y", "%d %b %Y", "%d-%m-%Y", "%d-%m-%y",
        "%d/%m/%Y", "%d/%m/%y", "%d.%m.%Y", "%d.%m.%y",
    )
    date_tokens = date_pattern.findall(text)
    # Some PDF extractors emit table-cell dates before the page title. Prefer
    # the explicitly labelled issue date when the centre provides one.
    date_token_group = (
        r"(\d{1,2}(?:[-/. ]+[A-Za-z]{3,9}|[-/. ]+\d{1,2})[-/. ]+\d{2,4}"
        r"|\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})"
    )
    issue_date_match = re.search(r"\b(?:Issue\s+)?Date\s*:\s*" + date_token_group, text, re.I)
    if issue_date_match:
        date_tokens.insert(0, issue_date_match.group(1))
    report_date = None
    for token in date_tokens:
        for date_format in date_formats:
            try:
                report_date = datetime.strptime(" ".join(token.split()), date_format).date()
                break
            except ValueError:
                continue
        if report_date:
            break
    if not report_date:
        raise RuntimeError(f"{centre} PDF did not expose a recognizable issue date.")
    from zoneinfo import ZoneInfo
    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    today = now.date()
    previous_day_still_valid = (
        report_date == today - timedelta(days=1)
        and now.time() < datetime.strptime("08:30", "%H:%M").time()
    )
    if report_date != today and not previous_day_still_valid:
        raise RuntimeError(f"{centre} forecast is dated {report_date.isoformat()} and is outside its live validity window.")

    # Preserve each centre's published wording; daily tables differ in layout.
    # pdfplumber reads these source PDFs' table cells and keeps each forecast
    # attached to its exact district row. Tripura uses a three-row cell group;
    # Assam adds a rotated forecast-label column.
    import pdfplumber
    district_row = None
    forecast_values = None
    with pdfplumber.open(io.BytesIO(pdf_content)) as source_pdf:
        for page in source_pdf.pages:
            for table in page.extract_tables() or []:
                for row_index, row in enumerate(table):
                    if not row or not row[0]:
                        continue
                    labels = []
                    for part in re.split(r"[/|]", str(row[0])):
                        # RMC PDF text extraction sometimes inserts (cid:NNN)
                        # glyph markers into the Hindi line beneath an English
                        # district name. Strip those markers before matching.
                        part = re.sub(r"\(cid:\d+\)", " ", part, flags=re.I)
                        english_words = re.findall(r"[A-Za-z][A-Za-z&.'-]*", part)
                        candidate = " ".join(english_words).strip()
                        if candidate:
                            labels.append(candidate)
                    if not labels or not unique_district_label_match(district, labels, threshold=0.86):
                        continue
                    group = [row]
                    for continuation in table[row_index + 1:row_index + 3]:
                        if continuation and not str(continuation[0] or "").strip():
                            group.append(continuation)
                        else:
                            break
                    first_forecast_column = 2 if len(row) >= 9 else 1
                    values = []
                    for column in range(first_forecast_column, max(len(cells) for cells in group)):
                        parts = []
                        for cells in group:
                            if column >= len(cells):
                                continue
                            cell = " ".join(str(cells[column] or "").split())
                            if re.search(r"\b(?:dry|rain|ra/ts|thunder|isol|scattered|likely|places|few)\b", cell, re.I):
                                parts.append(cell)
                        values.append(" · ".join(dict.fromkeys(parts)) or None)
                    if len(values) >= 5 and any(value for value in values[:5]):
                        district_row = row[0]
                        forecast_values = values
                        break
                if forecast_values is not None:
                    break
            if forecast_values is not None:
                break

    if forecast_values is None:
        raise RuntimeError(f"{centre} current PDF has no parseable forecast row for {district}.")
    return [{
        "district": district, "date": (report_date + timedelta(days=index)).isoformat(),
        "issue_date": report_date.isoformat(),
        "rainfall": forecast_values[index], "coverage": "",
        "source": f"{centre} district forecast PDF", "source_url": url,
    } for index in range(5)]


def fetch_live_district_forecasts(places, district_geometries=None):
    """Fetch exact-district live forecasts; regional RMC text is never assigned to a district."""
    states = sorted({state for _kind, state, _district in places}, key=normalized)
    rain_by_state_day, failures = {}, {}
    # The live IMD rainfall page has no <select>; its JavaScript map embeds the
    # exact state labels passed to the rainfall endpoint. Read those live labels.
    try:
        rain_page = requests.get(IMD_DISTRICT_RAIN_FORECAST_PAGE, headers=HEADERS, timeout=(5, 20))
        rain_page.raise_for_status()
        rain_state_options = _imd_rainfall_map_state_labels(rain_page.text)
    except Exception as exc:
        rain_state_options = []
        rain_state_error = str(exc)
    else:
        rain_state_error = ""
    rain_state_values = {}
    for state in states:
        matched_state = unique_district_label_match(
            state, [label for _value, label in rain_state_options], threshold=0.90
        )
        rain_state_values[state] = next(
            (value for value, label in rain_state_options if label == matched_state), None
        )
    rain_jobs = [(state, day) for state in states if rain_state_values.get(state)
                 for day in range(1, 6)]
    for state in states:
        if not rain_state_values.get(state):
            reason = rain_state_error or "State not listed in IMD's live rainfall forecast selector."
            for day in range(1, 6):
                failures[(state, day)] = reason
    with ThreadPoolExecutor(max_workers=min(10, max(1, len(rain_jobs)))) as pool:
        futures = {pool.submit(live_imd_district_rain_forecast, rain_state_values[state], day): (state, day)
                   for state, day in rain_jobs}
        for future, pair in futures.items():
            try:
                rain_by_state_day[pair] = future.result()
            except Exception as exc:
                failures[pair] = str(exc)

    output = []
    met_centre_pdf_cache = {}
    with ThreadPoolExecutor(max_workers=min(10, max(1, len(places)))) as pool:
        temperature_jobs = {}
        for _kind, state, district in places:
            geometry = (district_geometries or {}).get((state, district))
            if geometry is None:
                geometry = next((candidate for (boundary_state, boundary_district), candidate
                                 in (district_geometries or {}).items()
                                 if normalized(boundary_state) == normalized(state)
                                 and normalized(boundary_district) == normalized(district)), None)
            if geometry is not None:
                temperature_jobs[(state, district)] = pool.submit(
                    live_open_meteo_temperature_forecast, geometry
                )
        for kind, state, district in places:
            try:
                if (state, district) not in temperature_jobs:
                    raise RuntimeError("No live district boundary point was returned for Open-Meteo.")
                temperature_days = temperature_jobs[(state, district)].result()[:5]
                temperature_error = "" if temperature_days else "Open-Meteo returned no dated temperature forecast rows."
            except Exception as exc:
                temperature_days, temperature_error = [], str(exc)
            rainfall_days = []
            met_centre_days = None
            for day in range(1, 6):
                day_records = rain_by_state_day.get((state, day), {})
                matched_label = unique_district_label_match(district, list(day_records))
                record = day_records.get(district_label_key(matched_label)) if matched_label else None
                rainfall_days.append(record or {
                    "district": district, "date": None, "rainfall": None, "coverage": None,
                    "error": failures.get((state, day), "No exact live IMD district record was returned."),
                })
            # Use the matching Met Centre's live district PDF only when the
            # nationwide IMD district feed did not return that district/day.
            if any(row.get("rainfall") is None for row in rainfall_days):
                try:
                    state_key = normalized(state)
                    source_configs = MC_DISTRICT_FORECAST_PDFS.get(state_key, [])
                    last_source_error = "No current district PDF is connected for this Meteorological Centre."
                    for source_config in source_configs:
                        source_url = source_config[0]
                        if source_url not in met_centre_pdf_cache:
                            try:
                                mc_response = requests.get(source_url, headers=HEADERS, timeout=(5, 30))
                                mc_response.raise_for_status()
                                met_centre_pdf_cache[source_url] = mc_response.content
                            except Exception as exc:
                                met_centre_pdf_cache[source_url] = exc
                        cached_pdf = met_centre_pdf_cache[source_url]
                        if isinstance(cached_pdf, Exception):
                            last_source_error = str(cached_pdf)
                            continue
                        try:
                            met_centre_days = live_met_centre_district_forecast(
                                state, district, cached_pdf, source_config=source_config
                            )
                            break
                        except Exception as exc:
                            last_source_error = str(exc)
                    if met_centre_days is None:
                        raise RuntimeError(last_source_error)
                    mc_by_date = {_forecast_date_key(row.get("date")): row for row in met_centre_days}
                    for index, row in enumerate(rainfall_days):
                        if row.get("rainfall") is None:
                            mc_row = (mc_by_date.get(_forecast_date_key(row.get("date")))
                                      if row.get("date") else met_centre_days[index])
                            if mc_row and mc_row.get("rainfall") is not None:
                                row.update(mc_row)
                                row.pop("error", None)
                except Exception:
                    # Leave missing days visibly not reported rather than assigning a nearby
                    # district, stale report, or undated regional forecast.
                    pass
            output.append({
                "kind": kind, "state": state, "district": district,
                "fetched_at": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(timespec="seconds"),
                "rainfall_days": rainfall_days, "temperature_days": temperature_days,
                "temperature_error": temperature_error,
            })
    return output


def build_live_report_pdf(live_results, forecast_results, generated_at, generated_by="Signed-in user"):
    """Create a transient PDF from only the currently selected session's live feed results."""
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

    buffer = io.BytesIO()
    navy = colors.HexColor("#193b4a")
    teal = colors.HexColor("#287a68")
    line = colors.HexColor("#d7e3df")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold",
                              fontSize=19, leading=24, textColor=navy, alignment=TA_CENTER, spaceAfter=5))
    styles.add(ParagraphStyle(name="ReportSub", parent=styles["Normal"], fontSize=9, leading=13,
                              textColor=colors.HexColor("#5e7078"), alignment=TA_CENTER, spaceAfter=14))
    styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontName="Helvetica-Bold",
                              fontSize=13, leading=17, textColor=navy, spaceBefore=12, spaceAfter=7))
    styles.add(ParagraphStyle(name="District", parent=styles["Heading3"], fontName="Helvetica-Bold",
                              fontSize=10, leading=13, textColor=teal, spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle(name="Cell", parent=styles["BodyText"], fontSize=8, leading=10))
    styles.add(ParagraphStyle(name="TableHeader", parent=styles["BodyText"], fontName="Helvetica-Bold",
                              fontSize=8, leading=10, textColor=colors.white))
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8, leading=11,
                              textColor=colors.HexColor("#5e7078")))
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=15*mm, leftMargin=15*mm,
                            topMargin=16*mm, bottomMargin=17*mm,
                            title="DIWIS Live Weather Report", author="DIWIS")

    def para(value, style="Cell"):
        text = html.escape(str(value if value not in (None, "") else "No report"))
        return Paragraph(text, styles[style])

    def table(data, widths=None):
        converted = [[para(cell, "TableHeader") for cell in data[0]]]
        converted.extend([[para(cell) for cell in row] for row in data[1:]])
        result = Table(converted, colWidths=widths, repeatRows=1, hAlign="LEFT")
        result.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), navy),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), .4, line),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        return result

    story = [
        Paragraph("DIWIS · Live District Weather Report", styles["ReportTitle"]),
        Paragraph(
            f"Generated {html.escape(generated_at)} · Session-only data · No catchment analysis",
            styles["ReportSub"],
        ),
    ]
    all_keys = []
    for item in live_results:
        if item.get("error"):
            all_keys.append((item.get("kind"), item.get("state"), item.get("district")))
            continue
        all_keys.append((item.get("kind"), item.get("state"), item.get("district")))
    for forecast in forecast_results:
        key = (forecast.get("kind"), forecast.get("state"), forecast.get("district"))
        if key not in all_keys:
            all_keys.append(key)
    if not all_keys:
        story.append(para("No live data was returned for the selected districts."))

    current_by_key = {(item.get("kind"), item.get("state"), item.get("district")): item
                      for item in live_results}
    forecast_by_key = {(item.get("kind"), item.get("state"), item.get("district")): item
                       for item in forecast_results}
    primary_keys = [key for key in all_keys if key[0] == "Primary"]
    secondary_keys = [key for key in all_keys if key[0] != "Primary"]
    story.append(Paragraph("1. Primary district temperature", styles["Section"]))
    for kind, state, district in primary_keys:
        key = (kind, state, district)
        current = current_by_key.get(key, {})
        forecast = forecast_by_key.get(key, {})
        story.append(Paragraph(f"{html.escape(str(kind))} · {html.escape(str(district))}, {html.escape(str(state))}",
                               styles["District"]))
        temp_rows = forecast.get("temperature_days") or []
        temp_table = [["Open-Meteo forecast date", "Maximum (°C)", "Minimum (°C)"]]
        for row in temp_rows:
            temp_table.append([row.get("date"), row.get("maximum_c"), row.get("minimum_c")])
        if len(temp_table) == 1:
            temp_table.append(["No report", "No report", "No report"])
        story.append(Spacer(1, 4))
        story.append(table(temp_table, [55*mm, 55*mm, 55*mm]))
        if temp_rows:
            story.append(para(f"Temperature forecast source: {temp_rows[0].get('source') or 'Open-Meteo'}"
                              + (f" · grid coordinates {temp_rows[0].get('grid_latitude')}, {temp_rows[0].get('grid_longitude')}"
                                 if temp_rows[0].get("grid_latitude") is not None else ""), "Small"))

    def append_official_data(keys):
        for kind, state, district in keys:
            key = (kind, state, district)
            current = current_by_key.get(key, {})
            forecast = forecast_by_key.get(key, {})
            story.append(Paragraph(f"{html.escape(str(kind))} · {html.escape(str(district))}, {html.escape(str(state))}",
                                   styles["District"]))
            if kind != "Primary":
                temp_rows = forecast.get("temperature_days") or []
                if temp_rows:
                    temp_table = [["Open-Meteo forecast date", "Maximum (°C)", "Minimum (°C)"]]
                    temp_table.extend([[row.get("date"), row.get("maximum_c"), row.get("minimum_c")]
                                       for row in temp_rows])
                    story.append(table(temp_table, [55*mm, 55*mm, 55*mm]))
                    story.append(para(f"Temperature forecast source: {temp_rows[0].get('source') or 'Open-Meteo'}"
                                      + (f" · grid coordinates {temp_rows[0].get('grid_latitude')}, {temp_rows[0].get('grid_longitude')}"
                                         if temp_rows[0].get("grid_latitude") is not None else ""), "Small"))
            rainfall = current.get("rainfall") or {}
            story.append(para(
                f"Observed rainfall: {rainfall.get('value_mm') if rainfall.get('status') == 'OK' else 'No report'}"
                f" · Date: {rainfall.get('date') or 'No report'} · Source: {rainfall.get('source') or rainfall.get('reason') or 'No report'}"
            ))
            warning = current.get("warnings") or {}
            if warning.get("status") == "OK" and warning.get("items"):
                for warning_item in warning["items"]:
                    if isinstance(warning_item, dict):
                        hazards = ", ".join(str(value) for value in warning_item.get("hazards", [])) or "Warning"
                        story.append(para(f"Rain / thunderstorm warning: {hazards} · {format_clock_ampm(warning_item.get('text') or '')} · Source: {warning.get('source')}"))
            elif warning.get("status") == "OK" and warning.get("no_warning_days"):
                story.append(para(f"Rain / thunderstorm warning: Source reports no warning for day(s) {', '.join(map(str, warning['no_warning_days']))} · {warning.get('source')}"))
            else:
                story.append(para(f"Rain / thunderstorm warning: No report · {warning.get('reason') or 'No exact current official district record'}"))
            cyclone = current.get("cyclone") or {}
            cyclone_text = (f"Explicit cyclone warning reported · {cyclone.get('source')}"
                            if cyclone.get("status") == "OK" and cyclone.get("overlaps")
                            else f"No report · {cyclone.get('reason') or 'No verified current district cyclone record'}")
            story.append(para(f"Cyclone: {cyclone_text}"))
            lightning = current.get("lightning") or {}
            coordinates = lightning.get("coordinates") or []
            if coordinates:
                coord_rows = [["Latitude", "Longitude", "Source hour (UTC)"]]
                for point in coordinates:
                    if isinstance(point, dict):
                        coord_rows.append([point.get("latitude"), point.get("longitude"), format_clock_ampm(point.get("hour_utc"))])
                    else:
                        coord_rows.append([point, "", ""])
                story.append(para("Live lightning strike coordinates:"))
                story.append(table(coord_rows, [50*mm, 50*mm, 82*mm]))
            else:
                story.append(para(f"Live lightning strike coordinates: No report · {lightning.get('error') or 'No official coordinates returned'}"))

            rain_forecasts = forecast.get("rainfall_days") or []
            if rain_forecasts:
                forecast_table = [["Day", "Forecast date", "Rainfall", "Coverage"]]
                for index, row in enumerate(rain_forecasts, start=1):
                    forecast_table.append([
                        f"Day {index}", row.get("date"),
                        row.get("rainfall") or "No report",
                        row.get("coverage") or (row.get("error") or "No report"),
                    ])
                story.append(Spacer(1, 4))
                story.append(table(forecast_table, [16*mm, 32*mm, 42*mm, 90*mm]))

    story.append(Paragraph("3. Primary official live data", styles["Section"]))
    if primary_keys:
        append_official_data(primary_keys)
    else:
        story.append(para("Primary district data was not returned in this session."))

    story.append(Paragraph("4. Selected secondary state and district data", styles["Section"]))
    story.append(para("Only the secondary states and districts selected in DIWIS are included. No catchment or hydrological analysis is part of this section.", "Small"))
    if secondary_keys:
        append_official_data(secondary_keys)
    else:
        story.append(para("No secondary districts were selected."))

    source_urls = [
        ("IMD five-day district rainfall forecast", "https://mausam.imd.gov.in/responsive/5d_statewisedistricts_rf_forecast.php"),
        ("IMD public district rainfall observations", "https://mausam.imd.gov.in/responsive/rainfallinformation.php"),
        ("RMC Guwahati district warning and observation pages", "https://mausam.imd.gov.in/guwahati/"),
        ("NRSC–ISRO Bhuvan Lightning Portal", "https://bhuvan-app1.nrsc.gov.in/lightning/"),
        ("Open-Meteo temperature forecast", "https://open-meteo.com/"),
    ]
    story.append(Paragraph("Sources and report limits", styles["Section"]))
    story.append(para("Values are included only when returned by the live official pages during this session. Missing, stale, or unmatched feeds remain not reported. No forecast is estimated, and no secondary catchment analysis is included.", "Small"))
    for label, url in source_urls:
        story.append(Paragraph(
            f'<link href="{html.escape(url, quote=True)}" color="#287a68">{html.escape(label)}</link>',
            styles["Small"],
        ))
    story.append(Spacer(1, 4))
    story.append(para("Lightning reporting is limited to strike coordinates when the official feed supplies them.", "Small"))

    def footer(canvas, document):
        canvas.saveState()
        canvas.setStrokeColor(line)
        canvas.line(15*mm, 12*mm, A4[0] - 15*mm, 12*mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#708089"))
        canvas.setFont("Helvetica", 7)
        canvas.drawString(15*mm, 7*mm, f"Generated by {str(generated_by)[:64]}")
        canvas.drawRightString(A4[0] - 15*mm, 7*mm, f"Page {document.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return buffer.getvalue()


def build_rainfall_report_pdf(live_results, forecast_results, generated_at, generated_by="Signed-in user"):
    """Create an in-memory report from this session's live official-source results."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

    buffer = io.BytesIO()
    navy = colors.HexColor("#193b4a")
    teal = colors.HexColor("#287a68")
    border = colors.HexColor("#d7e3df")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="RainReportTitle", parent=styles["Title"], fontName="Helvetica-Bold",
                              fontSize=19, leading=24, textColor=navy, alignment=1, spaceAfter=5))
    styles.add(ParagraphStyle(name="RainReportSub", parent=styles["Normal"], fontSize=9, leading=13,
                              textColor=colors.HexColor("#5e7078"), alignment=1, spaceAfter=14))
    styles.add(ParagraphStyle(name="BulletinAuthority", parent=styles["Title"], fontName="Helvetica-Bold",
                              fontSize=14, leading=18, textColor=colors.HexColor("#17233a"), alignment=1, spaceAfter=2))
    styles.add(ParagraphStyle(name="BulletinSystem", parent=styles["Normal"], fontName="Helvetica-Bold",
                              fontSize=11, leading=14, textColor=colors.HexColor("#0087d4"), alignment=1, spaceAfter=3))
    styles.add(ParagraphStyle(name="BulletinMeta", parent=styles["Normal"], fontSize=8, leading=10,
                              textColor=colors.HexColor("#46566f"), alignment=1, spaceAfter=2))
    styles.add(ParagraphStyle(name="RainSection", parent=styles["Heading2"], fontName="Helvetica-Bold",
                              fontSize=13, leading=17, textColor=navy, spaceBefore=12, spaceAfter=7))
    styles.add(ParagraphStyle(name="RainDistrict", parent=styles["Heading3"], fontName="Helvetica-Bold",
                              fontSize=10, leading=13, textColor=teal, spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle(name="RainCell", parent=styles["BodyText"], fontSize=8, leading=10))
    styles.add(ParagraphStyle(name="RainHeader", parent=styles["BodyText"], fontName="Helvetica-Bold",
                              fontSize=8, leading=10, textColor=colors.white))
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=15*mm, leftMargin=15*mm,
                            topMargin=16*mm, bottomMargin=17*mm,
                            title="DIWIS Live District Weather Report", author="DIWIS")

    def table(rows, widths):
        converted = [[Paragraph(html.escape(str(value if value not in (None, "") else "No report")),
                                styles["RainHeader"] if row_index == 0 else styles["RainCell"])
                      for value in row] for row_index, row in enumerate(rows)]
        result = Table(converted, colWidths=widths, repeatRows=1, hAlign="LEFT")
        result.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), navy),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), .4, border),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        return result

    current_by_key = {(item.get("kind"), item.get("state"), item.get("district")): item
                      for item in live_results}
    forecast_by_key = {(item.get("kind"), item.get("state"), item.get("district")): item
                       for item in forecast_results}
    all_keys = list(current_by_key)
    all_keys.extend(key for key in forecast_by_key if key not in all_keys)
    primary_keys = [key for key in all_keys if key[0] == "Primary"]
    secondary_keys = [key for key in all_keys if key[0] != "Primary"]
    primary_header = primary_keys[0] if primary_keys else (all_keys[0] if all_keys else ("Primary", "Assam", "District not selected"))
    _, header_state, header_district = primary_header
    safe_district = html.escape(str(header_district))
    safe_state = html.escape(str(header_state))
    story = [
        Paragraph(f"DISTRICT DISASTER MANAGEMENT AUTHORITY (DDMA), {safe_district.upper()}", styles["BulletinAuthority"]),
        Paragraph("District Integrated Weather Information System (DIWIS) — Daily Bulletin", styles["BulletinSystem"]),
        Paragraph(f"District: {safe_district}, {safe_state}", styles["BulletinMeta"]),
        Paragraph(
            "Data Sources: India Meteorological Department (IMD), RMC Guwahati, Open-Meteo & NRSC–ISRO Bhuvan"
            f" &nbsp;|&nbsp; Bulletin Issued: {html.escape(generated_at)}",
            styles["BulletinMeta"],
        ),
        Spacer(1, 4),
        HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#0087d4"),
                   spaceBefore=2, spaceAfter=7),
    ]

    def append_rainfall(keys):
        for key in keys:
            kind, state, district = key
            current = current_by_key.get(key, {})
            forecast = forecast_by_key.get(key, {})
            story.append(Paragraph(
                f"{html.escape(str(kind))} · {html.escape(str(district))}, {html.escape(str(state))}",
                styles["RainDistrict"],
            ))
            story.append(Paragraph(
                html.escape(f"DIWIS data: {freshness_label(current.get('fetched_at'))}"),
                styles["RainCell"],
            ))
            observed = current.get("rainfall") or {}
            observed_value = observed.get("value_mm") if observed.get("status") == "OK" else None
            observed_label = ("No rain reported (0 mm)" if isinstance(observed_value, (int, float)) and observed_value == 0
                              else f"{observed_value} mm" if observed_value is not None else "No report · no verified live value")
            story.append(table([
                ["Observed rainfall", "Observation date", "Official source"],
                [observed_label,
                 observed.get("date"), observed.get("source") or observed.get("reason")],
            ], [48*mm, 42*mm, 90*mm]))

            rain_days = forecast.get("rainfall_days") or []
            forecast_rows = [["Forecast day", "Forecast date", "Rainfall forecast", "Distribution / coverage"]]
            for index, row in enumerate(rain_days, start=1):
                forecast_rows.append([
                    f"Day {index}", row.get("date"),
                    row.get("rainfall") or "No report",
                    row.get("coverage") or "No report",
                ])
            if len(forecast_rows) == 1:
                forecast_rows.append(["No report", "No report", "No report", "No report"])
            story.append(Spacer(1, 4))
            story.append(table(forecast_rows, [25*mm, 34*mm, 44*mm, 77*mm]))

    def append_primary_live(keys):
        for key in keys:
            kind, state, district = key
            current = current_by_key.get(key, {})
            forecast = forecast_by_key.get(key, {})
            story.append(Paragraph(
                f"{html.escape(str(district))}, {html.escape(str(state))}", styles["RainDistrict"]
            ))
            story.append(Paragraph(
                html.escape(f"DIWIS data: {freshness_label(current.get('fetched_at'))}"),
                styles["RainCell"],
            ))
            if current.get("error"):
                story.append(Paragraph(f"Live request not reported: {html.escape(str(current['error']))}", styles["RainCell"]))
                continue

            rainfall = current.get("rainfall") or {}
            rainfall_value = rainfall.get("value_mm") if rainfall.get("status") == "OK" else None
            rainfall_label = ("No rain reported (0 mm)" if isinstance(rainfall_value, (int, float)) and rainfall_value == 0
                              else f"{rainfall_value} mm" if rainfall_value is not None else "No report · no verified live value")
            rainfall_source = rainfall.get("source") or rainfall.get("reason")
            if rainfall.get("station"):
                rainfall_source = f"{rainfall_source} · station {rainfall['station']}"
            if rainfall.get("coverage_note"):
                rainfall_source = f"{rainfall_source} · {rainfall['coverage_note']}"
            story.append(table([
                ["Live observation", "Value", "Date / issue time", "Official source or status"],
                ["Observed rainfall", rainfall_label, rainfall.get("date"),
                 rainfall_source],
            ], [47*mm, 30*mm, 35*mm, 72*mm]))

            rain_days = forecast.get("rainfall_days") or []
            rain_rows = [["Rainfall forecast date", "Forecast", "Coverage / source status"]]
            rain_rows.extend([[row.get("date"), row.get("rainfall") if row.get("rainfall") is not None else "No report",
                               row.get("coverage") or row.get("error") or "No report"] for row in rain_days])
            if len(rain_rows) == 1:
                rain_rows.append(["No report", "No report", forecast.get("error") or "No live forecast returned"])
            story.append(Spacer(1, 4))
            story.append(table(rain_rows, [42*mm, 55*mm, 87*mm]))

            temp_days = forecast.get("temperature_days") or []
            temp_rows = [["Temperature forecast date", "Maximum (°C)", "Minimum (°C)"]]
            temp_rows.extend([[row.get("date"), row.get("maximum_c"), row.get("minimum_c")] for row in temp_days])
            if len(temp_rows) == 1:
                temp_rows.append(["No report", "No report", forecast.get("error") or "No live forecast returned"])
            story.append(Spacer(1, 4))
            story.append(table(temp_rows, [70*mm, 55*mm, 59*mm]))

            warnings = current.get("warnings") or {}
            nowcast = current.get("nowcast") or {}
            warning_items = warnings.get("items") or []
            warning_text = []
            for item in warning_items:
                if isinstance(item, dict):
                    hazards = ", ".join(map(str, item.get("hazards") or [])) or "Official warning"
                    warning_text.append(f"{hazards}: {format_clock_ampm(item.get('text') or '')}".strip())
            if warnings.get("status") == "OK" and not warning_text and warnings.get("no_warning_days"):
                warning_text.append("Source reports no warning for day(s) " + ", ".join(map(str, warnings["no_warning_days"])))
            warning_status = "\n".join(warning_text) if warning_text else warnings.get("reason") or "No report"
            story.append(Spacer(1, 4))
            story.append(table([
                ["Official warning / hazard feed", "Live result", "Source / issue date"],
                ["Rain / thunderstorm", warning_status, warnings.get("source") or warnings.get("issue_date") or "No report"],
                ["Live district nowcast", (
                    ("No warning" if nowcast.get("no_warning") else format_clock_ampm(nowcast.get("message") or "Live nowcast returned a warning"))
                    + (f" · issued {nowcast.get('issue_date')} {format_feed_clock(nowcast.get('issue_time'))} IST" if nowcast.get("issue_date") else "")
                    + (f" · valid up to {format_feed_clock(nowcast.get('valid_until'))} IST" if nowcast.get("valid_until") else "")
                    if nowcast.get("status") == "OK" else (
                        f"Expired · {nowcast_expiry_label(nowcast)}"
                        if nowcast.get("status") == "EXPIRED"
                        else f"STALE · last verified {nowcast.get('last_verified_at') or 'time not recorded'}"
                        if nowcast.get("status") == "STALE"
                        else f"No report · {nowcast.get('reason') or 'No verified live nowcast'}")),
                 nowcast.get("source") or "No report"],
            ], [42*mm, 92*mm, 50*mm]))

            lightning = current.get("lightning") or {}
            coordinates = lightning.get("coordinates") or []
            coordinate_rows = [[
                "Latitude", "Longitude", "Bhuvan source time", "Feed ID", "Current",
            ]]
            coordinate_rows.extend([[
                point.get("latitude"), point.get("longitude"),
                point.get("source_time") or "Not supplied",
                point.get("feed_id") or "Not supplied",
                point.get("current") or "Not supplied",
            ]
                                    if isinstance(point, dict)
                                    else [point, "No report", "No report", "No report", "No report"]
                                    for point in coordinates])
            if len(coordinate_rows) == 1:
                coordinate_rows.append([
                    "No feed points inside district" if lightning.get("status") == "OK"
                    else "NRSC live feed not reported",
                    format_clock_ampm(lightning.get("window_start")) or "No report",
                    "", "", "",
                ])
            story.append(Spacer(1, 4))
            story.append(Paragraph(
                f"Source: NRSC–ISRO Bhuvan hourly lightning data · window "
                f"{format_clock_ampm(lightning.get('window_start')) or 'not reported'} to {format_clock_ampm(lightning.get('window_end')) or 'not reported'}. "
                "Only point records within the selected district boundary are listed.",
                styles["RainCell"]))
            story.append(Paragraph(
                f"Bhuvan points returned inside this district boundary: {len(coordinates)}.",
                styles["RainCell"],
            ))
            story.append(table(coordinate_rows, [28*mm, 28*mm, 50*mm, 35*mm, 35*mm]))

    story.append(Paragraph("1. Primary district · all returned live data", styles["RainSection"]))
    if primary_keys:
        append_primary_live(primary_keys)
    else:
        story.append(Paragraph("Primary district live data was not returned in this session.", styles["RainCell"]))
    story.append(Paragraph("4. Selected secondary state and district rainfall", styles["RainSection"]))
    story.append(Paragraph(
        "Includes observed rainfall and rainfall forecasts returned for the selected secondary districts. "
        "No secondary temperature, cyclone, thunderstorm, lightning, or catchment content is included.",
        styles["RainCell"],
    ))
    if secondary_keys:
        append_rainfall(secondary_keys)
    else:
        story.append(Paragraph("No secondary districts were selected.", styles["RainCell"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        'Sources queried live by DIWIS: <link href="https://mausam.imd.gov.in/responsive/rainfallinformation.php" color="#287a68">'
        'IMD observed district rainfall</link> · '
        '<link href="https://www.imdpune.gov.in/cmpg/Realtimedata/Rainfall/Rain_Download.html" color="#287a68">'
        'IMD real-time 0.25° grid (only where a district has no IMD page value)</link> · '
        '<link href="https://mausam.imd.gov.in/responsive/5d_statewisedistricts_rf_forecast.php" color="#287a68">'
        'IMD five-day district rainfall forecast</link> · '
        '<link href="https://open-meteo.com/" color="#287a68">Open-Meteo temperature model</link> · '
        f'<link href="{RMC_DAILY_REPORT_URL}" color="#287a68">RMC Guwahati live daily forecast PDF</link> · '
        f'<link href="{IMD_NOWCAST_MAP_URL}" color="#287a68">IMD district nowcast</link> · '
        f'<link href="{IMD_WARNING_MAP_URL}" color="#287a68">IMD district warnings</link>. '
        'Field-level sources and not reported statuses are shown above. '
        'No cached or assumed readings are substituted.',
        styles["RainCell"],
    ))

    def footer(canvas, document):
        canvas.saveState()
        canvas.setStrokeColor(border)
        canvas.line(15*mm, 12*mm, A4[0] - 15*mm, 12*mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#708089"))
        canvas.setFont("Helvetica", 7)
        canvas.drawString(15*mm, 7*mm, f"Generated by {str(generated_by)[:64]}")
        canvas.drawRightString(A4[0] - 15*mm, 7*mm, f"Page {document.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return buffer.getvalue()


try:
    with st.spinner("Connecting to live district and state boundaries…"):
        neighbor_candidates, district_state, district_geometries, district_options = live_administrative_geography()
except Exception as exc:
    st.error(f"Live administrative geography is not reported: {exc}")
    st.info("No saved or hard-coded district list is used. Refresh after the live boundary service is available.")
    st.stop()

# Preserve the existing account authentication, role checks, assigned-district lock, and password reset.
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if not st.session_state.authenticated:
    welcome_col, login_col = st.columns([1.05, .95], gap="small")
    with welcome_col:
        st.markdown("""
        <div class="login-welcome">
          <div class="login-welcome-mark">🌦</div>
          <h1>Welcome to DIWIS</h1>
          <p>District Integrated Weather Info System brings district weather observations, forecasts and official warnings together in one clear workspace.</p>
          <div class="login-caption">LIVE DISTRICT WEATHER · IMD &amp; RMC SOURCES</div>
        </div>
        """, unsafe_allow_html=True)
    with login_col:
      with st.container(key="login_form_col"):
        st.markdown('<div class="login-form-title">Sign in to your account</div><div class="login-form-hint">Use your assigned DIWIS account to continue.</div>', unsafe_allow_html=True)
        with st.form("diwis_login_form"):
            login_district = st.selectbox("Operational district · Assam", district_options)
            st.caption("District list comes live from IMD's current district layers; a district IMD has not published yet will not appear.")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign in", type="primary", width="stretch")
        if submit:
            ok, message, user = authenticate_user(username, password, login_district, db_path=DB_PATH)
            if ok and user:
                st.session_state.authenticated = True
                st.session_state.user = user
                st.session_state.primary_district = user.get("active_district") or login_district
                st.rerun()
            else:
                st.error(message)
    st.stop()

if st.session_state.get("data_pipeline_version") != DATA_PIPELINE_VERSION:
    st.session_state.pop("live_results", None)
    st.session_state.pop("live_selection", None)
    st.session_state.pop("live_synced_at", None)
    st.session_state.pop("live_synced_epoch", None)
    st.session_state.pop("live_forecasts", None)
    st.session_state.pop("live_forecast_selection", None)
    st.session_state.data_pipeline_version = DATA_PIPELINE_VERSION

user = st.session_state.get("user") or {}
user_role = user.get("role", "staff")
user_district = user.get("active_district") or user.get("district", "")
if user.get("must_change_password") == 1:
    st.warning("Change your initial password to continue.")
    with st.form("required_password_change"):
        old_password = st.text_input("Current password", type="password")
        new_password = st.text_input("New password · at least 6 characters", type="password")
        confirm_password = st.text_input("Confirm new password", type="password")
        save_password = st.form_submit_button("Update password", type="primary")
    if save_password:
        if new_password != confirm_password or len(new_password.strip()) < 6:
            st.error("Enter matching passwords with at least 6 characters.")
        else:
            ok, message = update_user_password(user.get("username", ""), new_password, current_password=old_password, db_path=DB_PATH)
            if ok:
                st.session_state.user["must_change_password"] = 0
                st.success("Password updated.")
                st.rerun()
            else:
                st.error(message)
    st.stop()

st.sidebar.markdown('''<div class="sidebar-brand"><div class="sidebar-brand-mark">🌦</div><div><div class="sidebar-brand-name">DIWIS</div><div class="sidebar-brand-caption">District weather workspace</div></div></div>''', unsafe_allow_html=True)
navigation = ["Dashboard"]
if user_role in ("district_admin", "superadmin"):
    navigation.append("User administration")
navigation.append("Data sources")
navigation.append("My account")
if st.session_state.get("diwis_navigation") not in navigation:
    st.session_state.diwis_navigation = "Dashboard"
page = st.sidebar.radio("Navigation", navigation, index=0, key="diwis_navigation", label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.caption("LOCATION FILTERS")
st.sidebar.caption(f"Signed in · {user.get('full_name') or user.get('username')}")

if user_role == "superadmin":
    current_primary = st.session_state.get("primary_district") or user_district
    match_index = next((i for i, name in enumerate(district_options)
                        if normalized(name) == normalized(current_primary)), 0)
    primary_district = st.sidebar.selectbox("Primary district · Assam", district_options,
                                            index=match_index, key="primary_district_selector")
    st.session_state.primary_district = primary_district
else:
    primary_district = user_district
    st.sidebar.text_input("Primary district · Assam", value=primary_district, disabled=True)

neighboring_states = st.sidebar.multiselect(
    "Secondary states", neighbor_candidates,
    help="Includes Assam and states bordering Assam, from live administrative boundaries.",
    key="selected_neighbor_states",
)
secondary_district_options = sorted(
    {(state_name, district_name) for state_name, district_name in district_state
     if state_name in neighboring_states
     and not (normalized(state_name) == "assam" and normalized(district_name) == normalized(primary_district))},
    key=lambda item: (normalized(item[0]), normalized(item[1]))
)
stored_pairs = st.session_state.get("selected_neighbor_districts", [])
valid_pairs = [pair for pair in stored_pairs if pair in secondary_district_options]
if stored_pairs != valid_pairs:
    st.session_state.selected_neighbor_districts = valid_pairs
selected_pairs = st.sidebar.multiselect(
    "Secondary districts · multiple", secondary_district_options,
    format_func=lambda item: f"{item[1]} · {item[0]}",
    disabled=not neighboring_states, key="selected_neighbor_districts",
)
if page == "User administration" and user_role in ("district_admin", "superadmin"):
    st.subheader("User administration")
    st.caption("Manage account access. Weather readings are not stored with account records.")
    with st.form("create_portal_user"):
        allowed_roles = ["staff"] + (["district_admin", "superadmin"] if user_role == "superadmin" else [])
        new_role = st.selectbox("Account role", allowed_roles)
        new_district = st.selectbox("Account district", district_options)
        new_username = st.text_input("New username")
        new_full_name = st.text_input("Name")
        new_password = st.text_input("Initial password · at least 6 characters", type="password")
        create_submit = st.form_submit_button("Create account", type="primary")
    if create_submit:
        if len(new_password.strip()) < 6:
            st.error("Initial password must have at least 6 characters.")
        else:
            ok, message = create_user(new_username, new_password, new_full_name, new_role,
                                      "ALL" if new_role == "superadmin" else new_district,
                                      created_by=user.get("username", "operator"), db_path=DB_PATH)
            (st.success if ok else st.error)(message)
    accounts = get_district_users(user_district if user_role != "superadmin" else None,
                                  requester_role=user_role, db_path=DB_PATH)
    if accounts:
        st.dataframe(accounts, hide_index=True, width="stretch")

elif page == "Data sources":
    st.subheader("Data sources")
    st.caption("Where each reading on the dashboard comes from. Every value on the dashboard shows its own source and date.")
    st.markdown(
        "**Observed rainfall**  \n"
        "[IMD district rainfall](https://mausam.imd.gov.in/responsive/rainfallinformation.php) · "
        "[IMD 0.25° real-time grid](https://www.imdpune.gov.in/cmpg/Realtimedata/Rainfall/Rain_Download.html) "
        "(area-weighted estimate, used only when the district page has no value) · "
        "[RMC Guwahati](https://mausam.imd.gov.in/guwahati/) (Assam stations)\n\n"
        "**Rain forecast**  \n"
        "[IMD five-day district forecast](https://mausam.imd.gov.in/responsive/5d_statewisedistricts_rf_forecast.php) · "
        "Regional Met Centre district PDFs\n\n"
        "**Temperature**  \n"
        "[Open-Meteo](https://open-meteo.com/) model forecast at the district's reference point\n\n"
        "**Warnings and nowcast**  \n"
        "[IMD district warnings](https://mausam.imd.gov.in/responsive/districtWiseWarningGIS.php) · "
        "[IMD district nowcast](https://mausam.imd.gov.in/responsive/districtWiseNowcastGIS.php) · "
        "RMC Guwahati fallback for Assam\n\n"
        "**Lightning coordinates**  \n"
        "[NRSC–ISRO Bhuvan](https://bhuvan-app1.nrsc.gov.in/lightning/)"
    )

elif page == "My account":
    st.subheader("My account")
    st.write(user.get("full_name") or user.get("username"))
    st.caption(f"Role: {user_role.replace('_', ' ').title()} · Assigned district: {user_district}")
    if st.button("Sign out", width="stretch"):
        st.session_state.clear()
        st.rerun()

def fetch_selected_live_data(places):
    results = []
    progress = st.progress(0)
    rmc_station_report = None
    rmc_station_error = None
    public_rainfall_records = None
    public_rainfall_error = None
    rmc_today_report = None
    rmc_today_error = None

    def get_public_rainfall_records():
        nonlocal public_rainfall_records, public_rainfall_error
        if public_rainfall_records is None and public_rainfall_error is None:
            try:
                public_rainfall_records = live_imd_public_rainfall_records()
            except Exception as exc:
                public_rainfall_error = str(exc)
        if public_rainfall_error:
            raise RuntimeError(public_rainfall_error)
        return public_rainfall_records

    def get_rmc_station_report():
        nonlocal rmc_station_report, rmc_station_error
        if rmc_station_report is None and rmc_station_error is None:
            try:
                rmc_station_report = live_rmc_assam_station_observations()
            except Exception as exc:
                rmc_station_error = str(exc)
        if rmc_station_error:
            raise RuntimeError(rmc_station_error)
        return rmc_station_report

    def get_rmc_today_report():
        nonlocal rmc_today_report, rmc_today_error
        if rmc_today_report is None and rmc_today_error is None:
            try:
                rmc_today_report = live_rmc_assam_today_report()
            except Exception as exc:
                rmc_today_error = str(exc)
        if rmc_today_error:
            raise RuntimeError(rmc_today_error)
        return rmc_today_report

    lightning_feed = None
    lightning_feed_error = None
    warning_features = None
    warning_feed_error = None
    nowcast_features = None
    nowcast_feed_error = None
    rmc_warning_records = None
    rmc_warning_error = None
    rmc_nowcast_records = None
    rmc_nowcast_error = None

    def get_rmc_warning_records():
        nonlocal rmc_warning_records, rmc_warning_error
        if rmc_warning_records is None and rmc_warning_error is None:
            try:
                rmc_warning_records = live_rmc_assam_warning_features()
            except Exception as exc:
                rmc_warning_error = str(exc)
        if rmc_warning_error:
            raise RuntimeError(rmc_warning_error)
        return rmc_warning_records

    def get_rmc_nowcast_records():
        nonlocal rmc_nowcast_records, rmc_nowcast_error
        if rmc_nowcast_records is None and rmc_nowcast_error is None:
            try:
                rmc_nowcast_records = live_rmc_assam_nowcast_records()
            except Exception as exc:
                rmc_nowcast_error = str(exc)
        if rmc_nowcast_error:
            raise RuntimeError(rmc_nowcast_error)
        return rmc_nowcast_records

    with ThreadPoolExecutor(max_workers=3) as pool:
        lightning_future = pool.submit(live_nrsc_lightning_hourly_records)
        warning_future = pool.submit(live_imd_district_feed, IMD_DISTRICT_WARNING_LAYER)
        nowcast_future = pool.submit(live_imd_district_feed, IMD_DISTRICT_NOWCAST_LAYER)
        try:
            lightning_feed = lightning_future.result()
        except Exception as exc:
            lightning_feed_error = str(exc)
        try:
            warning_features = warning_future.result()
        except Exception as exc:
            warning_feed_error = str(exc)
        try:
            nowcast_features = nowcast_future.result()
        except Exception as exc:
            nowcast_feed_error = str(exc)

    for index, (kind, state, district) in enumerate(places):
        try:
            district_geometry = next(
                (geometry for (boundary_state, boundary_district), geometry in district_geometries.items()
                 if normalized(boundary_state) == normalized(state)
                 and normalized(boundary_district) == normalized(district)),
                None,
            )
            if district_geometry is None:
                raise RuntimeError(f"No exact live IMD boundary match for {district}, {state}.")
            rainfall = None
            try:
                rainfall = {"status": "OK", **live_imd_public_rainfall(
                    state, district, get_public_rainfall_records())}
            except Exception as imd_rain_error:
                rainfall_error = f"IMD public page: {imd_rain_error}"
            if rainfall is None and normalized(state) == "assam":
                try:
                    row = live_rmc_today_station_value(get_rmc_today_report(), district)
                    if row.get("rainfall") is None:
                        raise RuntimeError("RMC has no rainfall value for this station today.")
                    rainfall = {"status": "OK", "value_mm": row["rainfall"], "date": row["date"],
                                "source": row["source"], "station": row["station"],
                                "matched_source_label": row.get("matched_source_label"),
                                "coverage_note": row.get("coverage_note")}
                except Exception as rmc_exc:
                    try:
                        row = live_rmc_assam_station_value(get_rmc_station_report(), district)
                        rainfall = {"status": "OK", "value_mm": row.get("rain_mm"), "date": row["date"],
                                    "source": row["source"], "station": row.get("station"),
                                    "matched_source_label": row.get("matched_source_label"),
                                    "coverage_note": row.get("coverage_note")}
                    except Exception as pdf_exc:
                        rainfall_error += f" RMC public report: {rmc_exc}; RMC daily report: {pdf_exc}"
            if rainfall is None:
                try:
                    rainfall = {"status": "OK", **live_imd_grid_district_rainfall(district_geometry)}
                except Exception as grid_exc:
                    rainfall_error += f" IMD real-time grid: {grid_exc}"
            if rainfall is None:
                rainfall = {"status": "UNAVAILABLE", "reason": rainfall_error}

            temperatures = {
                "status": "FORECAST_ONLY",
                "source": "Open-Meteo live model forecast",
                "reason": "Temperature is sourced from Open-Meteo only.",
            }

            if warning_features is not None:
                warnings = live_imd_district_warning(warning_features, state, district, district_geometry)
            else:
                warnings = {"status": "UNAVAILABLE", "items": [], "reason": warning_feed_error}
            if warnings.get("status") != "OK" and normalized(state) == "assam":
                try:
                    warnings = live_rmc_assam_district_warning(get_rmc_warning_records(), district)
                except Exception as exc:
                    warnings["reason"] = f"IMD district feed: {warning_feed_error or warnings.get('reason')}; RMC Guwahati: {exc}"

            nowcast = compute_nowcast(state, district, district_geometry, nowcast_features,
                                      nowcast_feed_error, get_rmc_nowcast_records)
            nowcast_checked_at = datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(timespec="seconds")
            nowcast["last_checked_at"] = nowcast_checked_at
            if nowcast.get("status") in {"OK", "EXPIRED"}:
                nowcast["last_verified_at"] = nowcast_checked_at

            cyclone_items = [warning for warning in warnings.get("items", [])
                             if warning_mentions_cyclone(warning)]
            if cyclone_items:
                cyclone = {"status": "OK", "overlaps": True,
                           "source": warnings.get("source") or "IMD district warning map",
                           "issue_date": warnings.get("issue_date"), "items": cyclone_items}
            else:
                cyclone = {"status": "UNAVAILABLE", "reason":
                           "No explicit current district cyclone warning was found in the public RMC warning page."}

            if lightning_feed is not None:
                lightning = live_nrsc_lightning_coordinates(lightning_feed, district_geometry)
            else:
                lightning = {"status": "UNAVAILABLE", "coordinates": [], "error": lightning_feed_error}
            results.append({"district": district, "state": state, "kind": kind,
                            "fetched_at": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(timespec="seconds"),
                            "rainfall": rainfall, "temperatures": temperatures,
                            "lightning": lightning, "warnings": warnings, "nowcast": nowcast,
                            "cyclone": cyclone})
        except Exception as exc:
            results.append({"district": district, "state": state, "kind": kind, "error": str(exc)})
        progress.progress((index + 1) / len(places))
    st.session_state.live_results = results
    assam_geometries = sorted(
        ((district, geometry) for (state, district), geometry in district_geometries.items()
         if normalized(state) == "assam"),
        key=lambda row: normalized(row[0]),
    )
    if lightning_feed is None:
        st.session_state.assam_lightning_results = [
            {"district": district, "status": "UNAVAILABLE", "coordinates": [],
             "error": lightning_feed_error}
            for district, _geometry in assam_geometries
        ]
        st.session_state.assam_lightning_feed_count = None
        st.session_state.assam_lightning_window = None
    else:
        st.session_state.assam_lightning_results = [
            {"district": district, **live_nrsc_lightning_coordinates(lightning_feed, geometry)}
            for district, geometry in assam_geometries
        ]
        st.session_state.assam_lightning_feed_count = len(lightning_feed["records"])
        st.session_state.assam_lightning_window = {
            "start": lightning_feed["window_start"].strftime("%Y-%m-%d %H:%M UTC"),
            "end": lightning_feed["window_end"].strftime("%Y-%m-%d %H:%M UTC"),
        }
    st.session_state.live_synced_at = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %I:%M:%S %p IST")
    st.session_state.live_selection = tuple(places)


@st.fragment(run_every="15m")
def render_live_dashboard(primary_district, selected_pairs):
    st.subheader("Live district conditions")
    places = [("Primary", "Assam", primary_district)] + [("Secondary", state, district) for state, district in selected_pairs]
    selection_key = tuple(places)
    import time as _time
    last_sync = st.session_state.get("live_synced_epoch", 0)
    selection_changed = st.session_state.get("live_selection") != selection_key
    sync_due = selection_changed or not last_sync or _time.time() - last_sync >= 12 * 60 * 60
    button_label = "Load live data" if "live_results" not in st.session_state else "Refresh live data"
    manual_refresh = st.button(button_label, type="primary", width="stretch")
    if manual_refresh or sync_due:
        with st.status("Syncing live data…", expanded=False) as load_status:
            fetch_selected_live_data(places)
            load_status.update(label="Loading district forecasts…", state="running")
            st.session_state.live_forecasts = fetch_live_district_forecasts(places, district_geometries)
            st.session_state.live_forecast_selection = selection_key
            st.session_state.live_forecast_synced_at = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %I:%M:%S %p IST")
            try:
                st.session_state.live_snapshot_count = save_live_daily_snapshot(
                    st.session_state.get("live_results", []),
                    st.session_state.live_forecasts,
                    db_path=DB_PATH,
                )
                st.session_state.live_snapshot_error = ""
            except Exception as exc:
                st.session_state.live_snapshot_error = str(exc)
            load_status.update(label="Live data loaded", state="complete")
        st.session_state.live_synced_epoch = _time.time()
        st.session_state.nowcast_checked_epoch = _time.time()
        selection_changed = False
    elif (st.session_state.get("live_results") and not selection_changed
          and _time.time() - st.session_state.get("nowcast_checked_epoch", 0) >= 10 * 60):
        # Nowcasts are short-lived: re-read just those sources every ~15 minutes and store
        # the new entry (with its own issue/validity times) when the source has changed.
        changed_districts = refresh_live_nowcasts(places, district_geometries)
        st.session_state.nowcast_checked_epoch = _time.time()
        if changed_districts:
            try:
                save_live_daily_snapshot(st.session_state.get("live_results", []),
                                         st.session_state.get("live_forecasts", []), db_path=DB_PATH)
            except Exception as exc:
                st.session_state.live_snapshot_error = str(exc)
    snapshot_message = ("Refresh snapshot saved to SQLite history"
                        if not st.session_state.get("live_snapshot_error")
                        else "SQLite history save failed")
    st.caption(
        f"Updated: {st.session_state.get('live_synced_at', 'Not loaded')} · Full auto-sync every 12 hours · "
        f"Nowcasts re-checked every 15 minutes (last check: {st.session_state.get('nowcast_checked_at', 'not yet')}) · "
        f"{snapshot_message}"
    )
    if st.session_state.get("live_snapshot_error"):
        st.warning("Live data loaded, but the daily SQLite snapshot could not be saved.")
    results = [] if selection_changed else st.session_state.get("live_results", [])
    if selection_changed:
        st.info("Syncing live data for the selected districts…")
    forecast_selection = st.session_state.get("live_forecast_selection")
    forecast_results = (st.session_state.get("live_forecasts", [])
                        if forecast_selection == selection_key else [])
    forecast_by_place = {
        (normalized(row.get("state")), normalized(row.get("district"))): row
        for row in forecast_results
    }
    st.subheader("5-day district forecast")
    if forecast_results:
        st.caption(f"Live forecast request: {st.session_state.get('live_forecast_synced_at', 'time not reported')} · Rain: [IMD district rainfall forecast](https://mausam.imd.gov.in/responsive/5d_statewisedistricts_rf_forecast.php) · Temperature: [Open-Meteo](https://open-meteo.com/) only")
        forecast_group = None
        for forecast in forecast_results:
            current_group = "Primary" if forecast["kind"] == "Primary" else "Selected neighboring districts"
            if current_group != forecast_group:
                st.markdown(f"#### {current_group}")
                forecast_group = current_group
            st.markdown(f"**{forecast['kind']} · {forecast['district']}, {forecast['state']}**")
            st.caption(
                f"DIWIS forecast fetch: {freshness_label(forecast.get('fetched_at'))} · "
                f"source issue date: {next((row.get('issue_date') for row in forecast.get('rainfall_days', []) if row.get('issue_date')), 'not provided by feed')}."
            )
            temp_rows = forecast.get("temperature_days") or []
            temperatures_by_date = {
                _forecast_date_key(row.get("date")): row for row in temp_rows
                if _forecast_date_key(row.get("date"))
            }
            rows = []
            rain_rows = forecast.get("rainfall_days") or []
            for index in range(1, 6):
                rain = rain_rows[index - 1] if index <= len(rain_rows) else {}
                temp_candidate = temp_rows[index - 1] if index <= len(temp_rows) else {}
                forecast_date = rain.get("date") or temp_candidate.get("date") or "—"
                forecast_date_key = _forecast_date_key(forecast_date)
                temperature = temperatures_by_date.get(forecast_date_key, {}) if forecast_date_key else {}
                rows.append({
                    "Forecast day": f"Day {index}",
                    "Forecast date": forecast_date,
                    "Rainfall forecast": (
                        "No rain" if str(rain.get("coverage") or "").strip().casefold() == "no rain"
                        else " · ".join(value for value in (
                            str(rain.get("rainfall") or "").strip(),
                            str(rain.get("coverage") or "").strip(),
                        ) if value)
                        if rain.get("rainfall") is not None else "Not reported"
                    ),
                    "Rainfall source": rain.get("source") or "—",
                    # Always text, so the column is one type (numbers mixed with text break Arrow conversion).
                    "Temperature max (°C)": temperature_cell(temperature.get("maximum_c")),
                    "Temperature min (°C)": temperature_cell(temperature.get("minimum_c")),
                })
            st.dataframe(rows, hide_index=True, width="stretch")
            if temp_rows:
                temp_source = temp_rows[0]
                if temp_source.get("source_url") == "https://open-meteo.com/":
                    grid_lat, grid_lon = temp_source.get("grid_latitude"), temp_source.get("grid_longitude")
                    point_caption = (f" · model grid {grid_lat:.3f}, {grid_lon:.3f}"
                                     if isinstance(grid_lat, (int, float)) and isinstance(grid_lon, (int, float))
                                     else "")
                    st.caption(f"Temperature source: [Open-Meteo live model forecast](https://open-meteo.com/) · grid forecast at this district's live boundary reference point{point_caption}.")
                else:
                    st.caption(f"Temperature source: {temp_source.get('source') or 'Open-Meteo'}")
            missing_rain = [rain.get("error") for rain in forecast.get("rainfall_days", [])
                            if rain.get("error")]
            if missing_rain:
                st.caption("Rainfall: " + str(missing_rain[0])[:140])
            if not temp_rows:
                st.caption("Open-Meteo temperature: " + str(forecast.get("temperature_error") or "No forecast returned.")[:140])
    elif forecast_selection != selection_key:
        st.info("Load live data to see forecasts.")
    if results:
        st.subheader("Current results")
        if selected_pairs:
            st.caption("Neighboring-district readings require exact live feed matches; connected RMC station reports cover Assam.")
        current_group = None
        for item in results:
            group = "Primary" if item["kind"] == "Primary" else "Selected neighboring districts"
            if group != current_group:
                st.markdown(f"#### {group}")
                current_group = group
            st.subheader(f"{item['kind']} · {item['district']}, {item['state']}")
            if item.get("error"):
                st.warning(f"No live district result: {item.get('error')}")
                continue
            st.caption(
                f"DIWIS data fetch: {freshness_label(item.get('fetched_at'))} · "
                "Source issue/observation dates are shown per feed when available."
            )
            rainfall = item.get("rainfall") or {}
            temperatures = item.get("temperatures") or {}
            temperature_forecast = forecast_by_place.get(
                (normalized(item.get("state")), normalized(item.get("district"))), {}
            ).get("temperature_days") or []
            forecast_today = temperature_forecast[0] if temperature_forecast else {}
            using_temperature_forecast = (
                temperatures.get("status") != "OK"
                and forecast_today.get("maximum_c") is not None
                and forecast_today.get("minimum_c") is not None
            )
            max_temp = forecast_today.get("maximum_c") if using_temperature_forecast else temperatures.get("maximum_c")
            min_temp = forecast_today.get("minimum_c") if using_temperature_forecast else temperatures.get("minimum_c")
            m1, m2, m3 = st.columns(3)
            rain_value = rainfall.get("value_mm")
            try:
                rain_number = float(rain_value)
            except (TypeError, ValueError):
                rain_number = None
            rain_display = (("No rain · 0 mm" if rain_number == 0
                             else f"{rain_number:g} mm" if rain_number is not None else str(rain_value))
                            if rainfall.get("status") == "OK" else "No current district reading")
            rain_label = (
                "District rainfall · IMD grid average"
                if str(rainfall.get("source", "")).startswith("IMD real-time 0.25° rainfall grid")
                else "Station rainfall · daily observed" if rainfall.get("station")
                else "District rainfall · daily observed"
            )
            m1.metric(rain_label, rain_display)
            maximum = temperatures.get("maximum_c")
            minimum = temperatures.get("minimum_c")
            temp_label = "Temperature forecast" if using_temperature_forecast else "Temperature observed"
            m2.metric(f"{temp_label} · maximum", f"{float(max_temp):g} °C" if max_temp is not None else "No report")
            m3.metric(f"{temp_label} · minimum", f"{float(min_temp):g} °C" if min_temp is not None else "No report")
            source_notes = []
            if rainfall.get("status") == "OK":
                station = f" · station {rainfall['station']}" if rainfall.get("station") else ""
                matched_label = (f" · source label {rainfall['matched_source_label']}"
                                 if rainfall.get("matched_source_label") else "")
                coverage_note = (f" · {rainfall['coverage_note']}"
                                 if rainfall.get("coverage_note") else "")
                source_notes.append(
                    f"rainfall: {rainfall.get('source', 'IMD')} · date {rainfall.get('date')}"
                    f"{station}{matched_label}{coverage_note}"
                )
            else:
                source_notes.append(f"Rainfall: {rainfall.get('reason') or 'no matching current district record'}")
            if temperatures.get("status") == "OK":
                missing_extrema = []
                if maximum is None:
                    missing_extrema.append("maximum not reported")
                if minimum is None:
                    missing_extrema.append("minimum not reported")
                detail = f" · {' and '.join(missing_extrema)}" if missing_extrema else ""
                source_notes.append(f"Temperature: {temperatures.get('source')} · {temperatures.get('date')} · {temperatures.get('station')}{detail}")
            else:
                if using_temperature_forecast:
                    source_notes.append(
                        f"Temperature forecast: {forecast_today.get('source')} · {forecast_today.get('date')}"
                    )
                else:
                    source_notes.append(f"Temperature: {temperatures.get('reason') or 'no current district station report'}")
            st.caption(" · ".join(source_notes))
            source_urls = []
            if rainfall.get("status") == "OK":
                rain_source_links = {
                    "IMD public district rainfall page": "[IMD public district rainfall](https://mausam.imd.gov.in/responsive/rainfallinformation.php)",
                    "IMD real-time 0.25° rainfall grid (area-weighted district average)": "[IMD real-time 0.25° grid](https://www.imdpune.gov.in/cmpg/Realtimedata/Rainfall/Rain_Download.html)",
                    "RMC Guwahati today's weather report": "[RMC Guwahati today's weather report](https://mausam.imd.gov.in/imd_latest/contents/Todaysweather_mc.php?id=24)",
                    "RMC Guwahati daily station report": "[RMC Guwahati daily report](https://mausam.imd.gov.in/guwahati/mcdata/dwr.pdf)",
                }
                source_urls.append(rain_source_links.get(rainfall.get("source"), ""))
            if any(source_urls):
                st.caption("Source: " + " · ".join(dict.fromkeys(link for link in source_urls if link)))
            warnings = item.get("warnings") or {}
            st.markdown("**Rain and thunderstorm warning**")
            if warnings.get("status") != "OK":
                st.caption(f"No warning feed result · {warnings.get('reason') or 'IMD did not return a current district record'}")
            elif warnings.get("items"):
                for warning in warnings["items"]:
                    if not isinstance(warning, dict):
                        continue
                    hazards = warning.get("hazards") or []
                    label = ", ".join(str(hazard) for hazard in hazards) or "Warning"
                    extra_text = format_clock_ampm(warning.get("text"))
                    extra = f" · {extra_text}" if extra_text else ""
                    st.write(f"Day {warning.get('day', '—')} · {warning.get('date') or 'Date not reported'} · {label}{extra}")
                if warnings.get("source") == "RMC Guwahati":
                    warning_link = "[RMC Guwahati warning portal](https://mausam.imd.gov.in/imd_latest/contents/districtwise-warning_mc.php?id=24)"
                else:
                    warning_link = f"[IMD district warning map]({IMD_WARNING_MAP_URL})"
                st.caption(f"Source: {warnings.get('source', 'IMD')} · Updated {format_clock_ampm(warnings.get('updated_at') or warnings.get('issue_date') or 'time not reported')} · {warning_link}")
            elif warnings.get("no_warning_days"):
                days = ", ".join(str(day) for day in warnings["no_warning_days"])
                st.caption(f"{warnings.get('source', 'IMD')}: No warning · Days {days} · Updated {format_clock_ampm(warnings.get('updated_at') or warnings.get('issue_date') or 'time not reported')}")
            else:
                st.caption("No thunderstorm warning details in feed")
            if warnings.get("status") == "OK" and warnings.get("missing_days"):
                st.caption("Feed left day(s) " + ", ".join(map(str, warnings["missing_days"]))
                           + " blank. Treat those days as not reported, not as no warning.")
            if warnings.get("status") == "OK":
                warning_issue_date = warnings.get("issue_date") or warnings.get("updated_at")
                st.caption(
                    f"DIWIS checked with the live request · source issue date: "
                    f"{warning_issue_date or 'not provided'} · source update time: not provided by this feed."
                )
            nowcast = item.get("nowcast") or {}
            st.markdown("**Nowcast**")
            if nowcast.get("status") == "OK":
                issue = f"Issued {nowcast.get('issue_date') or 'time not supplied'} {format_feed_clock(nowcast.get('issue_time')) or ''} IST".strip()
                valid = f" · valid up to {format_feed_clock(nowcast.get('valid_until'))} IST" if nowcast.get("valid_until") else ""
                if nowcast.get("no_warning"):
                    st.success(f"No warning · {issue}{valid}")
                else:
                    st.warning(f"{format_clock_ampm(nowcast.get('message') or 'Live nowcast returned a district entry.')} · {issue}{valid}")
                if nowcast.get("source") == "RMC Guwahati district-wise nowcast":
                    st.caption("Source: [RMC Guwahati nowcast](https://mausam.imd.gov.in/imd_latest/contents/districtwisewarnings_mc.php?id=24)")
                else:
                    st.caption(f"Source: [IMD district nowcast map]({IMD_NOWCAST_MAP_URL})")
            elif nowcast.get("status") == "STALE":
                last_verified = freshness_label(nowcast.get("last_verified_at"), stale_after_minutes=15)
                message = nowcast.get("message") or "Last verified nowcast"
                st.warning(
                    f"STALE — last verified nowcast: {format_clock_ampm(message)}. "
                    f"{last_verified}; latest recheck failed."
                )
                st.caption(
                    f"{nowcast.get('recheck_error') or 'No current nowcast was verified.'} · "
                    f"[IMD nowcast map]({IMD_NOWCAST_MAP_URL})"
                )
            elif nowcast.get("status") == "EXPIRED":
                st.info(f"Expired · {nowcast_expiry_label(nowcast)}")
                recheck_note = f" · latest recheck failed: {nowcast['recheck_error']}" if nowcast.get("recheck_error") else ""
                st.caption(f"Source: [IMD district nowcast map]({IMD_NOWCAST_MAP_URL}){recheck_note}")
            else:
                st.caption(f"No current nowcast entry · {nowcast.get('reason') or 'IMD did not return a district record'} · [IMD nowcast map]({IMD_NOWCAST_MAP_URL})")
            cyclone = item.get("cyclone") or {}
            st.markdown("**Cyclone warning**")
            if cyclone.get("status") != "OK":
                if warnings.get("status") == "OK" and not any(
                    warning_mentions_cyclone(warning)
                    for warning in warnings.get("items", []) if isinstance(warning, dict)
                ):
                    st.caption("No cyclone warning listed in district feed")
                else:
                    st.caption(f"No cyclone status in current feed · {cyclone.get('reason') or warnings.get('reason') or 'no district cyclone entry'}")
            elif cyclone.get("overlaps"):
                if cyclone.get("source") == "RMC Guwahati district warning":
                    st.warning(f"RMC Guwahati has an explicit cyclone-related warning for this district · {cyclone.get('issue_date')}.")
                else:
                    st.warning(f"The live {cyclone.get('source', 'district warning feed')} includes a cyclone-related warning for this district.")
            else:
                st.caption("No cyclone warning listed · RMC Guwahati")
            lightning = item.get("lightning") or {}
            st.markdown("**Live lightning strike coordinates**")
            if lightning.get("status") == "OK":
                strikes = lightning.get("coordinates", [])
                if strikes:
                    st.caption(f"{len(strikes)} Bhuvan feed point(s) returned inside this district boundary.")
                    st.dataframe(strikes, hide_index=True, width="stretch")
                else:
                    st.caption("0 Bhuvan feed points returned inside this district boundary; this does not prove no lightning occurred.")
                st.caption(
                    f"Source: [NRSC–ISRO Bhuvan Lightning](https://bhuvan-app1.nrsc.gov.in/lightning/) · "
                    f"window {format_clock_ampm(lightning.get('window_start'))} to "
                    f"{format_clock_ampm(lightning.get('window_end'))} · "
                    f"DIWIS fetch: {freshness_label(item.get('fetched_at'))}"
                )
            else:
                st.caption(f"No coordinates returned · {lightning.get('error') or 'feed did not return district strike coordinates'} · [NRSC–ISRO Bhuvan](https://bhuvan-app1.nrsc.gov.in/lightning/)")
    assam_lightning_results = st.session_state.get("assam_lightning_results") or []
    if assam_lightning_results:
        st.divider()
        st.subheader("Bhuvan lightning feed · all Assam districts")
        st.caption(
            f"Query window: {st.session_state.get('assam_lightning_window') or {}} · "
            f"Bhuvan returned {st.session_state.get('assam_lightning_feed_count', 0)} point records "
            "across its queried feed; counts below are points inside each district polygon. "
            "Zero returned points is not proof that no lightning occurred."
        )
        unavailable_lightning = [
            row for row in assam_lightning_results if row.get("status") != "OK"
        ]
        if unavailable_lightning:
            st.warning(
                "The Bhuvan feed was unavailable; district counts are not reported. "
                + str(unavailable_lightning[0].get("error") or "No feed response.")
            )
        else:
            district_counts = []
            strike_rows = []
            for row in assam_lightning_results:
                strikes = row.get("coordinates") or []
                district_counts.append({
                    "District": row["district"],
                    "Feed points inside boundary": len(strikes),
                    "Result": (
                        f"{len(strikes)} point(s) returned"
                        if strikes else "No points returned inside boundary"
                    ),
                })
                for strike in strikes:
                    strike_rows.append({
                        "District": row["district"],
                        "Latitude": strike["latitude"],
                        "Longitude": strike["longitude"],
                        "Bhuvan source time": strike.get("source_time") or "Not supplied",
                        "Feed ID": strike.get("feed_id") or "Not supplied",
                        "Current": strike.get("current") or "Not supplied",
                        "Queried hour (UTC)": strike["hour_utc"],
                    })
            st.dataframe(district_counts, hide_index=True, width="stretch")
            if strike_rows:
                st.markdown("**Feed points inside Assam district boundaries**")
                st.dataframe(strike_rows, hide_index=True, width="stretch")
            else:
                st.caption(
                    "Bhuvan returned no points inside the 35 Assam district polygons "
                    "for this query window. This describes the feed response, not a "
                    "verified absence of lightning."
                )
    st.divider()
    st.subheader("Download report")
    st.caption("PDF: primary live data and selected district rainfall/forecasts.")
    if results or forecast_results:
        generated_at = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d %b %Y, %I:%M %p IST")
        generated_by = user.get("full_name") or user.get("username") or "Signed-in user"
        try:
            pdf_bytes = build_rainfall_report_pdf(results, forecast_results, generated_at, generated_by)
            report_filename = f"DIWIS_Live_District_Report_{datetime.now(ZoneInfo('Asia/Kolkata')).strftime('%Y%m%d_%I%M%p')}.pdf"
            st.download_button(
                "Download PDF report", data=pdf_bytes, file_name=report_filename,
                mime="application/pdf", type="primary", width="stretch",
            )
        except Exception as exc:
            st.error(f"Could not create the PDF report: {exc}")
    else:
        st.button("Download PDF report", disabled=True, width="stretch")


if page == "Dashboard":
    st.subheader("District dashboard")
    st.caption(f"Primary: {primary_district}, Assam · Comparison districts: {len(selected_pairs)}")
    render_live_dashboard(primary_district, selected_pairs)
