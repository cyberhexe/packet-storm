FROM ubuntu:latest

ENV PACKET_STORM_HOME="/packet-storm-cli"
ENV PACKET_STORM_DOCS="$PACKET_STORM_HOME/docs"

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install nginx inotify-tools pandoc vim python3 python3-pip python3-magic unzip -y && \
    mkdir "$PACKET_STORM_HOME"

WORKDIR "$PACKET_STORM_DOCS"

COPY requirements.txt "$PACKET_STORM_HOME/"
RUN pip3 install -r "$PACKET_STORM_HOME/requirements.txt"

WORKDIR "$PACKET_STORM_HOME"

COPY packet-storm-cli.py "$PACKET_STORM_HOME/"

ENTRYPOINT ["/usr/bin/python3", "packet-storm-cli.py"]