import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import os
import json
import shutil
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_default_report_paths(district_name: str) -> tuple[str, str, str]:
    """Resolves output JSON, PDF, and MD paths for the given district."""
    clean_dist = district_name.lower().replace(" ", "_").replace("-", "_")
    dist_dir = os.path.join(BASE_DIR, "output", clean_dist)
    os.makedirs(dist_dir, exist_ok=True)
    json_path = os.path.join(dist_dir, f"{clean_dist}_weather_forecast.json")
    pdf_path = os.path.join(dist_dir, f"DDMA_{clean_dist}_Daily_Weather_Report.pdf")
    md_path = os.path.join(dist_dir, f"DDMA_{clean_dist}_Daily_Weather_Report.md")
    return json_path, pdf_path, md_path


def generate_markdown_report(combined_data: dict = None, output_path: str = None) -> str:
    """Generates clean Government Standard Markdown Daily Weather Bulletin for active target district."""
    if not combined_data:
        # Fallback to Hailakandi legacy JSON if nothing specified
        legacy_json = os.path.join(BASE_DIR, "output_hailakandi", "hailakandi_weather_forecast.json")
        if os.path.exists(legacy_json):
            with open(legacy_json, "r", encoding="utf-8") as f:
                combined_data = json.load(f)
        else:
            return ""

    target = combined_data.get("metadata", {}).get("target_location", {})
    dist_name = target.get("district", "Hailakandi")
    state_name = target.get("state", "Assam")
    coords_str = target.get("coordinates", "24.68°N, 92.56°E")
    basin_str = target.get("river_basin", "Assam River Basin")
    
    if not output_path:
        _, _, output_path = get_default_report_paths(dist_name)
        
    obs = combined_data.get("observed_rainfall_past24h", {})
    temp = combined_data.get("temperature_data", {}).get("current_observation") or {}
    temp_fc = combined_data.get("temperature_data", {}).get("daily_temperature_forecast_5days", [])
    lightning = combined_data.get("lightning_zones_data", {})
    rainfall = combined_data.get("rainfall_forecast_5days", [])
    warnings = combined_data.get("severe_weather_warnings_5days", {}).get("daily_warnings", [])
    upstream_list = combined_data.get("upstream_catchment_rainfall") or combined_data.get("upstream_mizoram_rainfall", [])
    
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')
    
    t_c = temp.get('temperature_c')
    t_c_str = f"{t_c} °C" if t_c is not None else "N/A (Station Pending)"
    max_t = temp.get('today_max_c')
    min_t = temp.get('today_min_c')
    max_min_str = f"{max_t}°C / {min_t}°C" if max_t is not None and min_t is not None else "N/A"
    hum = temp.get('relative_humidity_pct')
    hum_str = f"{hum}%" if hum is not None else "N/A"
    w_spd = temp.get('wind_speed_kmh')
    w_spd_str = f"{w_spd} km/h" if w_spd is not None else "N/A"
    
    obs_rf = obs.get('actual_rainfall_mm')
    obs_rf_str = obs_rf if obs_rf is not None else "N/A (Telemetry Pending)"
    norm_rf = obs.get('normal_rainfall_mm')
    norm_rf_str = norm_rf if norm_rf is not None else "N/A"
    dep_rf = obs.get('departure_percentage')
    dep_rf_str = dep_rf if dep_rf is not None else "N/A"
    dep_cat = obs.get('departure_category', 'Normal')
    
    md = f"""# DISTRICT DISASTER MANAGEMENT AUTHORITY (DDMA), {dist_name.upper()}
## District Integrated Weather Information System (DIWIS)
**Daily Weather & Hydrological Intelligence Bulletin**

**District:** {dist_name} ({state_name}) | **Basin:** {basin_str} | **HQ Coordinates:** {coords_str}  
**Bulletin Issued:** {now_str} | **Primary Data Source:** India Meteorological Department (IMD) & IITM-ILDN

---

### 1. 🌡️ Current Meteorological Observations & Temperature
*Source: Surface Station Network & IMD / Regional Observatories*
* **Current Ambient Temperature:** {t_c_str}
* **Today's Maximum / Minimum Temperature:** {max_min_str}
* **Relative Humidity:** {hum_str} | **Surface Wind Speed:** {w_spd_str}

---

### 2. 🌧️ Observed Rainfall & 5-Day Rainfall Forecast Matrix
*Source: IMD Hydro-Meteorological Division (08:30 IST Record) & Central GeoServer Warning Network*
* **Past 24h Recorded Rainfall (at 08:30 IST):** {obs_rf_str}
* **Normal Standard Benchmark:** {norm_rf_str}
* **Rainfall Departure (%):** {dep_rf_str} ({dep_cat})

| Day | Forecast Date | Rainfall Prediction | Station Coverage | Severe Weather Alert Level | Hazard Types |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for i, rf in enumerate(rainfall):
        w = warnings[i] if i < len(warnings) else {}
        a_col = w.get('alert_color', 'Green')
        md += f"| Day {rf.get('day_index')} | {rf.get('date')} | {rf.get('rainfall_category')} | {rf.get('station_coverage')} | {a_col} Alert ({w.get('alert_level', 'No Action')}) | {w.get('warning_summary', 'No Warning')} |\n"

    md += f"""
