#!/usr/bin/env python3
"""
Backward-compatible wrapper for Hailakandi Weather Scraper.
Delegates to the unified dynamic weather_scraper engine.
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from weather_scraper import scrape_weather_data, main

if __name__ == "__main__":
    main()
