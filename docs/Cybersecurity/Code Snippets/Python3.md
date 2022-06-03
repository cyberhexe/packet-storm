Replace string occurrences in a binary file:

```python
#!/usr/bin/env python3
import re

source_file_name = "init.bak"
target_file_name = "modified.bak"

string_to_be_replaced = "sepolicy"
target_value = "sepolicz"


with open(source_file_name, "rb") as f:
    b = f.read()

file_as_hex = b.hex()

sequence_to_search_for = string_to_be_replaced.encode("ascii").hex()

target_sequence = target_value.encode("ascii").hex()


print(sequence_to_search_for in file_as_hex)

modified = re.sub(sequence_to_search_for, target_sequence, file_as_hex)

print(sequence_to_search_for in modified)
print(target_sequence in modified)

with open(target_file_name, "wb") as f:
    f.write(bytes.fromhex(modified))
```

Create a proxy server with Twistd:

```python
#!/usr/bin/env python3
from twisted.protocols.portforward import ProxyFactory
from twisted.application import internet,service

src_ip = "10.91.20.66"
src_port = 8080
dst_ip = "127.0.0.1"
dst_port = 8080

application = service.Application("Proxy")
server = ProxyFactory(dst_ip, dst_port)
ps = internet.TCPServer(src_port,server,50,src_ip)

ps.setServiceParent(application)
```
