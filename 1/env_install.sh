#!/usr/bin/env bash

pretty_print() {
    printf '\n%s\n\n' "$1"
}

case "$OSTYPE" in
    darwin*) os="macOS" ;;
    linux*)  os="Linux" ;;
    *)       os="unknown" ;;
esac

pretty_print "Operating system: $os"
