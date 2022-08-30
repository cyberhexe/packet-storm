# packet-storm

Your personal hacking station. 

Contains a Docker image with a tool that recursively 
walks through the given folder and creates a command-line note application for handling markdown and/or text files it discovers. 


### Usage

Building with Docker:
```bash
docker-compose up --build --force-recreate --detach
```

Using packet-storm:
```bash
docker attach packet-storm
```
