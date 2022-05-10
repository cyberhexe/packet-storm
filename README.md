# packet-storm

Your personal hacking station.


### Minimalistic setup

Building with Docker:
```bash
$ docker build -t packet-storm -f ./Dockerfile .
```

Printing help:
```bash
$ docker run --rm -it packet-storm -h
```

Running in interactive mode:
```bash
$ docker run --rm -it packet-storm
```

Or download the image from Docker Hub:

```bash
$ docker run --rm -it cyberhexe/packet-storm
```