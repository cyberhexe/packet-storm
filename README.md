# packet-storm

Your personal hacking station.


### Minimalistic setup

Building with Docker:
```bash
$ docker build -t packet-storm-cli -f ./devops/Dockerfile .
```

Printing help:
```bash
$ docker run --rm -it packet-storm-cli -h
```

Running in interactive mode:
```bash
$ docker run --rm -it packet-storm-cli
```

### Complete setup

This setup includes a Trilium server to sync the notes with.

Start the setup with docker-compose:

```bash
docker-compose -f devops/docker-compose.yml up -d --build --force-recreate
```

List the running containers:

```bash
docker ps
CONTAINER ID   IMAGE                     COMMAND                  CREATED         STATUS         PORTS                                                 NAMES
ecb65edf157a   devops_packet-storm-cli   "/bin/python3 packet…"   4 seconds ago   Up 2 seconds                                                         devops-packet-storm-cli-1
24880c4770f6   zadam/trilium             "docker-entrypoint.s…"   4 seconds ago   Up 3 seconds   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp, 8080/tcp   devops-trilium-server-1
```

Attach to the CLI:

```bash
$ docker attach ecb65edf157a
>>
```