---

### 3. ⚡ Coordinate-Specific Lightning & Convective Hazard Zones ({dist_name})
*Source: Regional Meteorological Centre (RMC) Guwahati / IITM-ILDN DAMINI Sensor Network*
* **Overall Alert:** **{lightning.get('overall_alert', 'Normal Watch')}**
* **Active Window:** **{lightning.get('active_window', 'Next 3 to 6 Hours')}**
* **Storm Track Movement:** **{lightning.get('storm_track_movement', 'Corridor transit')}**

| Sector / Zone | Coordinates | Key Localities Covered | IMD Alert Level | Weather Phenomenon & Winds |
| :--- | :--- | :--- | :--- | :--- |
"""
    for sec in lightning.get("sectors", []):
        alert_str = sec.get('alert_level', sec.get('risk_level', 'Yellow Alert'))
        phenom_winds = f"{sec.get('hazard_phenomenon', 'Thunderstorm')} | {sec.get('expected_winds', '')}"
        md += f"| **{sec.get('zone_name')}** | `{sec.get('coordinates')}` | {sec.get('localities')} | {alert_str} | {phenom_winds} |\n"

    md += f"""
*⚠️ **Field Safety Directive:** {lightning.get('safety_advice', 'Stay indoors in safe buildings during active thunder and lightning activity.')}*

---

### 4. 🌊 Upstream Catchment & Riverine Inflow Predictor Tracker
*Source: IMD Regional Flood Meteorological Division — Upstream Catchment Rainfall & Inflow Signals*

