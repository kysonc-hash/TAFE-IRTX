$prefPath = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Preferences"

if (Test-Path $prefPath) {
    # Terminate any background chrome processes to release file locks
    Stop-Process -Name chrome -ErrorAction SilentlyContinue
    
    # Read raw configurations
    $content = Get-Content $prefPath -Raw
    
    # Use direct regex string updates to dodge json quotation structure bugs
    if ($content -match '"restore_on_startup":') {
        $content = $content -replace '"restore_on_startup":\s*\d+', '"restore_on_startup":4'
    }
    
    # Write the target path straight back out to disk
    Set-Content $prefPath $content
    Write-Output "Chrome preferences updated successfully."
} else {
    Write-Error "Chrome preferences path not located. Run Chrome once on target PC."
}
