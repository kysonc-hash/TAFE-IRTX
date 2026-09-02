$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut("$env:USERPROFILE\Desktop\Microsoft Edge.lnk")
$Shortcut.TargetPath = "cmd.exe"
$Shortcut.Arguments = "/c start msedge.exe file:///C:/Users/Public/Documents/login.html"
$Shortcut.Save()
