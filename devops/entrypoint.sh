#!/bin/bash -e
_quit () {
  echo 'Caught sigquit, sending SIGQUIT to child';
  kill -s QUIT "$child";
}

trap _quit SIGQUIT;

echo 'Starting child (nginx)';
nginx -g 'daemon off;' &
child=$!;

echo 'Navigate to your browser to see the docs: http://127.0.0.1:80/packet-storm-docs/glossary';
wait $child;