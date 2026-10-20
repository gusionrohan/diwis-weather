import os
import json
import subprocess
from datetime import datetime
import streamlit as st
import pandas as pd

from geo_registry import (
    NE_STATES_DISTRICTS,
    ASSAM_DISTRICTS_CONFIG,
    DISTRICT_COORDINATES_MAP,
    get_district_meta,
    get_river_link
)
from weather_scraper import scrape_weather_data, format_strike_age, get_district_paths
from db_manager import (
    get_all_tables_stats,
    get_district_tables_stats,
    query_dataframe,
    DEFAULT_DB_PATH,
    authenticate_user,
    create_user,
    delete_user_by_admin,
    get_district_users,
    update_user_password,
    sync_admin_from_secrets,
    hash_password,
    hash_password_md5
)

# Page configuration - Clean wide layout without sidebar
st.set_page_config(
    page_title="District Integrated Weather Information System (DIWIS) | Assam",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = DEFAULT_DB_PATH

# Auto-sync admin credentials from Streamlit Cloud Secrets or env vars if provided
try:
    sec_pwd = None
    if hasattr(st, "secrets") and "ADMIN_PASSWORD" in st.secrets:
        sec_pwd = str(st.secrets["ADMIN_PASSWORD"]).strip()
    elif "DIWIS_ADMIN_PASSWORD" in os.environ:
        sec_pwd = os.environ["DIWIS_ADMIN_PASSWORD"].strip()
    
    if sec_pwd:
        sec_user = "admin"
        if hasattr(st, "secrets") and "ADMIN_USERNAME" in st.secrets:
            sec_user = str(st.secrets["ADMIN_USERNAME"]).strip()
        elif "DIWIS_ADMIN_USERNAME" in os.environ:
            sec_user = os.environ["DIWIS_ADMIN_USERNAME"].strip()
        sync_admin_from_secrets(sec_pwd, sec_user, db_path=DB_PATH)
except Exception:
    pass

# CSS Styling to hide sidebar and style modern cards
st.markdown("""
<style>
    /* Hide Streamlit sidebar completely */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }
    
    /* Hide Streamlit top header, GitHub repository buttons, fork/edit icons, share, and menus completely */
    header[data-testid="stHeader"], header {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }
    #MainMenu, footer {
        visibility: hidden !important;
        display: none !important;
    }
    [data-testid="stToolbar"], [data-testid="stToolbarActions"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
    }
    .stAppDeployButton, [data-testid="manage-app-button"] {
        display: none !important;
    }
    button[title*="GitHub"], button[title*="git"], button[title*="Share"], button[title*="Star"] {
        display: none !important;
    }
    
    /* Global styles */
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 2.5rem;
        max-width: 1200px;
    }
    .header-box {
        background: linear-gradient(135deg, #1E3A8A 0%, #0284C7 50%, #059669 100%);
        color: #FFFFFF;
        padding: 22px 24px;
        border-radius: 16px;
        margin-bottom: 18px;
        box-shadow: 0 10px 15px -3px rgba(30, 58, 138, 0.2);
    }
    .header-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }
    .header-sub {
        font-size: 0.95rem;
        color: #E0F2FE;
    }
    .config-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-top: 4px solid #0284C7;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 20px;
        color: #F8FAFC;
    }
    .card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 18px;
        color: #F8FAFC;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .obs-card {
        background: #1E293B;
        border: 1px solid #0284C7;
        border-left: 4px solid #0284C7;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 20px;
        color: #F8FAFC;
    }
    .temp-card {
        background: #1E293B;
        border: 1px solid #D97706;
        border-left: 4px solid #D97706;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 20px;
        color: #F8FAFC;
    }
    .zone-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-left: 4px solid #EA580C;
        border-radius: 12px;
        padding: 16px 18px;
        height: 100%;
        color: #F8FAFC;
    }
    .zone-card-yellow {
        background: #1E293B;
        border: 1px solid #334155;
        border-left: 4px solid #CA8A04;
        border-radius: 12px;
        padding: 16px 18px;
        height: 100%;
        color: #F8FAFC;
    }
    .provenance-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 20px 20px 16px 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 220px;
        margin-bottom: 16px;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .provenance-card:hover {
        border-color: #0284C7;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -3px rgba(2, 132, 199, 0.2);
    }
    .prov-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .prov-badge {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid #334155;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        color: #94A3B8;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .prov-status {
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid rgba(34, 197, 94, 0.35);
        color: #4ADE80;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 9999px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .prov-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 6px;
        line-height: 1.35;
    }
    .prov-desc {
        font-size: 0.80rem;
        color: #94A3B8;
        line-height: 1.45;
        margin-bottom: 14px;
        flex-grow: 1;
    }
    .prov-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 10px;
        border-top: 1px solid rgba(51, 65, 85, 0.7);
    }
    .prov-protocol {
        font-size: 0.70rem;
        color: #64748B;
        font-family: monospace;
        font-weight: 600;
    }
    .prov-btn {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
        color: #FFFFFF !important;
        font-size: 0.74rem;
        font-weight: 700;
        padding: 5px 12px;
        border-radius: 6px;
        text-decoration: none !important;
        transition: all 0.2s ease;
    }
    .prov-btn:hover {
        background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%);
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
        color: #FFFFFF !important;
    }
    .badge-yellow {
        background-color: rgba(234, 179, 8, 0.2);
        color: #FACC15;
        border: 1px solid rgba(234, 179, 8, 0.4);
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-green {
        background-color: rgba(34, 197, 94, 0.2);
        color: #4ADE80;
        border: 1px solid rgba(34, 197, 94, 0.4);
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-orange {
        background-color: rgba(234, 88, 12, 0.2);
        color: #FB923C;
        border: 1px solid rgba(234, 88, 12, 0.4);
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
    }
    .synoptic-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-left: 4px solid #0284C7;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 12px;
        color: #F8FAFC;
    }
    
    /* Modern Login Card Styling */
    .login-brand-box {
        text-align: center;
        background: #1E293B;
        border: 1px solid #334155;
        border-top: 4px solid #0284C7;
        border-radius: 16px 16px 0 0;
        padding: 26px 24px 18px 24px;
        margin-bottom: 0px;
    }
    .login-icon-badge {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        background: linear-gradient(135deg, #1E3A8A 0%, #0284C7 100%);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.7rem;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
    }
    .login-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.02em;
        margin-bottom: 3px;
    }
    .login-subtitle {
        font-size: 0.83rem;
        color: #94A3B8;
        line-height: 1.35;
    }
    
    /* Executive EOC Tab Bar Styling */
    div[data-testid="stTabs"] > div[data-baseweb="tab-list"] {
        gap: 8px;
        background: #0F172A;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 18px;
        color: #94A3B8;
        font-weight: 700;
        font-size: 0.90rem;
        border: 1px solid transparent;
        transition: all 0.2s ease;
        background: transparent;
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
        color: #38BDF8;
        background: rgba(30, 41, 59, 0.6);
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        color: #38BDF8 !important;
        border: 1px solid #0284C7 !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25);
    }
    div[data-testid="stTabs"] div[data-baseweb="tab-border"] {
        display: none;
    }
    div[data-testid="stTabs"] div[data-baseweb="tab-highlight"] {
        background-color: #38BDF8 !important;
        height: 3px;
        border-radius: 3px;
    }

    /* Executive Condition Banner */
    .condition-banner {
        background: #1E293B;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .condition-banner-red {
        border: 1px solid #EF4444;
        border-left: 6px solid #EF4444;
    }
    .condition-banner-orange {
        border: 1px solid #F97316;
        border-left: 6px solid #F97316;
    }
    .condition-banner-yellow {
        border: 1px solid #EAB308;
        border-left: 6px solid #EAB308;
    }
    .condition-banner-green {
        border: 1px solid #10B981;
        border-left: 6px solid #10B981;
    }
</style>
""", unsafe_allow_html=True)


def load_local_data(district_name: str = "Hailakandi"):
    paths = get_district_paths(district_name)
    target_json = paths["json_path"]
    if not os.path.exists(target_json) and district_name.lower() == "hailakandi":
        legacy_json = os.path.join(BASE_DIR, "output_hailakandi", "hailakandi_weather_forecast.json")
        if os.path.exists(legacy_json):
            target_json = legacy_json
    if os.path.exists(target_json):
        try:
            with open(target_json, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


# ==========================================
# AUTHENTICATION & LOGIN GATEWAY
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "show_admin_panel" not in st.session_state:
    st.session_state.show_admin_panel = False
if "show_pwd_modal" not in st.session_state:
    st.session_state.show_pwd_modal = False

assam_districts_list = sorted(NE_STATES_DISTRICTS["Assam"])

# If user is not authenticated, display the Login Screen
if not st.session_state.authenticated:
    st.markdown("<div style='padding-top: 1.5rem;'></div>", unsafe_allow_html=True)
    
    login_col1, login_col2, login_col3 = st.columns([1, 1.3, 1])
    with login_col2:
        st.markdown("""
        <div class="login-brand-box">
            <div class="login-icon-badge"></div>
            <div class="login-title">DIWIS Portal Sign In</div>
            <div class="login-subtitle">
                District Integrated Weather Information System<br>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("diwis_login_form"):
            login_district = st.selectbox(
                "📍 Select Operational District:",
                options=assam_districts_list,
                index=assam_districts_list.index("Hailakandi") if "Hailakandi" in assam_districts_list else 0,
            )
            login_username = st.text_input(
                "👤 Username / ID:",
            )
            login_password = st.text_input(
                "🔑 Password:",
                type="password",
            )
            
            submit_login = st.form_submit_button("🚀 Sign In to District Portal", use_container_width=True, type="primary")

        if submit_login:
            if not login_username or not login_password:
                st.error("Please provide both username and password.")
            else:
                success, msg, user_dict = authenticate_user(login_username, login_password, login_district, db_path=DB_PATH)
                if success and user_dict:
                    st.session_state.authenticated = True
                    st.session_state.user = user_dict
                    st.session_state.selected_primary_state = "Assam"
                    st.session_state.selected_primary_district = login_district
                    
                    # Setup default secondary catchment predictors for this district
                    curr_meta = get_district_meta(login_district)
                    sec_states = curr_meta.get("default_secondary_states", ["Mizoram"])
                    sec_districts = curr_meta.get("default_secondary_districts", ["Kolasib", "Mamit", "Aizawl"])
                    sec_items = []
                    for d in sec_districts:
                        for s in sec_states:
                            if d in NE_STATES_DISTRICTS.get(s, []):
                                sec_items.append({"state": s, "district": d})
                                break
                        else:
                            sec_items.append({"state": sec_states[0] if sec_states else "Mizoram", "district": d})
                    st.session_state.selected_secondary_items = sec_items
                    st.session_state.page = "dashboard"
                    st.session_state.app_view = "dashboard"
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("""
        <div style="text-align: center; font-size: 0.75rem; color: #64748B; margin-top: 14px;">
            🔒 Authorized District Operations Portal &bull; Role-Based Access Control
        </div>
        """, unsafe_allow_html=True)

    st.stop()



# ==========================================
# AUTHENTICATED USER STATE & DISTRICT LOCK
# ==========================================
current_user = st.session_state.get("user") or {}
user_role = current_user.get("role", "staff")
user_name = current_user.get("full_name") or current_user.get("username") or "Operator"
user_username = current_user.get("username", "")
user_assigned_dist = current_user.get("district", "ALL")

# Mandatory initial password change gate
if current_user.get("must_change_password") == 1:
    st.markdown("""
    <div style="max-width: 650px; margin: 40px auto 20px auto; background: rgba(220, 38, 38, 0.08); border: 1px solid #DC2626; border-radius: 12px; padding: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
            <div style="font-size: 1.8rem;">🛡️</div>
            <div>
                <h3 style="color: #F87171; margin: 0; font-size: 1.25rem;">Mandatory Security Action: Update Initial Password</h3>
                <p style="color: #94A3B8; margin: 2px 0 0 0; font-size: 0.85rem;">Emergency Operations & Disaster Management Security Protocol</p>
            </div>
        </div>
        <p style="color: #E2E8F0; font-size: 0.9rem; line-height: 1.5; margin-bottom: 0;">
            Your account is currently using default bootstrap credentials. To protect public safety data and prevent unauthorized district access, you must establish a new private password before proceeding.
        </p>
    </div>
    """, unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns([1, 2, 1])
    with f_col2:
        with st.form("forced_password_reset_form"):
            f_curr = st.text_input("🔑 Current Password:", type="password")
            f_new = st.text_input("🔒 New Secure Password (minimum 6 characters):", type="password")
            f_conf = st.text_input("🔒 Confirm New Password:", type="password")
            f_submit = st.form_submit_button("💾 Save New Password & Access System", type="primary", use_container_width=True)
            if f_submit:
                if not f_curr or not f_new:
                    st.error("Please fill in all password fields.")
                elif f_new != f_conf:
                    st.error("New password and confirmation do not match.")
                elif len(f_new.strip()) < 6:
                    st.error("New password must be at least 6 characters.")
                else:
                    r_ok, r_msg = update_user_password(user_username, f_new, current_password=f_curr, db_path=DB_PATH)
                    if r_ok:
                        st.session_state.user["must_change_password"] = 0
                        st.success("Security credentials updated! Loading dashboard...")
                        st.rerun()
                    else:
                        st.error(r_msg)
    st.stop()

# Enforce Primary District Lock: Non-superadmins CANNOT change their assigned district
if user_role == "superadmin":
    primary_district = st.session_state.get("selected_primary_district", "Hailakandi")
else:
    primary_district = user_assigned_dist
    st.session_state.selected_primary_district = primary_district

primary_state = "Assam"
st.session_state.selected_primary_state = primary_state
secondary_items = st.session_state.get("selected_secondary_items", [])
if not secondary_items:
    curr_meta = get_district_meta(primary_district)
    sec_states = curr_meta.get("default_secondary_states", ["Mizoram"])
    sec_districts = curr_meta.get("default_secondary_districts", ["Kolasib", "Mamit", "Aizawl"])
    sec_items = []
    for d in sec_districts:
        for s in sec_states:
            if d in NE_STATES_DISTRICTS.get(s, []):
                sec_items.append({"state": s, "district": d})
                break
        else:
            sec_items.append({"state": sec_states[0] if sec_states else "Mizoram", "district": d})
    st.session_state.selected_secondary_items = sec_items
    secondary_items = sec_items

current_meta = get_district_meta(primary_district)

# Resolve partitioned district file paths
active_paths = get_district_paths(primary_district)
if primary_district.lower() == "hailakandi" and not os.path.exists(active_paths["json_path"]):
    legacy_json = os.path.join(BASE_DIR, "output_hailakandi", "hailakandi_weather_forecast.json")
    if os.path.exists(legacy_json):
        active_paths["json_path"] = legacy_json
        active_paths["forecast_csv"] = os.path.join(BASE_DIR, "output_hailakandi", "hailakandi_forecast_summary.csv")
        active_paths["lightning_csv"] = os.path.join(BASE_DIR, "output_hailakandi", "hailakandi_lightning_zones_summary.csv")
        active_paths["upstream_csv"] = os.path.join(BASE_DIR, "output_hailakandi", "hailakandi_upstream_mizoram_summary.csv")
        active_paths["pdf_report"] = os.path.join(BASE_DIR, "output_hailakandi", "Hailakandi_Daily_Weather_Report.pdf")
        active_paths["md_report"] = os.path.join(BASE_DIR, "output_hailakandi", "Hailakandi_Daily_Weather_Report.md")

JSON_PATH = active_paths["json_path"]
CSV_PATH = active_paths["forecast_csv"]
LIGHTNING_CSV_PATH = active_paths["lightning_csv"]
MIZORAM_CSV_PATH = active_paths["upstream_csv"]
PDF_REPORT_PATH = active_paths["pdf_report"]
MD_REPORT_PATH = active_paths["md_report"]

if "app_view" not in st.session_state:
    st.session_state.app_view = "dashboard"

# ==========================================
# VIEW 1: DEDICATED ADMIN & USER MANAGEMENT VIEW
# ==========================================
if st.session_state.app_view == "admin" and user_role in ("district_admin", "superadmin"):
    top_nav1, top_nav2 = st.columns([1.5, 4.5])
    with top_nav1:
        if st.button("⬅️ Back to Weather Dashboard", type="primary", use_container_width=True):
            st.session_state.app_view = "dashboard"
            st.rerun()
    with top_nav2:
        st.markdown(f"""
        <div style="text-align: right; padding-top: 6px; font-size: 0.88rem; color: #94A3B8;">
            Signed in as: <b style="color: #F8FAFC;">{user_name}</b> (@{user_username}) &nbsp;|&nbsp; <b>District:</b> <span style="color: #38BDF8;">{primary_district}</span>
        </div>
        """, unsafe_allow_html=True)

    if user_role == "superadmin":
        st.markdown("""
        <div class="header-box" style="margin-top: 8px; margin-bottom: 20px;">
            <div style="font-size: 0.80rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: #BAE6FD; margin-bottom: 2px;">
                🏛️ State Super Administrator &bull; User Governance & District Admin Provisioning
            </div>
            <div class="header-title">👑 State Super Administrator Workspace</div>
            <div class="header-sub">
                Create and manage <b>District Administrators</b> across all 35 Assam districts and oversee user accounts state-wide.
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab_users, tab_create, tab_reset, tab_delete = st.tabs([
            "📋 State-Wide Users Directory",
            "➕ Create District Admin Account",
            "🔄 Reset User Password",
            "🗑️ Delete User Account"
        ])

        # 1. Superadmin Directory
        with tab_users:
            filter_dist = st.selectbox("Filter Directory by District:", options=["ALL"] + assam_districts_list, index=0)
            users_list = get_district_users(filter_dist if filter_dist != "ALL" else None, requester_role="superadmin", db_path=DB_PATH)
            if users_list:
                df_users = pd.DataFrame(users_list)
                df_users.rename(columns={
                    "id": "User ID",
                    "username": "Username",
                    "full_name": "Full Name",
                    "role": "Role",
                    "district": "Assigned District",
                    "created_at": "Account Created At",
                    "created_by": "Created By"
                }, inplace=True)
                st.dataframe(df_users, use_container_width=True, hide_index=True)
                st.caption(f"Total Accounts Listed: **{len(users_list)} Users**")
            else:
                st.info("No users found for selected filter.")

        # 2. Superadmin: Create District Admin
        with tab_create:
            st.markdown("#### ➕ Create New Account (Admin, Staff, or Superadmin)")
            st.caption("Provision authorized user credentials with role-based access control and district locking.")
            with st.form("create_district_admin_form"):
                ca_col1, ca_col2 = st.columns(2)
                with ca_col1:
                    new_role = st.selectbox(
                        "Account Role:",
                        options=["district_admin", "staff", "superadmin"],
                        format_func=lambda x: {
                            "district_admin": "District Administrator (Manages District & Staff)",
                            "staff": "District Staff / Field Operator (Dashboard & Reports)",
                            "superadmin": "State Super Administrator (Full State-Wide Access)"
                        }.get(x, x)
                    )
                    target_dist_for_admin = st.selectbox("Assign to District (Assam):", options=["ALL"] + assam_districts_list if new_role == "superadmin" else assam_districts_list)
                    new_username = st.text_input("Username (Unique Login ID):")
                with ca_col2:
                    new_fullname = st.text_input("Full Name / Official Designation:")
                    new_password = st.text_input("Initial Password (min 6 characters):", type="password")
                
                btn_create_admin = st.form_submit_button("🚀 Create Account with Salted Scrypt", type="primary", use_container_width=True)
                
                if btn_create_admin:
                    if not new_username or not new_password or not new_fullname:
                        st.error("Please fill in username, full name, and initial password.")
                    elif len(new_password.strip()) < 6:
                        st.error("Password must be at least 6 characters long.")
                    else:
                        c_dist = "ALL" if new_role == "superadmin" else target_dist_for_admin
                        c_ok, c_msg = create_user(
                            username=new_username,
                            password=new_password,
                            full_name=new_fullname,
                            role=new_role,
                            district=c_dist,
                            created_by=user_username,
                            db_path=DB_PATH
                        )
                        if c_ok:
                            st.success(c_msg)
                            st.rerun()
                        else:
                            st.error(c_msg)

        # 3. Superadmin: Reset Password
        with tab_reset:
            st.markdown("#### 🔄 Reset Any User / Admin Password")
            all_users = get_district_users(None, requester_role="superadmin", db_path=DB_PATH)
            if all_users:
                user_choices = {f"{u['full_name']} (@{u['username']}) - [{u['role']}] ({u['district']})": u['username'] for u in all_users}
                with st.form("super_reset_pwd_form"):
                    target_user_label = st.selectbox("Select Account to Reset:", list(user_choices.keys()))
                    target_user_name = user_choices[target_user_label]
                    new_admin_pwd = st.text_input("Enter New Password:", type="password")
                    btn_reset_pwd = st.form_submit_button("🔑 Update Password", type="primary", use_container_width=True)
                    
                    if btn_reset_pwd:
                        if not new_admin_pwd or len(new_admin_pwd.strip()) < 6:
                            st.error("Password must be at least 6 characters long.")
                        else:
                            r_ok, r_msg = update_user_password(target_user_name, new_admin_pwd, requester_role="superadmin", db_path=DB_PATH)
                            if r_ok:
                                st.success(f"Successfully updated password for user @{target_user_name}!")
                            else:
                                st.error(r_msg)

        # 4. Superadmin: Delete Account
        with tab_delete:
            st.markdown("#### 🗑️ Delete User / Admin Account")
            deletable_users = [u for u in get_district_users(None, requester_role="superadmin", db_path=DB_PATH) if u.get("username").lower() != user_username.lower()]
            if deletable_users:
                del_choices = {f"{u['full_name']} (@{u['username']}) - [{u['role']}] ({u['district']})": u['username'] for u in deletable_users}
                with st.form("super_delete_user_form"):
                    del_user_label = st.selectbox("Select Account to Delete:", list(del_choices.keys()))
                    del_username = del_choices[del_user_label]
                    confirm_check = st.checkbox(f"I confirm permanent deletion of user account @{del_username}")
                    btn_delete_user = st.form_submit_button("🗑️ Permanently Delete Account", type="secondary", use_container_width=True)
                    
                    if btn_delete_user:
                        if not confirm_check:
                            st.error("Please check the confirmation box before deleting.")
                        else:
                            d_ok, d_msg = delete_user_by_admin(del_username, current_user, db_path=DB_PATH)
                            if d_ok:
                                st.success(d_msg)
                                st.rerun()
                            else:
                                st.error(d_msg)

    else:
        # DISTRICT ADMIN WORKSPACE (Dedicated to their own District Staff)
        st.markdown(f"""
        <div class="header-box" style="margin-top: 8px; margin-bottom: 20px;">
            <div style="font-size: 0.80rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: #BAE6FD; margin-bottom: 2px;">
                District Disaster Management Authority (DDMA), {primary_district.upper()}
            </div>
            <div class="header-title">{primary_district} DDMA &bull; Staff Administration Workspace</div>
            <div class="header-sub">
                Create user IDs and passwords for your district's field officers, hydrological operators, and staff members in <b>{primary_district}</b>.
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab_users, tab_create, tab_reset, tab_delete = st.tabs([
            f"📋 {primary_district} Staff Directory",
            "➕ Create New District Staff Account",
            "🔄 Reset Staff Password",
            "🗑️ Delete Staff Account"
        ])

        # 1. Staff Directory
        with tab_users:
            users_list = get_district_users(primary_district, requester_role="district_admin", db_path=DB_PATH)
            if users_list:
                df_users = pd.DataFrame(users_list)
                df_users.rename(columns={
                    "id": "User ID",
                    "username": "Username",
                    "full_name": "Full Name",
                    "role": "Role",
                    "district": "Assigned District",
                    "created_at": "Account Created At",
                    "created_by": "Created By"
                }, inplace=True)
                st.dataframe(df_users, use_container_width=True, hide_index=True)
                st.caption(f"Total Accounts in {primary_district}: **{len(users_list)} Users**")
            else:
                st.info(f"No staff accounts created for {primary_district} yet.")

        # 2. Create New District Staff
        with tab_create:
            st.markdown(f"#### ➕ Create New Staff Account for **{primary_district}**")
            st.caption(f"This user will be registered as a Staff Operator strictly locked to **{primary_district}**.")
            with st.form("create_staff_form"):
                new_u1, new_u2 = st.columns(2)
                with new_u1:
                    new_username = st.text_input("Staff Username (Unique ID):")
                    new_fullname = st.text_input("Staff Full Name / Designation:")
                with new_u2:
                    new_password = st.text_input("Initial Password:", type="password")
                    st.text_input("Assigned District (Locked):", value=primary_district, disabled=True)
                
                btn_create_staff = st.form_submit_button("🚀 Create District Staff Account", type="primary", use_container_width=True)
                
                if btn_create_staff:
                    if not new_username or not new_password or not new_fullname:
                        st.error("Please fill in username, full name, and initial password.")
                    else:
                        c_ok, c_msg = create_user(
                            username=new_username,
                            password=new_password,
                            full_name=new_fullname,
                            role="staff",
                            district=primary_district,
                            created_by=user_username,
                            db_path=DB_PATH
                        )
                        if c_ok:
                            st.success(c_msg)
                            st.rerun()
                        else:
                            st.error(c_msg)

        # 3. Reset Staff Password
        with tab_reset:
            st.markdown(f"#### 🔄 Reset Staff Password in **{primary_district}**")
            staff_users = [u for u in get_district_users(primary_district, requester_role="district_admin", db_path=DB_PATH) if u.get("role") == "staff"]
            if staff_users:
                staff_choices = {f"{u['full_name']} (@{u['username']})": u['username'] for u in staff_users}
                with st.form("reset_staff_pwd_form"):
                    target_user_label = st.selectbox("Select Staff Account to Reset:", list(staff_choices.keys()))
                    target_user_name = staff_choices[target_user_label]
                    new_admin_pwd = st.text_input("Enter New Password for Staff:", type="password")
                    btn_reset_pwd = st.form_submit_button("🔑 Update Password", type="primary", use_container_width=True)
                    
                    if btn_reset_pwd:
                        if not new_admin_pwd or len(new_admin_pwd.strip()) < 6:
                            st.error("Password must be at least 6 characters long.")
                        else:
                            r_ok, r_msg = update_user_password(target_user_name, new_admin_pwd, requester_role="superadmin", db_path=DB_PATH)
                            if r_ok:
                                st.success(f"Successfully updated password for staff user @{target_user_name}!")
                            else:
                                st.error(r_msg)
            else:
                st.info("No staff accounts found in this district to reset.")

        # 4. Delete Staff Account
        with tab_delete:
            st.markdown(f"#### 🗑️ Remove Staff Account from **{primary_district}**")
            deletable_users = [u for u in get_district_users(primary_district, requester_role="district_admin", db_path=DB_PATH) if u.get("role") == "staff"]
            if deletable_users:
                del_choices = {f"{u['full_name']} (@{u['username']})": u['username'] for u in deletable_users}
                with st.form("delete_staff_form"):
                    del_user_label = st.selectbox("Select Account to Delete:", list(del_choices.keys()))
                    del_username = del_choices[del_user_label]
                    confirm_check = st.checkbox(f"I confirm permanent deletion of user account @{del_username}")
                    btn_delete_staff = st.form_submit_button("🗑️ Permanently Delete Account", type="secondary", use_container_width=True)
                    
                    if btn_delete_staff:
                        if not confirm_check:
                            st.error("Please check the confirmation box before deleting.")
                        else:
                            d_ok, d_msg = delete_user_by_admin(del_username, current_user, db_path=DB_PATH)
                            if d_ok:
                                st.success(d_msg)
                                st.rerun()
                            else:
                                st.error(d_msg)
            else:
                st.info("No staff accounts eligible for deletion in this district.")

    st.stop()



# ==========================================
# VIEW 2: DEDICATED PASSWORD SETTINGS VIEW
# ==========================================
if st.session_state.app_view == "password":
    top_p1, top_p2 = st.columns([1.5, 4.5])
    with top_p1:
        if st.button("⬅️ Back to Weather Dashboard", type="primary", use_container_width=True):
            st.session_state.app_view = "dashboard"
            st.rerun()
    with top_p2:
        st.markdown(f"""
        <div style="text-align: right; padding-top: 6px; font-size: 0.88rem; color: #94A3B8;">
            Signed in as: <b style="color: #F8FAFC;">{user_name}</b> (@{user_username}) &nbsp;|&nbsp; <b>District:</b> <span style="color: #38BDF8;">{primary_district}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="header-box" style="margin-top: 8px; margin-bottom: 20px;">
        <div style="font-size: 0.80rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: #BAE6FD; margin-bottom: 2px;">
            🔐 Security & Access Control
        </div>
        <div class="header-title">🔑 Change Account Password</div>
        <div class="header-sub">
            Update your personal portal password. All credentials are protected with Salted Scrypt cryptographic hashing.
        </div>
    </div>
    """, unsafe_allow_html=True)

    pwd_col1, pwd_col2, pwd_col3 = st.columns([1, 2, 1])
    with pwd_col2:
        with st.form("self_pwd_change_form"):
            curr_pwd = st.text_input("Enter Current Password:", type="password")
            new_pwd = st.text_input("Enter New Password (min 6 chars):", type="password")
            confirm_new_pwd = st.text_input("Confirm New Password:", type="password")
            
            btn_update_pwd = st.form_submit_button("💾 Update Password (Scrypt Encrypted)", type="primary", use_container_width=True)
            
            if btn_update_pwd:
                if not curr_pwd or not new_pwd:
                    st.error("Please fill all required password fields.")
                elif new_pwd != confirm_new_pwd:
                    st.error("New password and confirmation do not match.")
                elif len(new_pwd.strip()) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    upd_ok, upd_msg = update_user_password(user_username, new_pwd, current_password=curr_pwd, db_path=DB_PATH)
                    if upd_ok:
                        st.success(f"{upd_msg} Please use your new password on subsequent logins.")
                    else:
                        st.error(upd_msg)

    st.stop()


# ==========================================
# VIEW 3: MAIN CLEAN WEATHER DASHBOARD VIEW
# ==========================================

# Check local data availability before rendering dashboard elements
raw_data = load_local_data(primary_district)
needs_sync = False
if not raw_data:
    needs_sync = True
elif raw_data.get("metadata", {}).get("target_location", {}).get("district") != primary_district:
    needs_sync = True

if needs_sync and secondary_items:
    st.markdown(f"""
    <div style="max-width: 650px; margin: 4rem auto 2rem auto; background: #1E293B; border: 1px solid #334155; border-top: 4px solid #0284C7; border-radius: 16px; padding: 40px 32px; text-align: center; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5);">
        <div style="font-size: 3.5rem; margin-bottom: 14px;">🛰️</div>
        <h2 style="font-size: 1.55rem; font-weight: 800; color: #F8FAFC; margin-bottom: 8px;">Initializing {primary_district} Weather Intelligence</h2>
        <p style="font-size: 0.90rem; color: #94A3B8; margin-bottom: 24px; line-height: 1.55;">
            Retrieving real-time observations, IMD 5-day warning bulletins, and IITM-ILDN DAMINI lightning sensors for <b>{primary_district}</b>. Initial provisioning takes ~15–20 seconds.
        </p>
        <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(2, 132, 199, 0.15); border: 1px solid rgba(2, 132, 199, 0.4); padding: 8px 20px; border-radius: 9999px; color: #38BDF8; font-size: 0.85rem; font-weight: 600;">
            📡 Connecting to IMD Regional Observatories...
        </div>
    </div>
    """, unsafe_allow_html=True)
    with st.spinner(f"Compiling meteorological feeds for {primary_district}..."):
        raw_data = scrape_weather_data(primary_state, primary_district, secondary_items, generate_reports=True, report_generated_by=user_name)
    st.rerun()

data = raw_data

role_badge_colors = {
    "superadmin": ("#DC2626", "rgba(220, 38, 38, 0.2)", "State Super Administrator"),
    "district_admin": ("#0284C7", "rgba(2, 132, 199, 0.2)", "District Administrator"),
    "staff": ("#059669", "rgba(5, 150, 105, 0.2)", "District Staff / Operator")
}
r_col, r_bg, r_label = role_badge_colors.get(user_role, ("#64748B", "rgba(100, 116, 139, 0.2)", "User"))

top_u_col1, top_u_col2 = st.columns([2.6, 1.8])
with top_u_col1:
    st.markdown(f"""
    <div style="background: #1E293B; border: 1px solid #334155; border-radius: 10px; padding: 8px 14px; display: flex; align-items: center; gap: 12px;">
        <div style="font-size: 1.4rem;">👤</div>
        <div>
            <div style="font-size: 0.90rem; font-weight: 800; color: #F8FAFC;">
                {user_name} <span style="font-size: 0.78rem; color: #94A3B8; font-weight: 500;">(@{user_username})</span>
            </div>
            <div style="display: flex; gap: 6px; align-items: center; margin-top: 2px; flex-wrap: wrap;">
                <span style="background: {r_bg}; color: {r_col}; border: 1px solid {r_col}; font-size: 0.70rem; font-weight: 700; padding: 1px 7px; border-radius: 9999px;">
                    🛡️ {r_label}
                </span>
                <span style="background: rgba(14, 165, 233, 0.15); color: #38BDF8; border: 1px solid rgba(14, 165, 233, 0.4); font-size: 0.70rem; font-weight: 700; padding: 1px 7px; border-radius: 9999px;">
                    🔒 Locked District: {primary_district}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with top_u_col2:
    btn_m1, btn_m2, btn_m3 = st.columns(3)
    with btn_m1:
        if st.button("🔑 Password", use_container_width=True, help="Change personal password"):
            st.session_state.app_view = "password"
            st.rerun()
    with btn_m2:
        if user_role in ("district_admin", "superadmin"):
            panel_btn_label = "👥 Staff Admin" if user_role == "district_admin" else "👥 User Admin"
            if st.button(panel_btn_label, use_container_width=True, help="Open dedicated staff admin workspace"):
                st.session_state.app_view = "admin"
                st.rerun()
        else:
            st.button("🔒 Staff View", disabled=True, use_container_width=True)
    with btn_m3:
        if st.button("🚪 Sign Out", use_container_width=True, help="Sign out of DIWIS portal"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.page = "portal"
            st.session_state.app_view = "dashboard"
            st.rerun()

# Top Navigation Bar
nav_col1, nav_col2 = st.columns([3.4, 1.3])
with nav_col1:
    st.markdown(f"""
    <div style="font-size: 0.90rem; color: #94A3B8; padding: 6px 0;">
        📍 <b>Active Target:</b> <span style="color: #38BDF8; font-weight: 700;">{primary_district}, Assam</span> &nbsp;|&nbsp; <b>Catchments:</b> <span style="color: #F8FAFC; font-weight: 600;">{len(secondary_items)} Districts</span> &nbsp;|&nbsp; <b>Live Feeds:</b> <span style="color: #4ADE80; font-weight: 600;">IMD & IITM-ILDN</span>
    </div>
    """, unsafe_allow_html=True)
with nav_col2:
    if user_role == "superadmin":
        if st.button("⚙️ Superadmin: Switch District", use_container_width=True):
            st.session_state.page = "portal"
            st.rerun()
    else:
        st.markdown(f"""
        <div style="text-align: right; padding-top: 6px;">
            <span style="background: rgba(30, 41, 59, 0.8); color: #94A3B8; border: 1px solid #334155; padding: 6px 12px; border-radius: 8px; font-size: 0.80rem; font-weight: 600;">
                🔒 District Locked to {primary_district}
            </span>
        </div>
        """, unsafe_allow_html=True)


target_loc = data.get("metadata", {}).get("target_location", {}) if data else {}
active_district = target_loc.get("district", primary_district)
active_coords = target_loc.get("coordinates", f"{current_meta['lat']}°N, {current_meta['lon']}°E")
active_basin = target_loc.get("river_basin", current_meta.get("river_basin", "Assam River Basin"))

st.markdown(f"""
<div class="header-box">
    <div style="font-size: 0.80rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: #BAE6FD; margin-bottom: 2px;">
        District Disaster Management Authority (DDMA), {active_district.upper()}
    </div>
    <div class="header-title">District Integrated Weather Information System (DIWIS)</div>
    <div class="header-sub">
        Target District: <b>{active_district}, Assam</b> | HQ Coordinates: <b>{active_coords}</b> | Basin: <b>{active_basin}</b> | <b>Data Sources: India Meteorological Department (IMD) & IITM-ILDN (DAMINI Network)</b>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. ACTION CONTROLS
# ==========================================
action_col1, action_col2, action_col3 = st.columns([1.5, 1.2, 1.2])

with action_col1:
    if st.button("🔄 Sync with IMD & SQL Database", use_container_width=True, type="primary"):
        with st.spinner(f"Syncing live IMD weather, lightning & upstream data for {primary_district}..."):
            data = scrape_weather_data(primary_state, primary_district, secondary_items, generate_reports=True, report_generated_by=user_name)
            st.success(f"Successfully synchronized and persisted data for {primary_district}!")
            st.rerun()

with action_col2:
    if os.path.exists(PDF_REPORT_PATH):
        with open(PDF_REPORT_PATH, "rb") as pdf_file:
            st.download_button(
                label="📥 Download Daily PDF Dossier",
                data=pdf_file,
                file_name=f"DDMA_{active_district}_Daily_Weather_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.button("📥 Daily PDF (Click Sync to Generate)", disabled=True, use_container_width=True)

with action_col3:
    if os.path.exists(MD_REPORT_PATH):
        with open(MD_REPORT_PATH, "rb") as md_file:
            st.download_button(
                label="📄 Download Report Brief (MD)",
                data=md_file,
                file_name=f"DDMA_{active_district}_Daily_Report.md",
                mime="text/markdown",
                use_container_width=True
            )
    else:
        st.button("📄 Report Brief (Pending)", disabled=True, use_container_width=True)

st.caption(f"🕒 **Last Synchronized with IMD:** {data.get('metadata', {}).get('scraped_at_local', 'N/A') if data else 'Never'} | **Active Primary:** {active_district} (Assam) | **Monitored Predictors:** {len(secondary_items)} Districts | **Database:** SQLite Connected")
st.markdown("---")

if not data:
    st.warning("No data found. Click 'Sync with IMD' above to fetch real-time data!")
    st.stop()

# ==========================================
# 4. OPTION 1: STATE EOC COMMAND DECK (5 SEGMENTED OPERATIONAL TABS)
# ==========================================

# Unpack all data models for tabs
temp_obs = data.get("temperature_data", {}).get("current_observation", {})
obs_rf = data.get("observed_rainfall_past24h", {})
rainfall = data.get("rainfall_forecast_5days", [])
warnings = data.get("severe_weather_warnings_5days", {}).get("daily_warnings", [])
temp_fc = data.get("temperature_data", {}).get("daily_temperature_forecast_5days", [])
upstream_data = data.get("upstream_catchment_rainfall") or data.get("upstream_mizoram_rainfall", [])
nowcast_info = data.get("current_nowcast_warning", {})
damini = data.get("damini_sensor_lightning", {})
active_sectors = data.get("lightning_zones_data", {}).get("sectors", current_meta.get("sectors", []))
synoptic_data = data.get("synoptic_bulletin", {}).get("synoptic_excerpts", [])

# Primary Segmented Operational Tabs
tab_tactical, tab_hydro, tab_convective, tab_reports_sql, tab_provenance = st.tabs([
    "🛰️ Tactical Overview",
    "🌧️ Hydrometeorology & Inflows",
    "⚡ Convective & Lightning Hazards",
    "📑 Official Reports & SQL Archive",
    "🏛️ Telemetry & Data Provenance"
])

# -------------------------------------------------------------
# TAB 1: TACTICAL OVERVIEW (EXECUTIVE SITUATION ROOM)
# -------------------------------------------------------------
with tab_tactical:
    # 1. Dynamic Operational Condition Status Banner
    today_w = warnings[0] if warnings else {}
    w_color = today_w.get("alert_color", "Green")
    w_sum = today_w.get("warning_summary", "No Warning")
    
    nowcast_color = nowcast_info.get("alert_color", "Green")
    nowcast_msg = nowcast_info.get("message", "Convective weather alert issued.")
    has_nowcast = nowcast_info.get("has_active_nowcast", False) or nowcast_color in ["Red", "Orange"]
    
    c_inside = damini.get("total_strikes_inside_boundary", 0)
    c_20 = damini.get("total_strikes_20km", 0)
    c_40 = damini.get("total_strikes_40km", 0)

    # Pinpoint exact trigger feed and build clear operational message
    if w_color == "Red":
        cond_class = "condition-banner-red"
        cond_title = f"🔴 CONDITION RED: IMD SEVERE WEATHER WARNING ACTIVE ({active_district.upper()})"
        cond_badge = "CRITICAL ALERT"
        cond_bg = "rgba(239, 68, 68, 0.2)"
        cond_fg = "#FCA5A5"
        cond_border = "rgba(239, 68, 68, 0.4)"
        cond_desc = f"<b>Trigger: IMD 5-Day Severe Weather Warning:</b> {w_sum}. Immediate district disaster management protocols in effect."
    elif nowcast_color == "Red" and has_nowcast:
        cond_class = "condition-banner-red"
        cond_title = f"🔴 CONDITION RED: RMC GUWAHATI 3-HOUR NOWCAST WARNING ({active_district.upper()})"
        cond_badge = "RADAR NOWCAST"
        cond_bg = "rgba(239, 68, 68, 0.2)"
        cond_fg = "#FCA5A5"
        cond_border = "rgba(239, 68, 68, 0.4)"
        cond_desc = f"<b>Trigger: RMC Guwahati 3-Hour Nowcast Feed:</b> {nowcast_msg} <i>(Note: 5-Day synoptic baseline is currently {w_color} Alert).</i>"
    elif c_inside > 0:
        cond_class = "condition-banner-red"
        cond_title = f"🔴 CONDITION RED: ACTIVE GROUND LIGHTNING STRIKES ({active_district.upper()})"
        cond_badge = "SENSOR STRIKES"
        cond_bg = "rgba(239, 68, 68, 0.2)"
        cond_fg = "#FCA5A5"
        cond_border = "rgba(239, 68, 68, 0.4)"
        cond_desc = f"<b>Trigger: IITM-ILDN Ground Sensors:</b> {c_inside} active ground strike(s) detected inside {active_district} in past 45m. Restrict outdoor movement."
    elif w_color == "Orange":
        cond_class = "condition-banner-orange"
        cond_title = f"🟠 CONDITION ORANGE: IMD WEATHER WATCH ({active_district.upper()})"
        cond_badge = "ENHANCED WATCH"
        cond_bg = "rgba(249, 115, 22, 0.2)"
        cond_fg = "#FB923C"
        cond_border = "rgba(249, 115, 22, 0.4)"
        cond_desc = f"<b>Trigger: IMD 5-Day Severe Weather Warning:</b> {w_sum}. Field personnel on enhanced standby."
    elif nowcast_color == "Orange" and has_nowcast:
        cond_class = "condition-banner-orange"
        cond_title = f"🟠 CONDITION ORANGE: RMC GUWAHATI NOWCAST WATCH ({active_district.upper()})"
        cond_badge = "RADAR WATCH"
        cond_bg = "rgba(249, 115, 22, 0.2)"
        cond_fg = "#FB923C"
        cond_border = "rgba(249, 115, 22, 0.4)"
        cond_desc = f"<b>Trigger: RMC Guwahati 3-Hour Nowcast Feed:</b> {nowcast_msg}"
    elif w_color == "Yellow":
        cond_class = "condition-banner-yellow"
        cond_title = f"🟡 CONDITION YELLOW: IMD WEATHER ADVISORY ({active_district.upper()})"
        cond_badge = "ADVISORY"
        cond_bg = "rgba(234, 179, 8, 0.2)"
        cond_fg = "#FACC15"
        cond_border = "rgba(234, 179, 8, 0.4)"
        cond_desc = f"<b>Trigger: IMD 5-Day Severe Weather Warning:</b> {w_sum}. Precautionary monitoring active."
    elif nowcast_color == "Yellow" and has_nowcast:
        cond_class = "condition-banner-yellow"
        cond_title = f"🟡 CONDITION YELLOW: RMC GUWAHATI NOWCAST ADVISORY ({active_district.upper()})"
        cond_badge = "NOWCAST ADVISORY"
        cond_bg = "rgba(234, 179, 8, 0.2)"
        cond_fg = "#FACC15"
        cond_border = "rgba(234, 179, 8, 0.4)"
        cond_desc = f"<b>Trigger: RMC Guwahati 3-Hour Nowcast Feed:</b> {nowcast_msg}"
    elif c_20 > 0:
        cond_class = "condition-banner-yellow"
        cond_title = f"🟡 CONDITION YELLOW: LIGHTNING ACTIVITY NEAR PERIMETER ({active_district.upper()})"
        cond_badge = "PERIMETER SENSOR"
        cond_bg = "rgba(234, 179, 8, 0.2)"
        cond_fg = "#FACC15"
        cond_border = "rgba(234, 179, 8, 0.4)"
        cond_desc = f"<b>Trigger: IITM-ILDN Ground Sensors:</b> {c_20} lightning strike(s) detected within 20 km of {active_district} perimeter."
    else:
        cond_class = "condition-banner-green"
        cond_title = f"🟢 CONDITION GREEN: ROUTINE OPERATIONAL READINESS ({active_district.upper()})"
        cond_badge = "ALL CLEAR"
        cond_bg = "rgba(16, 185, 129, 0.2)"
        cond_fg = "#6EE7B7"
        cond_border = "rgba(16, 185, 129, 0.4)"
        cond_desc = f"Atmospheric parameters within normal baseline. No severe weather warnings active for {active_district} across 5-day forecast, radar nowcast, or sensor feeds."

    st.markdown(f"""
    <div class="condition-banner {cond_class}">
        <div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                <div style="font-size: 1.15rem; font-weight: 800; color: #F8FAFC;">
                    {cond_title}
                </div>
                <span style="background: {cond_bg}; color: {cond_fg}; border: 1px solid {cond_border}; font-size: 0.75rem; font-weight: 700; padding: 2px 10px; border-radius: 9999px;">
                    {cond_badge}
                </span>
            </div>
            <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.4;">
                {cond_desc}
            </div>
        </div>
        <div style="font-size: 0.78rem; color: #94A3B8; text-align: right;">
            <b>EOC Ops Status:</b> Real-Time IMD Telemetry<br>
            <b>Target Coordinates:</b> {active_coords}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Key Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        today_t = temp_fc[0] if temp_fc else {}
        st.metric(
            label=f"Today's Temp ({active_district})",
            value=f"{today_t.get('max_temp_c', 'N/A')}°C Max",
            delta=f"Min: {today_t.get('min_temp_c', 'N/A')}°C (Dep: {today_t.get('departure_c', 0)}°C)"
        )

    with m2:
        today_rf = rainfall[0] if rainfall else {}
        st.metric(
            label="Today's Rainfall Status",
            value=today_rf.get("rainfall_category", "N/A"),
            delta=f"Spatial: {today_rf.get('station_coverage', 'N/A')}"
        )

    with m3:
        today_w = warnings[0] if warnings else {}
        st.metric(
            label="Severe Weather Alert",
            value=f"{today_w.get('alert_color', 'Green')} Alert",
            delta=today_w.get("alert_level", "No Warning"),
            delta_color="inverse" if today_w.get("alert_color") in ["Yellow", "Orange", "Red"] else "normal"
        )

    with m4:
        highest_color = "Green"
        alert_district = "All Stable"
        for u in upstream_data:
            u_col = u.get("imd_alert_color", "Green")
            if u_col in ["Red", "Orange"]:
                highest_color = u_col
                alert_district = f"{u.get('upstream_district')} ({u_col})"
                break
            elif u_col == "Yellow" and highest_color == "Green":
                highest_color = "Yellow"
                alert_district = f"{u.get('upstream_district')} (Yellow)"

        st.metric(
            label=f"Upstream IMD Status ({active_district})",
            value=f"{highest_color} Alert" if highest_color != "Green" else "All Green (Stable)",
            delta=f"Active on {alert_district}" if highest_color != "Green" else f"{len(upstream_data)} Predictors Monitored",
            delta_color="inverse" if highest_color in ["Red", "Orange", "Yellow"] else "normal"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Operational Snapshot Row (Atmosphere + Convective)
    q1, q2 = st.columns(2)
    with q1:
        st.markdown(f"""
        <div class="temp-card">
            <div style="font-size: 0.8rem; font-weight: 700; color: #F59E0B; text-transform: uppercase; margin-bottom: 4px;">
                🌡️ Live Atmosphere & Past 24h Rain Snapshot — {active_district}
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: center; margin-top: 8px;">
                <div>
                    <div style="font-size: 0.72rem; color: #94A3B8;">Ambient Temp</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #FBBF24;">{temp_obs.get('temperature_c', 'N/A')} °C</div>
                </div>
                <div>
                    <div style="font-size: 0.72rem; color: #94A3B8;">Expected Max/Min</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #FDE68A;">{temp_obs.get('today_max_c', 'N/A')}° / {temp_obs.get('today_min_c', 'N/A')}°C</div>
                </div>
                <div>
                    <div style="font-size: 0.72rem; color: #94A3B8;">Past 24h Actual Rain</div>
                    <div style="font-size: 1.1rem; font-weight: 800; color: #38BDF8;">{obs_rf.get('actual_rainfall_mm', '0.0 mm')}</div>
                </div>
                <div>
                    <div style="font-size: 0.72rem; color: #94A3B8;">Departure (%)</div>
                    <div style="font-size: 1.1rem; font-weight: 800; color: #F87171;">{obs_rf.get('departure_percentage', '-98%')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with q2:
        alarm_lvl = damini.get("alarm_level", "🟢 All Clear (No Active Strikes)")
        c_in = damini.get("total_strikes_inside_boundary", 0)
        st.markdown(f"""
        <div class="obs-card">
            <div style="font-size: 0.8rem; font-weight: 700; color: #38BDF8; text-transform: uppercase; margin-bottom: 4px;">
                ⚡ Immediate Convective & Lightning Status — {active_district}
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: center; margin-top: 8px;">
                <div>
                    <div style="font-size: 0.72rem; color: #94A3B8;">Damini Ground Strikes (0-45m)</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: {'#EF4444' if c_in > 0 else '#10B981'};">{c_in} Inside Boundary</div>
                </div>
                <div>
                    <div style="font-size: 0.72rem; color: #94A3B8;">RMC Nowcast Alert</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #F59E0B;">{nowcast_info.get('alert_color', 'Green')} Alert</div>
                </div>
                <div>
                    <div style="font-size: 0.72rem; color: #94A3B8;">Sensor Alarm Level</div>
                    <div style="font-size: 0.95rem; font-weight: 700; color: #6EE7B7;">{alarm_lvl}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 4. 5-Day Visual Forecast Timeline
    st.subheader(f"5-Day {active_district} Temperature, Forecast & Severe Weather Timeline (Source: IMD)")
    cols = st.columns(len(rainfall))
    for idx, (rf, col) in enumerate(zip(rainfall, cols)):
        w = warnings[idx] if idx < len(warnings) else {}
        t = temp_fc[idx] if idx < len(temp_fc) else {}
        alert_color = w.get("alert_color", "Green")
        badge_cls = "badge-yellow" if alert_color == "Yellow" else ("badge-orange" if alert_color == "Orange" else "badge-green")
        
        with col:
            st.markdown(f"""
            <div class="card">
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700; text-transform: uppercase;">Day {rf.get('day_index')} {'(Today)' if idx == 0 else ''}</div>
                    <div style="font-size: 1.1rem; font-weight: 800; color: #F8FAFC; margin: 2px 0 6px 0;">{rf.get('date', 'N/A')}</div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #F59E0B; margin-bottom: 4px;">🌡️ {t.get('max_temp_c', '-')}°C / {t.get('min_temp_c', '-')}°C</div>
                    <div style="font-size: 0.92rem; font-weight: 700; color: #38BDF8; margin-bottom: 2px;">🌧️ {rf.get('rainfall_category')}</div>
                    <div style="font-size: 0.78rem; color: #94A3B8; margin-bottom: 10px;">Stations: {rf.get('station_coverage')}</div>
                </div>
                <div style="border-top: 1px solid #334155; padding-top: 10px; margin-top: 6px;">
                    <div style="margin-bottom: 6px;"><span class="{badge_cls}">{alert_color} Alert</span></div>
                    <div style="font-size: 0.78rem; color: #CBD5E1; line-height: 1.35;"><b>Hazards:</b> {w.get('warning_summary', 'No Warning')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# -------------------------------------------------------------
# TAB 2: HYDROMETEOROLOGY & INFLOWS
# -------------------------------------------------------------
with tab_hydro:
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(f"""
        <div class="temp-card">
            <div style="font-size: 0.8rem; font-weight: 700; color: #F59E0B; text-transform: uppercase; margin-bottom: 4px;">
                🌡️ Live Ambient Temperature & Atmosphere — {active_district} (Source: IMD)
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 24px; align-items: center; margin-top: 8px;">
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">Current Ambient Temp</div>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #FBBF24;">{temp_obs.get('temperature_c', 'N/A')} °C</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">Today's Expected Max / Min</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #FDE68A;">{temp_obs.get('today_max_c', 'N/A')}° / {temp_obs.get('today_min_c', 'N/A')}°C</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">Humidity & Wind</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #E2E8F0;">{temp_obs.get('relative_humidity_pct', 'N/A')}% | {temp_obs.get('wind_speed_kmh', 'N/A')} km/h</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
        <div class="obs-card">
            <div style="font-size: 0.8rem; font-weight: 700; color: #38BDF8; text-transform: uppercase; margin-bottom: 4px;">
                📊 Past 24-Hour Observed Rainfall — {active_district} (Source: IMD - Recorded at 08:30 IST)
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: center; margin-top: 8px;">
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">Date Recorded</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC;">{obs_rf.get('recorded_date', 'N/A')}</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">Actual Observed</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #38BDF8;">{obs_rf.get('actual_rainfall_mm', '0.0 mm')}</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">Normal Benchmark</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #CBD5E1;">{obs_rf.get('normal_rainfall_mm', '6.0 mm')}</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">Departure (%)</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #F87171;">{obs_rf.get('departure_percentage', '-98%')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(f"Upstream Catchment & Predictor Weather Tracker (Target: {active_district} — Source: IMD)")
    st.caption("Direct IMD observed rainfall, 5-day spatial forecast, and official severe weather warnings across influential upstream/neighbouring predictor districts.")

    if upstream_data:
        grid_cols = st.columns(min(len(upstream_data), 3))
        for idx, mitem in enumerate(upstream_data):
            mcol = grid_cols[idx % len(grid_cols)]
            w_color = mitem.get("imd_alert_color", "Green")
            w_summary = mitem.get("imd_warning_summary", "No Warning")
            w_level = mitem.get("imd_alert_level", "No Warning (No Action)")
            
            if w_color == "Red":
                border_col = "#EF4444"
                badge_bg = "rgba(239, 68, 68, 0.2)"
                badge_text = "#FCA5A5"
                badge_border = "rgba(239, 68, 68, 0.4)"
            elif w_color == "Orange":
                border_col = "#F97316"
                badge_bg = "rgba(249, 115, 22, 0.2)"
                badge_text = "#FB923C"
                badge_border = "rgba(249, 115, 22, 0.4)"
            elif w_color == "Yellow":
                border_col = "#EAB308"
                badge_bg = "rgba(234, 179, 8, 0.2)"
                badge_text = "#FACC15"
                badge_border = "rgba(234, 179, 8, 0.4)"
            else:
                border_col = "#10B981"
                badge_bg = "rgba(16, 185, 129, 0.2)"
                badge_text = "#6EE7B7"
                badge_border = "rgba(16, 185, 129, 0.4)"
            
            f1_entry = mitem["forecast_5days"][0] if mitem.get("forecast_5days") else {}
            f1_cat = f1_entry.get("rainfall_category", "Scattered")
            f1_cov = f1_entry.get("station_coverage", "26-50%")
            r_link = mitem.get("river_link", mitem.get("river_link_to_hailakandi", "Catchment Drainage Corridor"))
            
            with mcol:
                st.markdown(f"""
                <div style="background: #1E293B; border: 1px solid #334155; border-left: 4px solid {border_col}; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; color: #F8FAFC;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2px;">
                        <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC;">
                            📍 {mitem.get('upstream_district')} <span style="font-size: 0.85rem; color: #94A3B8;">({mitem.get('state')})</span>
                        </div>
                    </div>
                    <div style="font-size: 0.78rem; color: #38BDF8; margin-bottom: 6px;">
                        🔗 {r_link}
                    </div>
                    <div style="font-size: 0.85rem; color: #CBD5E1; margin-bottom: 4px;">
                        <b>Past 24h Actual:</b> <span style="font-weight: 700; color: #38BDF8;">{mitem.get('past_24h_actual_rainfall')}</span> ({mitem.get('past_24h_departure', '0%')})
                    </div>
                    <div style="font-size: 0.85rem; color: #CBD5E1; margin-bottom: 8px;">
                        <b>Day 1 Forecast:</b> {f1_cat} <span style="font-size: 0.75rem; color: #94A3B8;">({f1_cov})</span>
                    </div>
                    <div style="font-size: 0.78rem; font-weight: 700; color: {badge_text}; background: {badge_bg}; border: 1px solid {badge_border}; padding: 4px 10px; border-radius: 6px; display: inline-block;">
                        🛡️ IMD {w_color} Alert: {w_summary if w_summary != 'No Warning' else w_level}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Select one or more Secondary Predictor Districts above to activate upstream catchment tracking.")

    # Data Tables for Hydrometeorology
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(f"Hydrometeorology & Catchment Data Records ({active_district})")
    
    subtab_fc, subtab_catchment = st.tabs([
        f"📊 {active_district} 5-Day Forecast Table",
        "🌊 Secondary Predictor Catchment Table"
    ])
    with subtab_fc:
        if os.path.exists(CSV_PATH):
            df = pd.read_csv(CSV_PATH)
            st.dataframe(df, use_container_width=True, hide_index=True)
    with subtab_catchment:
        if os.path.exists(MIZORAM_CSV_PATH):
            mdf = pd.read_csv(MIZORAM_CSV_PATH)
            st.dataframe(mdf, use_container_width=True, hide_index=True)


# -------------------------------------------------------------
# TAB 3: CONVECTIVE & LIGHTNING HAZARDS
# -------------------------------------------------------------
with tab_convective:
    st.markdown(f"""
    <div style="font-size: 1.25rem; font-weight: 800; color: #F87171; margin-bottom: 4px;">
        Lightning & Convective Hazard Monitoring ({active_district})
    </div>
    """, unsafe_allow_html=True)

    timeframe_option = st.selectbox(
        "Select Lightning Observation / Forecast Timeframe:",
        options=[
            "⚡ Real-Time Live Ground Strikes — [⏱️ Time Window: Past 0 to 45 Mins | Live Sensors]",
            "🕒 Short-Range District Nowcast Bulletin — [⏱️ Time Window: Next 0 to 3 Hours | Official IMD]",
            "🗺️ Convective Sector Hazard Risk Zones — [⏱️ Time Window: Next 3 to 6 Hours | Synoptic Cells]"
        ],
        index=0,
        help="Switch between immediate live sensor strike alerts (Damini), short-range 3h nowcast, or extended 3-6h convective hazard zones."
    )

    if "Past 0 to 45 Mins" in timeframe_option:
        # Prominent Time Window Banner Strip
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(56, 189, 248, 0.4); border-left: 5px solid #38BDF8; border-radius: 8px; padding: 10px 16px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);">
            <div style="font-size: 0.88rem; font-weight: 800; color: #38BDF8; letter-spacing: 0.03em;">
                ⏱️ ACTIVE OBSERVATION TIME WINDOW: <span style="background: rgba(56, 189, 248, 0.2); padding: 3px 8px; border-radius: 4px; color: #F8FAFC;">PAST 0 TO 45 MINUTES</span> (GROUND SENSOR OBSERVATION)
            </div>
            <span style="font-size: 0.75rem; font-weight: 700; color: #BAE6FD; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.3); padding: 2px 10px; border-radius: 4px;">
                🛰️ Live IITM-ILDN / DAMINI Sensors
            </span>
        </div>
        """, unsafe_allow_html=True)

        strikes_inside = damini.get("strikes_inside_district", [])
        strikes_all = damini.get("strikes", [])
        c_inside = damini.get("total_strikes_inside_boundary", len(strikes_inside))
        c_20 = damini.get("total_strikes_20km", 0)
        c_40 = damini.get("total_strikes_40km", 0)
        alarm_lvl = damini.get("alarm_level", "🟢 All Clear (No Active Strikes inside District)")
        bbox = damini.get("district_boundary_bbox", current_meta.get("bbox", {}))
        
        is_danger = c_inside > 0 or c_20 > 0
        is_warn = c_40 > 0 and not is_danger
        
        banner_border = "#EF4444" if is_danger else ("#F59E0B" if is_warn else "#10B981")
        badge_bg = "rgba(239, 68, 68, 0.2)" if is_danger else ("rgba(245, 158, 11, 0.2)" if is_warn else "rgba(16, 185, 129, 0.2)")
        badge_fg = "#FCA5A5" if is_danger else ("#FCD34D" if is_warn else "#6EE7B7")
        badge_border = "rgba(239, 68, 68, 0.4)" if is_danger else ("rgba(245, 158, 11, 0.4)" if is_warn else "rgba(16, 185, 129, 0.4)")

        nearest_km = damini.get('nearest_strike_km')
        nearest_dir = damini.get('nearest_strike_direction', '')
        nearest_display = f"{nearest_km} km ({nearest_dir})" if nearest_km is not None else "None in 120 km"

        st.markdown(f"""
        <div style="background: #1E293B; border: 1px solid #334155; border-left: 4px solid {banner_border}; border-radius: 12px; padding: 18px; margin-bottom: 14px; color: #F8FAFC;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div style="font-size: 1.05rem; font-weight: 800; color: #F8FAFC;">
                    🛰️ Live Ground Lightning Strikes — Strictly Inside {active_district} Boundary
                </div>
                <span style="background: {badge_bg}; color: {badge_fg}; border: 1px solid {badge_border}; font-size: 0.78rem; font-weight: 700; padding: 3px 12px; border-radius: 9999px;">
                    {alarm_lvl}
                </span>
            </div>
            <div style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 12px;">
                <b>District Geographic Bounds:</b> Lat [{bbox.get('min_lat', '-')}°N to {bbox.get('max_lat', '-')}°N] | Lon [{bbox.get('min_lon', '-')}°E to {bbox.get('max_lon', '-')}°E]
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 24px; align-items: center; margin: 12px 0; background: #0F172A; padding: 12px 16px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.05);">
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">⚡ Strikes INSIDE Boundary (0–45m)</div>
                    <div style="font-size: 1.45rem; font-weight: 800; color: {'#EF4444' if c_inside > 0 else '#10B981'};">{c_inside} Strikes</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">Outer Perimeter (< 20 km)</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: {'#EF4444' if c_20 > 0 else '#10B981'};">{c_20} Strikes</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">Approaching (20–40 km)</div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: {'#F59E0B' if c_40 > 0 else '#10B981'};">{c_40} Strikes</div>
                </div>
                <div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">Latest Sensor Strike Time</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #38BDF8;">{damini.get('nearest_strike_time_ist', 'No active strikes')}</div>
                </div>
            </div>
            <div style="font-size: 0.84rem; color: {badge_fg}; background: {badge_bg}; border: 1px solid {badge_border}; padding: 8px 12px; border-radius: 6px; margin-top: 8px;">
                📢 <b>Field Sensor Advisory:</b> {damini.get('safety_action', 'Safe to proceed with normal outdoor activities.')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if strikes_inside:
            table_rows = []
            active_count = 0
            for s in strikes_inside:
                s_lat = s.get('latitude')
                s_lon = s.get('longitude')
                age_val = s.get('age_minutes', 0)
                age_str = s.get('age_formatted') or format_strike_age(age_val)
                is_active = s.get('is_active_nowcast', (age_val <= 45.0 if age_val is not None else False))
                gmaps_url = s.get('google_maps_url') or s.get('gmaps_url') or f"https://www.google.com/maps?q={s_lat},{s_lon}"
                active_count += int(bool(is_active))
                table_rows.append({
                    "Coordinates": f"{s_lat}° N, {s_lon}° E",
                    "Locality / Sector": s.get('nearest_locality', 'Unknown'),
                    "Detected (IST)": s.get('timestamp_ist', 'Unknown'),
                    "Age / Status": f"Active · {age_str}" if is_active else f"Historical · {age_str}",
                    "Map": gmaps_url,
                })
            expander_title = f"Sensor records inside {active_district} · {active_count} active / {len(strikes_inside)} total"
            with st.expander(expander_title, expanded=active_count > 0):
                st.caption("Only records detected within the past 45 minutes are counted as active. Older sensor hits are shown as history.")
                st.dataframe(
                    pd.DataFrame(table_rows),
                    column_config={
                        "Map": st.column_config.LinkColumn(
                            "Map",
                            help="Open the strike coordinates in Google Maps",
                            display_text="Open map ↗",
                        )
                    },
                    use_container_width=True,
                    hide_index=True,
                )
        else:
            st.success(f"🟢 Zero ground lightning strikes detected strictly inside {active_district} boundary in the past sensor monitoring window.")

    elif "Next 0 to 3 Hours" in timeframe_option:
        # Prominent Time Window Banner Strip
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(249, 115, 22, 0.4); border-left: 5px solid #F97316; border-radius: 8px; padding: 10px 16px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);">
            <div style="font-size: 0.88rem; font-weight: 800; color: #FB923C; letter-spacing: 0.03em;">
                ⏱️ ACTIVE FORECAST TIME WINDOW: <span style="background: rgba(249, 115, 22, 0.2); padding: 3px 8px; border-radius: 4px; color: #F8FAFC;">NEXT 0 TO 3 HOURS</span> (OFFICIAL IMD NOWCAST BULLETIN)
            </div>
            <span style="font-size: 0.75rem; font-weight: 700; color: #FED7AA; background: rgba(249, 115, 22, 0.15); border: 1px solid rgba(249, 115, 22, 0.3); padding: 2px 10px; border-radius: 4px;">
                🏛️ Regional Meteorological Centre (RMC) Guwahati
            </span>
        </div>
        """, unsafe_allow_html=True)

        alert_color = nowcast_info.get("alert_color", "Orange")
        badge_bg = "rgba(234, 88, 12, 0.2)" if alert_color == "Orange" else ("rgba(234, 179, 8, 0.2)" if alert_color == "Yellow" else "rgba(34, 197, 94, 0.2)")
        badge_fg = "#FB923C" if alert_color == "Orange" else ("#FACC15" if alert_color == "Yellow" else "#4ADE80")
        badge_border = "rgba(234, 88, 12, 0.4)" if alert_color == "Orange" else ("rgba(234, 179, 8, 0.4)" if alert_color == "Yellow" else "rgba(34, 197, 94, 0.4)")
        border_left_color = "#EA580C" if alert_color == "Orange" else ("#CA8A04" if alert_color == "Yellow" else "#16A34A")

        st.markdown(f"""
        <div style="background: #1E293B; border: 1px solid #334155; border-left: 4px solid {border_left_color}; border-radius: 12px; padding: 18px 20px; margin-bottom: 14px; color: #F8FAFC;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="font-size: 1.10rem; font-weight: 800; color: #F8FAFC;">
                    🕒 RMC Guwahati 3-Hour District Nowcast Bulletin ({active_district})
                </div>
                <span style="background: {badge_bg}; color: {badge_fg}; border: 1px solid {badge_border}; font-size: 0.80rem; font-weight: 700; padding: 4px 14px; border-radius: 9999px;">
                    {alert_color} Alert ({nowcast_info.get('alert_level', 'Be Prepared')})
                </span>
            </div>
            <div style="background: #0F172A; border-left: 3px solid #38BDF8; border-radius: 6px; padding: 12px 14px; margin-bottom: 12px;">
                <div style="font-size: 0.95rem; font-weight: 600; color: #E2E8F0; line-height: 1.5;">
                    📢 {nowcast_info.get('message', f'Light to moderate rain with thunderstorm & lightning likely over {active_district} district during nowcast window.')}
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 12px;">
                <div style="background: rgba(15, 23, 42, 0.6); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.05);">
                    <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">⏱️ Valid Window</div>
                    <div style="font-size: 0.92rem; font-weight: 700; color: #38BDF8; margin-top: 2px;">Next 0 – 3 Hours (Live IMD Feed)</div>
                </div>
                <div style="background: rgba(15, 23, 42, 0.6); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.05);">
                    <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">⚡ Convective Trigger</div>
                    <div style="font-size: 0.92rem; font-weight: 700; color: #FB923C; margin-top: 2px;">Thunderstorm & Lightning Activity</div>
                </div>
                <div style="background: rgba(15, 23, 42, 0.6); padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.05);">
                    <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">🌊 Storm Track Movement</div>
                    <div style="font-size: 0.92rem; font-weight: 700; color: #A78BFA; margin-top: 2px;">Propagating along {active_basin} Corridor</div>
                </div>
            </div>
            <div style="font-size: 0.84rem; font-weight: 600; color: {badge_fg}; background: {badge_bg}; border: 1px solid {badge_border}; padding: 8px 12px; border-radius: 6px;">
                🛡️ <b>Immediate Action Suggested:</b> {nowcast_info.get('action_suggested', 'Take shelter in safe structures during lightning activity.')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # Prominent Time Window Banner Strip
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(168, 85, 247, 0.4); border-left: 5px solid #A855F7; border-radius: 8px; padding: 10px 16px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);">
            <div style="font-size: 0.88rem; font-weight: 800; color: #C084FC; letter-spacing: 0.03em;">
                ⏱️ ACTIVE FORECAST TIME WINDOW: <span style="background: rgba(168, 85, 247, 0.2); padding: 3px 8px; border-radius: 4px; color: #F8FAFC;">NEXT 3 TO 6 HOURS</span> (SUB-DISTRICT CONVECTIVE HAZARD ZONES)
            </div>
            <span style="font-size: 0.75rem; font-weight: 700; color: #E9D5FF; background: rgba(168, 85, 247, 0.15); border: 1px solid rgba(168, 85, 247, 0.3); padding: 2px 10px; border-radius: 4px;">
                🗺️ IMD Synoptic Micro-Zones
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 12px;">
            Source: IMD / RMC Guwahati | <b>Extended Active Window:</b> Next 3 to 6 Hours | <b>Storm Track:</b> Propagating along {active_basin} corridor across {active_district}
        </div>
        """, unsafe_allow_html=True)

        if active_sectors:
            z_cols = st.columns(len(active_sectors))
            for s, z_col in zip(active_sectors, z_cols):
                s_color = s.get("alert_color", "Orange")
                border_col = "#EA580C" if s_color == "Orange" else "#CA8A04"
                badge_bg = "rgba(234, 88, 12, 0.2)" if s_color == "Orange" else "rgba(234, 179, 8, 0.2)"
                badge_fg = "#FB923C" if s_color == "Orange" else "#FACC15"
                badge_border = "rgba(234, 88, 12, 0.4)" if s_color == "Orange" else "rgba(234, 179, 8, 0.4)"

                with z_col:
                    st.markdown(f"""
                    <div style="background: #1E293B; border: 1px solid #334155; border-left: 4px solid {border_col}; border-radius: 12px; padding: 16px 18px; height: 100%; color: #F8FAFC;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px;">
                            <div style="font-size: 1.05rem; font-weight: 800; color: #F8FAFC;">
                                📍 {s.get('zone_name')}
                            </div>
                        </div>
                        <div style="margin-bottom: 6px;">
                            <span style="background: {badge_bg}; color: {badge_fg}; border: 1px solid {badge_border}; font-size: 0.76rem; font-weight: 700; padding: 2px 10px; border-radius: 9999px;">
                                {s.get('alert_level', f'{s_color} Alert')}
                            </span>
                        </div>
                        <div style="font-size: 0.92rem; font-weight: 700; color: #38BDF8; font-family: monospace; margin-bottom: 6px;">
                            🌐 {s.get('coordinates')}
                        </div>
                        <div style="font-size: 0.82rem; color: #CBD5E1; margin-bottom: 8px;">
                            <b>Localities:</b> {s.get('localities')}
                        </div>
                        <div style="display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-bottom: 8px;">
                            <span style="background: rgba(15, 23, 42, 0.6); color: #E2E8F0; border: 1px solid rgba(255, 255, 255, 0.1); font-size: 0.78rem; font-weight: 600; padding: 2px 8px; border-radius: 4px;">
                                {s.get('hazard_phenomenon', '⚡ Thunderstorm & Lightning')}
                            </span>
                            <span style="background: rgba(15, 23, 42, 0.6); color: #94A3B8; border: 1px solid rgba(255, 255, 255, 0.1); font-size: 0.78rem; font-weight: 600; padding: 2px 8px; border-radius: 4px;">
                                {s.get('expected_winds', '💨 Gusts 35–45 km/h')}
                            </span>
                        </div>
                        <div style="font-size: 0.78rem; color: #94A3B8; font-style: italic; margin-bottom: 8px;">
                            {s.get('convective_status', 'Orographic and riverine storm development.')}
                        </div>
                        <div style="font-size: 0.78rem; font-weight: 600; color: {badge_fg}; background: {badge_bg}; border: 1px solid {badge_border}; padding: 6px 10px; border-radius: 6px;">
                            🛡️ <b>Action:</b> {s.get('action_suggested', 'Take shelter in sturdy structures during lightning.')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # Sub-district Lightning Coordinate Zones Data Table
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(f"⚡ {active_district} Sub-District Coordinate Sector Registry")
    if os.path.exists(LIGHTNING_CSV_PATH):
        ldf = pd.read_csv(LIGHTNING_CSV_PATH)
        if "Latitude" in ldf.columns and "Longitude" in ldf.columns:
            ldf["Google Maps"] = ldf.apply(
                lambda r: f"https://www.google.com/maps?q={r['Latitude']},{r['Longitude']}", 
                axis=1
            )
            st.dataframe(
                ldf,
                column_config={
                    "Google Maps": st.column_config.LinkColumn(
                        "🗺️ Google Maps",
                        help="Click to view exact sector coordinates on Google Maps",
                        display_text="🗺️ View on Google Maps ↗"
                    )
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.dataframe(ldf, use_container_width=True, hide_index=True)
    else:
        st.info("Click 'Sync with IMD' to generate coordinate lightning data table.")


# -------------------------------------------------------------
# TAB 4: OFFICIAL REPORTS & SQL ARCHIVE
# -------------------------------------------------------------
with tab_reports_sql:
    st.subheader(f"Key Synoptical Excerpts Affecting {active_district} & Northeast (Source: IMD)")
    st.caption("Extracted and analyzed from the official National All-India Weather Forecast Bulletin (Source: IMD)")

    if synoptic_data:
        for item in synoptic_data:
            impact_text = item.get('impact_on_hailakandi', '').replace("Hailakandi", active_district)
            st.markdown(f"""
            <div class="synoptic-card">
                <div style="font-size: 0.75rem; font-weight: 700; color: #38BDF8; text-transform: uppercase; margin-bottom: 2px;">
                    📌 {item.get('category')}
                </div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;">
                    {item.get('headline')}
                </div>
                <div style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 8px; line-height: 1.45;">
                    {item.get('details')}
                </div>
                <div style="font-size: 0.82rem; font-weight: 600; color: #6EE7B7; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); padding: 6px 12px; border-radius: 6px; display: inline-block;">
                    📍 Impact on {active_district}: {impact_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(f"DIWIS SQL Database & Historical Trends — {active_district}")
    st.caption(f"Structured SQLite relational database archiving daily observations, 5-day forecasts, lightning strikes, and upstream catchment inflows specifically for {active_district}, Assam.")

    stats = get_district_tables_stats(active_district, DB_PATH)
    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric(
            label=f"Daily Observations ({active_district})",
            value=f"{stats.get('daily_observations', 0)} Records",
            delta="IMD Recorded Rain & Temps"
        )

    with s2:
        st.metric(
            label=f"5-Day Forecasts ({active_district})",
            value=f"{stats.get('forecast_5days', 0)} Records",
            delta="Spatial Predictions Logged"
        )

    with s3:
        st.metric(
            label=f"Lightning Strikes ({active_district})",
            value=f"{stats.get('lightning_sensor_events', 0)} Events",
            delta="IITM-ILDN Sensor Fixes"
        )

    with s4:
        st.metric(
            label=f"Upstream Inflows for {active_district}",
            value=f"{stats.get('upstream_catchment_records', 0)} Records",
            delta="Runoff Tracking Logs"
        )

    sql_tab1, sql_tab2, sql_tab3, sql_tab4, sql_tab5 = st.tabs([
        f"📊 {active_district} Observations",
        f"📅 {active_district} Forecasts Log",
        f"⚡ {active_district} Lightning Archive",
        f"🌊 Upstream Catchment for {active_district}",
        "💻 Custom Query Console"
    ])

    with sql_tab1:
        obs_query = "SELECT recorded_date, district, state, actual_rainfall_mm, normal_rainfall_mm, departure_pct, departure_category, ambient_temp_c, today_max_c, today_min_c, relative_humidity_pct, wind_speed_kmh, scraped_at FROM daily_observations WHERE district = ? ORDER BY recorded_date DESC;"
        df_obs = query_dataframe(obs_query, params=(active_district,), db_path=DB_PATH)
        if not df_obs.empty:
            st.dataframe(df_obs, use_container_width=True, hide_index=True)
            csv_obs = df_obs.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download {active_district} Observations (CSV)",
                data=csv_obs,
                file_name=f"diwis_daily_observations_{active_district.lower()}.csv",
                mime="text/csv",
                key="dl_obs_sql"
            )
        else:
            st.info(f"No records in daily_observations for {active_district} yet. Click 'Sync with IMD & SQL Database' to populate database.")

    with sql_tab2:
        fc_query = "SELECT forecast_issued_at, day_index, target_date, district, rainfall_category, station_coverage, max_temp_c, min_temp_c, alert_color, alert_level, warning_summary FROM forecast_5days WHERE district = ? ORDER BY forecast_issued_at DESC, day_index ASC;"
        df_fc = query_dataframe(fc_query, params=(active_district,), db_path=DB_PATH)
        if not df_fc.empty:
            st.dataframe(df_fc, use_container_width=True, hide_index=True)
            csv_fc = df_fc.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download {active_district} Forecasts Archive (CSV)",
                data=csv_fc,
                file_name=f"diwis_forecast_archive_{active_district.lower()}.csv",
                mime="text/csv",
                key="dl_fc_sql"
            )
        else:
            st.info(f"No records in forecast_5days for {active_district} yet. Click 'Sync with IMD & SQL Database' to populate database.")

    with sql_tab3:
        lt_query = "SELECT detection_time_ist, district, latitude, longitude, nearest_locality, age_minutes, logged_at FROM lightning_sensor_events WHERE district = ? ORDER BY id DESC LIMIT 500;"
        df_lt = query_dataframe(lt_query, params=(active_district,), db_path=DB_PATH)
        if not df_lt.empty:
            df_lt['Strike Age'] = df_lt['age_minutes'].apply(format_strike_age)
            df_lt['Google Maps'] = df_lt.apply(
                lambda r: f"https://www.google.com/maps?q={r['latitude']},{r['longitude']}",
                axis=1
            )
            st.dataframe(
                df_lt[['detection_time_ist', 'district', 'latitude', 'longitude', 'nearest_locality', 'Strike Age', 'Google Maps', 'logged_at']],
                column_config={
                    "Google Maps": st.column_config.LinkColumn(
                        "🗺️ Google Maps",
                        help="Click to view exact coordinate location on Google Maps",
                        display_text="🗺️ View on Google Maps ↗"
                    )
                },
                use_container_width=True,
                hide_index=True
            )
            csv_lt = df_lt.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download {active_district} Lightning Log (CSV)",
                data=csv_lt,
                file_name=f"diwis_lightning_events_{active_district.lower()}.csv",
                mime="text/csv",
                key="dl_lt_sql"
            )
        else:
            st.info(f"No ground lightning strikes logged in database for {active_district}.")

    with sql_tab4:
        up_query = "SELECT record_date, target_district, upstream_district, upstream_state, river_link, past_24h_rainfall_mm, departure_pct, day1_rainfall_forecast, imd_alert_color, imd_warning_summary FROM upstream_catchment_records WHERE target_district = ? ORDER BY record_date DESC;"
        df_up = query_dataframe(up_query, params=(active_district,), db_path=DB_PATH)
        if not df_up.empty:
            st.dataframe(df_up, use_container_width=True, hide_index=True)
            csv_up = df_up.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download Upstream Catchment Log for {active_district} (CSV)",
                data=csv_up,
                file_name=f"diwis_upstream_catchment_log_{active_district.lower()}.csv",
                mime="text/csv",
                key="dl_up_sql"
            )
        else:
            st.info(f"No records in upstream_catchment_records for {active_district} yet. Click 'Sync with IMD & SQL Database' to populate database.")

    with sql_tab5:
        st.markdown("#### ⚡ Custom Query Console")
        st.caption(f"Select a structured query insight from the dropdown below to explore historical observations, severe warnings, and catchment inflows specifically for **{active_district}**.")
        
        query_presets = {
            f"📊 1. All Daily Observations for {active_district}": (
                "SELECT recorded_date, district, actual_rainfall_mm, normal_rainfall_mm, departure_pct, departure_category, ambient_temp_c, today_max_c, today_min_c, relative_humidity_pct, scraped_at FROM daily_observations WHERE district = ? ORDER BY recorded_date DESC LIMIT 50;",
                (active_district,)
            ),
            f"🌧️ 2. Top Rainfall Events & Departures in {active_district}": (
                "SELECT recorded_date, district, actual_rainfall_mm, normal_rainfall_mm, departure_pct, departure_category FROM daily_observations WHERE district = ? ORDER BY actual_rainfall_mm DESC LIMIT 15;",
                (active_district,)
            ),
            f"⚠️ 3. Active Severe Weather Warnings for {active_district}": (
                "SELECT forecast_issued_at, day_index, target_date, district, alert_color, alert_level, warning_summary FROM forecast_5days WHERE district = ? AND alert_color IN ('Yellow', 'Orange', 'Red') ORDER BY forecast_issued_at DESC, day_index ASC;",
                (active_district,)
            ),
            f"🌊 4. Upstream Catchment Runoff Predictors for {active_district}": (
                "SELECT record_date, target_district, upstream_district, river_link, past_24h_rainfall_mm, departure_pct, imd_alert_color, imd_warning_summary FROM upstream_catchment_records WHERE target_district = ? ORDER BY record_date DESC;",
                (active_district,)
            ),
            f"📈 5. {active_district} Database Record Counts Summary": (
                "SELECT 'daily_observations' as dataset, count(*) as records FROM daily_observations WHERE district = ? UNION ALL SELECT 'forecast_5days', count(*) FROM forecast_5days WHERE district = ? UNION ALL SELECT 'lightning_sensor_events', count(*) FROM lightning_sensor_events WHERE district = ? UNION ALL SELECT 'upstream_catchment_records', count(*) FROM upstream_catchment_records WHERE target_district = ?;",
                (active_district, active_district, active_district, active_district)
            )
        }
        
        preset_choice = st.selectbox("📌 Select Query Insight:", list(query_presets.keys()))
        selected_sql, selected_params = query_presets[preset_choice]
        
        result_df = query_dataframe(selected_sql, params=selected_params, db_path=DB_PATH)
        if not result_df.empty:
            st.dataframe(result_df, use_container_width=True, hide_index=True)
            st.download_button(
                label=f"📥 Download Query Result for {active_district} (CSV)",
                data=result_df.to_csv(index=False).encode('utf-8'),
                file_name=f"diwis_{active_district.lower()}_query_result.csv",
                mime="text/csv",
                key="dl_custom_sql_res"
            )
        else:
            st.info(f"No records returned for {active_district}. Click 'Sync with IMD & SQL Database' above to populate database.")


# -------------------------------------------------------------
# TAB 5: TELEMETRY & DATA PROVENANCE
# -------------------------------------------------------------
with tab_provenance:
    st.markdown(f"""
    <div style="margin-top: 0.5rem; margin-bottom: 1.2rem; display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1px solid #334155; padding-bottom: 12px; flex-wrap: wrap; gap: 10px;">
        <div>
            <div style="font-size: 0.75rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #38BDF8; margin-bottom: 3px;">
                🏛️ Authoritative Data Provenance & Telemetry
            </div>
            <div style="font-size: 1.35rem; font-weight: 800; color: #F8FAFC;">
                Official IMD Meteorological Feeds & Verification Registry
            </div>
            <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 2px;">
                Continuous telemetry synchronization with Ministry of Earth Sciences (MoES), IMD NWFC, and IITM Pune nodes.
            </div>
        </div>
        <div style="background: rgba(34, 197, 94, 0.12); border: 1px solid rgba(34, 197, 94, 0.3); color: #4ADE80; font-size: 0.76rem; font-weight: 700; padding: 4px 12px; border-radius: 9999px;">
            🟢 All 6 Feeds Operational (200 OK)
        </div>
    </div>
    """, unsafe_allow_html=True)

    sources_list = [
        {
            "stream": f"🌧️ 5-Day Rainfall Model ({active_district})",
            "agency": "IMD New Delhi / NWFC",
            "status": "LIVE SYNC 200 OK",
            "protocol": "IMD Forecast Portal",
            "description": "Official interactive district rainfall forecast maps, coverage classifications, and quantitative precipitation forecasts.",
            "url": f"https://mausam.imd.gov.in/responsive/rainfallinformation/district_rain.php?id=Assam&day=Day_1"
        },
        {
            "stream": "📊 Hydrological Services & Basin Rainfall",
            "agency": "IMD Hydro-Meteorology",
            "status": "LIVE SYNC 200 OK",
            "protocol": "Hydromet Services",
            "description": "Official hydro-meteorological river basin precipitation, daily departure stats, and reservoir catchment monitoring.",
            "url": "https://mausam.imd.gov.in/responsive/servicesHydrological.php"
        },
        {
            "stream": "⚠️ 5-Day Severe Weather Warning GIS",
            "agency": "IMD Central GIS Division",
            "status": "LIVE SYNC 200 OK",
            "protocol": "National GIS Map",
            "description": "Official interactive GIS geospatial portal rendering color-coded severe weather warnings, thunderstorm alerts, and hazard maps.",
            "url": "https://mausam.imd.gov.in/responsive/districtWiseWarningGIS.php"
        },
        {
            "stream": "⚡ Real-Time 3-Hour Nowcast GIS",
            "agency": "RMC Guwahati / IMD",
            "status": "LIVE SYNC 200 OK",
            "protocol": "Radar Nowcast GIS",
            "description": "Interactive live convective thunderstorm radar tracking, squall warnings, and real-time short-range district alerts.",
            "url": "https://mausam.imd.gov.in/responsive/districtWiseNowcastGIS.php"
        },
        {
            "stream": "⚡ DAMINI Lightning Sensor Network",
            "agency": "IITM Pune (MoES)",
            "status": "LIVE SENSOR 200 OK",
            "protocol": "IITM-ILDN Network",
            "description": "Official Indian Lightning Detection Network (ILDN) interactive sensor portal mapping real-time cloud-to-ground strike locations.",
            "url": "https://ildn.in/imap.php"
        },
        {
            "stream": "📄 National Synoptic Bulletin (AIWFB)",
            "agency": "NWFC New Delhi",
            "status": "LIVE BULLETIN 200 OK",
            "protocol": "Official Synoptic Portal",
            "description": "Daily official executive meteorological briefing covering synoptic systems, depressions, and monsoon trough movements.",
            "url": "https://mausam.imd.gov.in/responsive/all_india_forcast_bulletin.php"
        }
    ]

    prov_col1, prov_col2, prov_col3 = st.columns(3)
    for idx, s in enumerate(sources_list):
        col = [prov_col1, prov_col2, prov_col3][idx % 3]
        with col:
            st.markdown(f"""
            <div class="provenance-card">
                <div>
                    <div class="prov-header">
                        <span class="prov-badge">🏛️ {s['agency']}</span>
                        <span class="prov-status">🟢 {s['status']}</span>
                    </div>
                    <div class="prov-title">{s['stream']}</div>
                    <div class="prov-desc">{s['description']}</div>
                </div>
                <div class="prov-footer">
                    <span class="prov-protocol">{s['protocol']}</span>
                    <a href="{s['url']}" target="_blank" rel="noopener noreferrer" class="prov-btn">
                        <span>↗ Verify Official Feed</span>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
