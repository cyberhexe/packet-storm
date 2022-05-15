### Sweeping databases

Using mssql_ping module 
*Hint: Use the `scanner/mssql/mssql_login` module to brute-force the password.*

```bash
msf > use auxiliary/scanner/mssql/mssql_ping 
msf auxiliary(mssql_ping) > set RHOSTS 10.211.55.1/24 
RHOSTS => 10.211.55.1/24 
msf auxiliary(mssql_ping) > exploit
```
