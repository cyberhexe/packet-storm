Windows Credentials Editor v1.0
(c) 2010 Amplia Security, Hernan Ochoa
Contact: hernan@ampliasecurity.com
http://www.ampliasecurity.com
-------------------------------------------------------------

Abstract
----------
Windows Credentials Editor (WCE) allows to list logon sessions and add, change, list and delete associated credentials (ex.: LM/NT hashes). This can be used, for example, to perform pass-the-hash on Windows and also obtain NT/LM hashes from memory (from interactive logons, services, remote desktop connections, etc.) which can be used in further attacks.

Supported Platforms
-------------------
Windows Credentials Editor supports Windows XP, 2003, Vista, 7 and 2008 (Vista was
not actually tested yet, but it should work).

Requirements
-------------
This tool requires administrator privileges.

Options
--------
Windows Credentials Editor provides the following options:

Options:
        -l              List logon sessions and NTLM credentials (default).
        -s              Changes NTLM credentials of current logon session.
                        Parameters: <UserName>:<DomainName>:<LMHash>:<NTHash>.
        -r              Lists logon sessions and NTLM credentials indefinitely.
                        Refreshes every 5 seconds if new sessions are found.
                        Optional: -r<refresh interval>.
        -c              Run <cmd> in a new session with the specified NTLM crede
ntials.
                        Parameters: <cmd>.
        -e              Lists logon sessions NTLM credentials indefinitely.
                        Refreshes every time a logon event occurs.
        -o              saves all output to a file.
                        Parameters: <filename>.
        -i              Specify LUID instead of use current logon session.
                        Parameters: <luid>.
        -d              Delete NTLM credentials from logon session.
                        Parameters: <luid>.
        -v              verbose output.

Examples:

	* List current logon sessions

C:\>wce -l
WCE v1.0 (Windows Credentials Editor) - (c) 2010 Amplia Security - by Hernan Ochoa (hernan@ampliasecurity.com)
Use -h for help.

meme:meme:11111111111111111111111111111111:11111111111111111111111111111111

	* List current logon sessions with verbose output enabled

C:\>wce -l -v
WCE v1.0 (Windows Credentials Editor) - (c) 2010 Amplia Security - by Hernan Ochoa (hernan@ampliasecurity.com)
Use -h for help.

Current Logon Session LUID: 00064081h
Logon Sessions Found: 8
WIN-REK2HG6EBIS\auser:NTLM
        LUID:0006409Fh
WIN-REK2HG6EBIS\auser:NTLM
        LUID:00064081h
NT AUTHORITY\ANONYMOUS LOGON:NTLM
        LUID:00019137h
NT AUTHORITY\IUSR:Negotiate
        LUID:000003E3h
NT AUTHORITY\LOCAL SERVICE:Negotiate
        LUID:000003E5h
WORKGROUP\WIN-REK2HG6EBIS$:Negotiate
        LUID:000003E4h
\:NTLM
        LUID:0000916Ah
WORKGROUP\WIN-REK2HG6EBIS$:NTLM
        LUID:000003E7h

00064081:meme:meme:11111111111111111111111111111111:11111111111111111111111111111111	

	* Change NTLM credentials associated with current logon session

C:\>wce -s auser:adomain:99999999999999999999999999999999:99999999999999999999999999999999
WCE v1.0 (Windows Credentials Editor) - (c) 2010 Amplia Security - by Hernan Ochoa (hernan@ampliasecurity.com)
Use -h for help.

Changing NTLM credentials of current logon session (00064081h) to:
Username: auser
domain: admin
LMHash: 99999999999999999999999999999999
NTHash: 99999999999999999999999999999999
NTLM credentials successfully changed!

	* Add/Change NTLM credentials of a logon session (not the current one)

C:\>wce -i 3e5 -s auser:adomain:99999999999999999999999999999999:99999999999999999999999999999999 
WCE v1.0 (Windows Credentials Editor) - (c) 2010 Amplia Security - by Hernan Och
oa (hernan@ampliasecurity.com)
Use -h for help.

Changing NTLM credentials of logon session 000003E5h to:
Username: auser
domain: admin
LMHash: 99999999999999999999999999999999
NTHash: 99999999999999999999999999999999
NTLM credentials successfully changed!

	* Delete NTLM credentials associated with a logon session

C:\>wce -d 3e5
WCE v1.0 (Windows Credentials Editor) - (c) 2010 Amplia Security - by Hernan Ochoa (hernan@ampliasecurity.com)
Use -h for help.

NTLM credentials successfully deleted!

	* Run WCE indefinitely, waiting for new credentials/logon sessions.
	Refresh is performed every time a logon event is registered in the Event Log.

C:\>wce -e

	* Run WCE indefinitely, waiting for new credentials/logon sessions
	Refresh is every 5 seconds by default.

C:\>wce -r

	* Run WCE indefinitely, waiting for new credentials/logon sessions, but refresh every 1 second (by default wce refreshes very 5 seconds)

C:\>wce -r5

