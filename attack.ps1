New-Item -Path "HKCU:\Software\Policies\Google\Chrome" -Force
New-ItemProperty -Path "HKCU:\Software\Policies\Google\Chrome" -Name "RestoreOnStartup" -Value 4 -PropertyType DWord -Force
New-Item -Path "HKCU:\Software\Policies\Google\Chrome\RestoreOnStartupURLs" -Force
New-ItemProperty -Path "HKCU:\Software\Policies\Google\Chrome\RestoreOnStartupURLs" -Name "1" -Value "file:///C:/Users/Public/login.html" -PropertyType String -Force
