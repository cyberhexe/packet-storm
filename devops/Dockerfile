FROM ubuntu:latest

ENV PACKET_STORM_HOME="/packet-storm"
ENV PACKET_STORM_DOCS="$PACKET_STORM_HOME/docs"

RUN apt update && \
    apt install software-properties-common -y && \
    add-apt-repository ppa:giuspen/ppa && \
    apt update || exit 1 && \
    apt install python3 python3-pip xvfb cherrytree -y && \
    mkdir "$PACKET_STORM_HOME"


WORKDIR "$PACKET_STORM_DOCS"
COPY docs "$PACKET_STORM_DOCS"
COPY devops/scripts/convert-ctb.sh "$PACKET_STORM_DOCS"

COPY devops/scripts/docs-parse.py "$PACKET_STORM_HOME"
COPY devops/scripts/requirements.txt "$PACKET_STORM_HOME"

RUN pip3 install -r "$PACKET_STORM_HOME/requirements.txt"

RUN /bin/bash convert-ctb.sh pentest-glossary.ctb "output"

WORKDIR "$PACKET_STORM_HOME"
ENTRYPOINT ["/bin/python3", "docs-parse.py", "-ed", "docs/output"]
