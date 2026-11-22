#!/usr/bin/env bash
set -e

printf '%s\n' 'Starting installation...'
if (( EUID == 0 )); then
    apt-get update
    apt-get install -y tree
else
    sudo apt-get update
    sudo apt-get install -y tree
fi
printf '%s\n' 'Installation complete!'
