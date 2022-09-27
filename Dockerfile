FROM ubuntu:latest

ENV PACKET_STORM_HOME="/packet-storm-cli"

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install neovim wget curl git nginx inotify-tools pandoc vim-nox python3 python3-pip python3-magic unzip -y && \
    mkdir "$PACKET_STORM_HOME"

# configure vim
RUN mkdir -p /root/.vim/autoload/
COPY vimrc /root/.vimrc
RUN vim +'PlugInstall --sync' +qa


COPY requirements.txt "$PACKET_STORM_HOME/"
RUN pip3 install -r "$PACKET_STORM_HOME/requirements.txt"

WORKDIR "$PACKET_STORM_HOME"

COPY ./src "$PACKET_STORM_HOME/src"

ENTRYPOINT ["/usr/bin/python3", "src/packet_storm/packet-storm-cli.py"]