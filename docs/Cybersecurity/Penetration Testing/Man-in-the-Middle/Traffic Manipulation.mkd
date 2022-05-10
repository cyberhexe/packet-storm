## Using mitmproxy

- https://docs.mitmproxy.org/stable/

`mitmproxy` is a set of tools that provide an interactive, SSL/TLS-capable intercepting proxy for HTTP/1, HTTP/2, and WebSockets.

## Starting the proxy on the given port

```bash
mitmproxy -p 5050
```

Using an addon to spoof HTTP on-the-fly:

```bash
$ cat http-replace-content.py
#!/usr/bin/env python3
import os
from mitmproxy import http
from mitmproxy import ctx

# e.g.: replacing the title of the http://example.com website
server_host = 'example.com'
original_content = "Example Domain"
new_content = "Totally Hacked"


def response(flow: http.HTTPFlow):
    if server_host == flow.request.host:
        ctx.log.info(f"Replacing '{original_content}' with '{new_content}'")
        flow.response.content = flow.response.content.replace(bytes(original_content.encode('utf8')),
                                                              bytes(new_content.encode('utf8')))
                                                              
$ mitmproxy -p 5050 --script http-replace-content.py
```
