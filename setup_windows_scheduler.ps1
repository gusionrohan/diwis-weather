# PowerShell script to register Windows Scheduled Task for DHARA Weather Scraper
$taskName = "DHARA_Weather_SQL_Sync"
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument '/c "D:\WebScrap\run_sync.bat"'

# Trigger at 08:45 AM daily and 04:45 PM daily
$trigger1 = New-ScheduledTaskTrigger -Daily -At "08:45AM"
$trigger2 = New-ScheduledTaskTrigger -Daily -At "04:45PM"

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register or update task
try {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger @($trigger1, $trigger2) -Settings $settings -Description "Automatic sync for DHARA IMD Weather & SQL Database"
    Write-Host "✅ Successfully registered Windows Scheduled Task: $taskName" -ForegroundColor Green
    Write-Host "   Triggers: Daily at 08:45 AM and 04:45 PM IST" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Error creating scheduled task: $_" -ForegroundColor Red
}
