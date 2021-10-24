#!/bin/bash

LOGIN_SHELL="/bin/bash"
KEY_PASSWORD="$(openssl rand -hex 30|sha256sum |cut -d" " -f1)"
KEY_FILENAME="id_reverse-ssh"

if [ -d "./reverse-ssh" ]; then
  echo "The reverse-ssh directory already exists, not cloning it";
else
  git clone https://github.com/Fahrj/reverse-ssh;
fi

cd reverse-ssh &&
rm -rf bin/* &&
ssh-keygen -q -t ed25519 -N "$KEY_PASSWORD" -f "$KEY_FILENAME" <<< y && \

RS_SHELL="$LOGIN_SHELL" RS_PASS="$KEY_PASSWORD" RS_PUB="$(cat $KEY_FILENAME.pub)" make compressed && \

echo "======================================================"
echo "Done. Use the $KEY_FILENAME private key to login as the 'reverse' user." &&
echo "Use the following password for logging in: $KEY_PASSWORD"