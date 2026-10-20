@echo off
cd /d "D:\WebScrap"
echo Running DHARA Weather Scraper & SQL Database Sync...
python weather_scraper.py >> scheduler.log 2>&1
echo Done.