| Predictor District | State | Catchment / River Link | Past 24h Actual Rain | Day 1 Forecast | IMD Warning Alert |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for m in upstream_list:
        f1_entry = m.get('forecast_5days', [{}])[0]
        f1_str = f"{f1_entry.get('rainfall_category', 'Scattered')} ({f1_entry.get('station_coverage', '')})"
        w_alert = m.get('official_imd_status', m.get('runoff_risk', 'Green Alert (No Warning)'))
        md += f"| {m.get('upstream_district')} | {m.get('state', 'Northeast')} | {m.get('river_link', '')} | {m.get('past_24h_actual_rainfall', 'N/A')} | {f1_str} | {w_alert} |\n"

    md += f"""
---

### 5. 🌐 Synoptic Weather Analysis
*Source: National Weather Forecasting Centre (NWFC), IMD New Delhi — All-India Weather Forecast Bulletin*

*Official Disaster Management Dossier generated by **District Integrated Weather Information System (DIWIS)**.*  
*Compiled for the Office of the District Commissioner & District Disaster Management Authority (DDMA), {dist_name}, Assam.*  
*Data Sources: India Meteorological Department (IMD), Ministry of Earth Sciences, Govt. of India & IITM Pune.*
"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as mf:
        mf.write(md)
        
    return output_path


def generate_pdf_report(custom_data: dict = None, generated_by: str = "Operator", output_path: str = None) -> str:
    """Generates a professional 1-page PDF Weather & Inflow Bulletin for the target district with perfect text-wrapping."""
    if custom_data:
        data = custom_data
    else:
        # Fallback to Hailakandi legacy JSON if nothing passed
        legacy_json = os.path.join(BASE_DIR, "output_hailakandi", "hailakandi_weather_forecast.json")
        if not os.path.exists(legacy_json):
            print("JSON not found for PDF report")
            return None
        with open(legacy_json, "r", encoding="utf-8") as f:
            data = json.load(f)

    target = data.get("metadata", {}).get("target_location", {})
    dist_name = target.get("district", "Hailakandi")
    state_name = target.get("state", "Assam")
    coords_str = target.get("coordinates", "24.68°N, 92.56°E")

    if not output_path:
        _, output_path, _ = get_default_report_paths(dist_name)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=32,
        leftMargin=32,
        topMargin=26,
        bottomMargin=26
    )
    
    styles = getSampleStyleSheet()
    govt_head_style = ParagraphStyle(
        'GovtHead',
        parent=styles['Normal'],
        fontSize=13.5,
        leading=16.5,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#0F172A"),
        alignment=1,
        spaceAfter=2
    )
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=10.0,
        leading=12.5,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#0284C7"),
        alignment=1,
        spaceAfter=2
    )
    loc_style = ParagraphStyle(
        'DocLoc',
        parent=styles['Normal'],
        fontSize=7.8,
        leading=10.0,
        fontName='Helvetica',
        textColor=colors.HexColor("#334155"),
        alignment=1,
        spaceAfter=1
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontSize=7.0,
        leading=9.0,
        textColor=colors.HexColor("#64748B"),
        alignment=1,
        spaceAfter=3
    )
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=8.5,
        leading=11,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=3,
        spaceAfter=2
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=6.8,
        leading=9.0,
        textColor=colors.HexColor("#1E293B")
    )
    cell_head_style = ParagraphStyle(
        'CellHead',
        parent=styles['Normal'],
        fontSize=6.8,
        leading=8.8,
        fontName='Helvetica-Bold',
        textColor=colors.white,
        alignment=0
    )
    cell_body_style = ParagraphStyle(
        'CellBody',
        parent=styles['Normal'],
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor("#1E293B"),
        alignment=0
    )
    cell_bold_style = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontSize=6.5,
        leading=8.5,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#0F172A"),
        alignment=0
    )
    footer_style = ParagraphStyle(
        'DocFooter',
        parent=styles['Normal'],
        fontSize=6.2,
        leading=8.0,
        textColor=colors.HexColor("#64748B"),
        spaceBefore=3
    )
    
    story = []
    
    # 1. Header Banner
    story.append(Paragraph(f"DISTRICT DISASTER MANAGEMENT AUTHORITY (DDMA), {dist_name.upper()}", govt_head_style))
    story.append(Paragraph("District Integrated Weather Information System (DIWIS) — Daily Bulletin", title_style))
    story.append(Paragraph(f"District: <b>{dist_name}</b>, {state_name} (HQ: {coords_str}) &nbsp;|&nbsp; River Basin: <b>{data.get('metadata', {}).get('target_location', {}).get('river_basin', 'Assam Basin')}</b>", loc_style))
    story.append(Paragraph(f"Data Sources: <b>India Meteorological Department (IMD) & IITM-ILDN</b> &nbsp;|&nbsp; Bulletin Issued: <b>{datetime.now().strftime('%d-%b-%Y %H:%M IST')}</b>", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.0, color=colors.HexColor("#0284C7"), spaceAfter=3))

    # 2. Temperature Section (Current Observations Only)
    temp_obs = data.get("temperature_data", {}).get("current_observation") or {}
    
    story.append(Paragraph(f"<b>1. 🌡️ Current Meteorological & Temperature Observations — {dist_name}</b>", section_heading))
    
    t_c = temp_obs.get('temperature_c')
    t_c_display = f"{t_c} °C" if t_c is not None else "N/A"
    hum = temp_obs.get('relative_humidity_pct')
    hum_display = f"{hum}%" if hum is not None else "N/A"
    max_t = temp_obs.get('today_max_c')
    min_t = temp_obs.get('today_min_c')
    max_min = f"{max_t}°C / {min_t}°C" if max_t is not None and min_t is not None else "N/A"
    w_spd = temp_obs.get('wind_speed_kmh')
    w_spd_display = f"{w_spd} km/h" if w_spd is not None else "N/A"
    
    temp_metrics = [
        [
            Paragraph(f"<b>Current Ambient Temp:</b> {t_c_display}", body_style),
            Paragraph(f"<b>Today's Max / Min:</b> {max_min}", body_style),
            Paragraph(f"<b>Relative Humidity:</b> {hum_display}", body_style),
            Paragraph(f"<b>Surface Wind Speed:</b> {w_spd_display}", body_style)
        ]
    ]
    t_temp_metrics = Table(temp_metrics, colWidths=[137, 137, 137, 137])
    t_temp_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFBEB")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#FDE68A")),
        ('PADDING', (0,0), (-1,-1), 3.2),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_temp_metrics)
    story.append(Spacer(1, 4))

    # 3. Rainfall Section
    obs = data.get("observed_rainfall_past24h", {})
    rainfall = data.get("rainfall_forecast_5days", [])
    warnings = data.get("severe_weather_warnings_5days", {}).get("daily_warnings", [])
    
    story.append(Paragraph(f"<b>2. 🌧️ Observed Rainfall & 5-Day Forecast Matrix — {dist_name} (Source: IMD)</b>", section_heading))
    
    act_rf = obs.get('actual_rainfall_mm')
    act_rf_display = act_rf if act_rf is not None else "N/A (Pending)"
    norm_rf = obs.get('normal_rainfall_mm')
    norm_rf_display = norm_rf if norm_rf is not None else "N/A"
    dep_rf = obs.get('departure_percentage')
    dep_rf_display = dep_rf if dep_rf is not None else "N/A"
    dep_cat = obs.get('departure_category', 'Normal')
    
    rain_metrics = [
        [
            Paragraph(f"<b>Past 24h Recorded:</b> {act_rf_display}", body_style),
            Paragraph(f"<b>Normal Benchmark:</b> {norm_rf_display}", body_style),
            Paragraph(f"<b>Departure (%):</b> {dep_rf_display} ({dep_cat})", body_style),
            Paragraph(f"<b>Status:</b> {obs.get('status', 'OK')}", body_style)
        ]
    ]
    t_rain_metrics = Table(rain_metrics, colWidths=[137, 137, 137, 137])
    t_rain_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0F9FF")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#BAE6FD")),
        ('PADDING', (0,0), (-1,-1), 2.8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_rain_metrics)
    story.append(Spacer(1, 2))
    
    # 5-Day Rainfall & Severe Weather Warning Table
    forecast_table_data = [
        [
            Paragraph("Day", cell_head_style),
            Paragraph("Forecast Date", cell_head_style),
            Paragraph("Rainfall Prediction", cell_head_style),
            Paragraph("Station Coverage", cell_head_style),
            Paragraph("Severe Weather Alert Level", cell_head_style),
            Paragraph("Hazard Types & Details", cell_head_style)
        ]
    ]
    for idx, rf in enumerate(rainfall):
        w = warnings[idx] if idx < len(warnings) else {}
        a_col = w.get('alert_color', 'Green')
        forecast_table_data.append([
            Paragraph(f"Day {rf.get('day_index')}", cell_bold_style),
            Paragraph(str(rf.get('date', 'N/A')), cell_body_style),
            Paragraph(str(rf.get('rainfall_category', 'N/A')), cell_body_style),
            Paragraph(str(rf.get('station_coverage', 'N/A')), cell_body_style),
            Paragraph(f"<b>{a_col} Alert</b> ({w.get('alert_level', 'No Action')})", cell_body_style),
            Paragraph(str(w.get('warning_summary', 'No Warning')), cell_body_style)
        ])
        
    t_forecast = Table(forecast_table_data, colWidths=[38, 65, 88, 77, 135, 145])
    t_forecast.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('PADDING', (0,0), (-1,-1), 2.2),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_forecast)
    story.append(Spacer(1, 3))

    # 4. Lightning Zones Table
    story.append(Paragraph(f"<b>3. ⚡ Lightning & Convective Hazard Zones — {dist_name} (3–6 Hr Window | Source: IMD / IITM)</b>", section_heading))
    l_data = data.get("lightning_zones_data", {})
    sectors = l_data.get("sectors", [])
    
    l_table_data = [
        [
            Paragraph("Sector / Zone", cell_head_style),
            Paragraph("Coordinates", cell_head_style),
            Paragraph("Key Localities Covered", cell_head_style),
            Paragraph("IMD Warning Alert", cell_head_style),
            Paragraph("Expected Winds & Safety", cell_head_style)
        ]
    ]
    for s in sectors:
        alert_str = s.get("alert_level", "Orange Alert")
        wind_act = f"{s.get('expected_winds', '')} — {s.get('action_suggested', '')}"
        l_table_data.append([
            Paragraph(s.get("zone_name", ""), cell_bold_style),
            Paragraph(s.get("coordinates", ""), cell_body_style),
            Paragraph(s.get("localities", ""), cell_body_style),
            Paragraph(alert_str, cell_body_style),
            Paragraph(wind_act, cell_body_style)
        ])
        
    t_lightning = Table(l_table_data, colWidths=[115, 75, 140, 95, 123])
    t_lightning.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#991B1B")),
        ('PADDING', (0,0), (-1,-1), 2.2),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#FECACA")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FEF2F2"), colors.white]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_lightning)
    story.append(Paragraph("<font size=6 color='#64748B'>*Note: For 0–45 min real-time sensor lightning strike alarms in the field, refer to DAMINI / IITM Lightning Location Network (LLN).</font>", body_style))
    story.append(Spacer(1, 2.5))

    # 5. Upstream Hydrological Inflow & Predictor Catchment Table
    story.append(Paragraph(f"<b>4. 🌊 Upstream Catchment & Weather Tracker for {dist_name} (Source: IMD)</b>", section_heading))
    upstream_list = data.get("upstream_catchment_rainfall") or data.get("upstream_mizoram_rainfall", [])
    miz_data = [
        [
            Paragraph("Predictor District", cell_head_style),
            Paragraph("Catchment / River Link", cell_head_style),
            Paragraph("Past 24h Rain", cell_head_style),
            Paragraph("Day 1 Forecast", cell_head_style),
            Paragraph("IMD Warning Alert", cell_head_style)
        ]
    ]
    for m in upstream_list:
        m_risk = m.get("official_imd_status", m.get("runoff_risk", "Green Alert"))
        m_link = m.get("river_link", "")
        f1_e = m.get("forecast_5days", [{}])[0]
        f1_txt = f"{f1_e.get('rainfall_category', 'Data Pending')}"
        d_label = f"{m.get('upstream_district', '')} ({m.get('state', '')})"
        miz_data.append([
            Paragraph(d_label, cell_bold_style),
            Paragraph(m_link, cell_body_style),
            Paragraph(str(m.get("past_24h_actual_rainfall", "-")), cell_body_style),
            Paragraph(f1_txt, cell_body_style),
            Paragraph(m_risk, cell_body_style)
        ])
    t_miz = Table(miz_data, colWidths=[95, 175, 62, 85, 131])
    t_miz.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0D9488")),
        ('PADDING', (0,0), (-1,-1), 2.2),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F0FDFA")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_miz)
    story.append(Spacer(1, 3))

    # 6. Regional Synoptic Systems
    story.append(Paragraph(f"<b>5. 🌐 Regional Synoptic Systems & Moisture Analysis (Source: IMD AIWFB Bulletin)</b>", section_heading))
    synoptic = data.get("synoptic_bulletin", {}).get("synoptic_excerpts", [])
    for s in synoptic[:2]:
        story.append(Paragraph(f"• <b>{s.get('headline')}:</b> {s.get('details')}", body_style))
        story.append(Spacer(1, 1))
        
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#94A3B8"), spaceAfter=2))
    story.append(Paragraph(f"<i>Official Weather Intelligence Dossier compiled by <b>District Integrated Weather Information System (DIWIS)</b> for DDMA {dist_name}. <b>Data Source: India Meteorological Department (IMD)</b>, Ministry of Earth Sciences, Govt. of India. Alert Colors indicate IMD Severe Weather Warning Level for Thunderstorm/Rainfall Hazards.</i>", footer_style))

    def draw_page_footer(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#64748B"))
        footer_y = 14
        canvas.drawCentredString(letter[0] / 2, footer_y, f"District Disaster Management Authority (DDMA), {dist_name}")
        canvas.drawRightString(letter[0] - 32, footer_y, f"Generated by: {generated_by or 'Operator'}")
        canvas.restoreState()

    doc.build(story, onFirstPage=draw_page_footer, onLaterPages=draw_page_footer)
    print(f"Generated Daily PDF report for {dist_name}: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_markdown_report()
    generate_pdf_report()
