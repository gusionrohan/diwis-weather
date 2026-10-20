#!/usr/bin/env python3
"""
Automated Multi-District Scheduler for DIWIS / DHARA
Runs automatically aligned with IMD's morning and evening bulletin release schedules (08:45 IST and 16:45 IST),
synchronizing all configured districts into partitioned directories and the central SQL database.
"""

import os
import sys
import time
import argparse
import logging
from datetime import datetime
import schedule

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "scheduler.log")

# Setup structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("DIWIS_Scheduler")

from weather_scraper import scrape_weather_data
from geo_registry import NE_STATES_DISTRICTS

DEFAULT_TARGET_DISTRICTS = [
    "Hailakandi",
    "Cachar",
    "Karimganj",
    "Kamrup Metropolitan",
    "Dibrugarh",
    "Biswanath"
]


def run_sync_job(districts: list = None):
    """Executes synchronization across all target districts with isolated error handling."""
    if not districts:
        districts = DEFAULT_TARGET_DISTRICTS

    logger.info(f"🚀 Triggering Scheduled Weather & SQL Database Sync for {len(districts)} districts...")
    
    success_count = 0
    fail_count = 0

    for dist in districts:
        try:
            logger.info(f"[*] Syncing district: {dist}...")
            scrape_weather_data(
                primary_state="Assam",
                primary_district=dist,
                generate_reports=True,
                report_generated_by="Automated Scheduler"
            )
            success_count += 1
            logger.info(f"✅ [{dist}] Sync and report generation completed successfully.")
        except Exception as e:
            fail_count += 1
            logger.error(f"❌ [{dist}] Sync failed: {e}", exc_info=True)

    logger.info(f"🏁 Sync cycle finished: {success_count} succeeded, {fail_count} failed.\n")


def main():
    parser = argparse.ArgumentParser(description="DIWIS Automated Multi-District Weather & SQL Scheduler")
    parser.add_argument("--districts", nargs="*", default=None, help="List of primary districts to monitor")
    parser.add_argument("--all-districts", action="store_true", help="Sync all 35 Assam districts")
    parser.add_argument("--run-now-only", action="store_true", help="Run sync once immediately and exit")
    args = parser.parse_args()

    if args.all_districts:
        target_districts = sorted(NE_STATES_DISTRICTS.get("Assam", []))
    elif args.districts:
        target_districts = args.districts
    else:
        target_districts = DEFAULT_TARGET_DISTRICTS

    logger.info("=" * 65)
    logger.info("  DIWIS WEATHER & SQL DATABASE AUTOMATED MULTI-DISTRICT SCHEDULER")
    logger.info("=" * 65)
    logger.info(f"📍 Active Target Districts ({len(target_districts)}): {', '.join(target_districts[:6])}{'...' if len(target_districts) > 6 else ''}")
    logger.info("📅 Scheduled Daily Run Times (IST):")
    logger.info("   1. 08:45 AM (Morning Bulletin & 24h Observed Rainfall Release)")
    logger.info("   2. 04:45 PM (Evening Forecast & Warning Release)")
    logger.info("=" * 65)

    # Initial execution on startup
    logger.info("[*] Performing initial synchronization cycle...")
    run_sync_job(target_districts)

    if args.run_now_only:
        logger.info("[*] Run-now completed. Exiting.")
        return

    # Schedule recurring morning and evening jobs
    schedule.every().day.at("08:45").do(run_sync_job, districts=target_districts)
    schedule.every().day.at("16:45").do(run_sync_job, districts=target_districts)

    logger.info("[*] Scheduler is active. Press Ctrl+C to terminate.\n")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
