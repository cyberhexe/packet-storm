## HTTP

Starting a Tomcat server with Docker:

```bash
#!/bin/bash

dirname=${PWD##*/}
image='tomcat:8'

docker run \
  --rm -it \
  --entrypoint=/bin/bash \
  -v `pwd`:/${dirname} \
  $image
```

Starting a Flask server with CORS:

```python
#!/usr/bin/env python3
from flask import Flask, send_file
from flask_cors import CORS

ip = '127.0.0.1'
port = 5555

app = Flask(__name__)

@app.route('/plugin')
def static_file():
    return send_file(f"./plugin/Plugin.tgz")

CORS(app)
app.run(host=ip, port=port, debug=True)
```


## SMB

Starting an SMB server with Docker:

```bash
#!/bin/bash

#alias impacket="docker run --rm -it rflathers/impacket"

if [ -z "$1" ]; then
    echo "Usage: $0 <folder>"
    exit 0
fi


docker run --rm -it -p 445:445 \
  -v $1":/tmp/serve" \
  rflathers/impacket smbserver.py \
  -smb2support my-awesome-share /tmp/serve
```

## Remote Metasploit

- https://metasploit.help.rapid7.com/docs/running-metasploit-remotely

```bash
msfdb init
msfd -a 127.0.0.1 -p 31337

nc 127.0.0.1 31337
```
