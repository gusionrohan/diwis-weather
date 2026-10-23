$ErrorActionPreference = "Stop"
$taskName = "DIWIS_Daily_History_Collection"
$projectRoot = $PSScriptRoot
$scriptPath = Join-Path $projectRoot "daily_snapshot.py"
$python = (Get-Command python.exe -ErrorAction Stop).Source

if (-not (Test-Path $scriptPath)) {
    throw "Collector script not found: $scriptPath"
}

$action = New-ScheduledTaskAction `
    -Execute $python `
    -Argument "`"$scriptPath`"" `
    -WorkingDirectory $projectRoot
$trigger = New-ScheduledTaskTrigger -Daily -At "09:00AM"
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Hours 4)
$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType Interactive `
    -RunLevel Limited

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Append daily live DIWIS history for all districts offered by the app." `
    -Force | Out-Null

Write-Host "Registered $taskName to run daily at 09:00 in the Windows system time zone."
Write-Host "The current task runs while $env:USERNAME is logged on and starts late runs when possible."
Write-Host "Collector logs: $(Join-Path $projectRoot 'logs\daily_snapshot.log')"
