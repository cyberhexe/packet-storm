## Tail Files

Get last edited file:

```bash
dir | sort LastWriteTime |select -last 1
```

Tail a file with Powershell:

```bash
Get-Content .\file.log -wait -tail 1
Get-Content .\file.log -wait -tail 1 |Select-String -Pattern "select version"
Get-Content .\file.log -wait -tail 1 |Select-String -Pattern "(resourceid( >|\))|syntax error)"
```

Tail a file, filter the output and include 2 lines around it:

```bash
Get-Content .\file.log -wait -tail 1 |Select-String -Pattern "error" -context 0,2
```
