FROM ubuntu:latest

ENV PACKET_STORM_HOME="/packet-storm"
ENV PACKET_STORM_DOCS="$PACKET_STORM_HOME/documentation"
ENV NGINX_DOCS_PATH="/var/www/html/packet-storm-docs"

RUN apt update && \
    apt install software-properties-common -y && \
    add-apt-repository ppa:giuspen/ppa && \
    apt update || exit 1 && \
    apt install xvfb cherrytree nginx -y && \
    mkdir "$NGINX_DOCS_PATH" && \
    mkdir "$PACKET_STORM_HOME"

EXPOSE 80

WORKDIR "$PACKET_STORM_DOCS"

COPY documentation "$PACKET_STORM_DOCS"
COPY devops/convert-ctb.sh "$PACKET_STORM_DOCS"
RUN /bin/bash convert-ctb.sh pentest-glossary.ctb "$NGINX_DOCS_PATH"

COPY devops/entrypoint.sh "$PACKET_STORM_HOME"

ENTRYPOINT ["/bin/bash", "/packet-storm/entrypoint.sh"]