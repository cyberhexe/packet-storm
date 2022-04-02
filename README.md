# packet-storm

Items and tools you may need on a red team engagement.

- You can find various tools devided by their category at the `./tools` folder
- You can find some basic wordlists stored under the `./wordlists` folder
- You can find a simple pentest report template and related technical documentation inside the `./documentation` folder

The app converts the cherrytree notes into HTML files and exports them to an Nginx server.
Use this command for building it:
```bash
$ docker build -t packet-storm-docs -f ./devops/Dockerfile .
```

Use the following command to start the server in Docker:
```bash
$ docker run --rm -it packet-storm-docs:latest
root@6d0e4a4a09d2:/# 
```

or this if you want to get an interactive shell:
```bash
$ docker run --rm -it --entrypoint=/bin/bash packet-storm-docs:latest
root@6d0e4a4a09d2:/# 
```
