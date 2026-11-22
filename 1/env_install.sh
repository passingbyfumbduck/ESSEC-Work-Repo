#!/usr/bin/env bash
set -e

pretty_print() {
    printf '\n%s\n\n' "$1"
}

install_apt_packages() {
    local apt=(apt-get)
    if (( EUID != 0 )); then
        apt=(sudo apt-get)
    fi
    "${apt[@]}" update
    "${apt[@]}" install -y "$@"
}

case "$OSTYPE" in
    darwin*) os="macOS" ;;
    linux*)  os="Linux" ;;
    *)       os="unknown" ;;
esac

pretty_print "Operating system: $os"

case "$os" in
    macOS) command -v brew >/dev/null || { printf '%s\n' 'Install Homebrew first.' >&2; exit 1; } ;;
    Linux) command -v apt-get >/dev/null || { printf '%s\n' 'This script requires apt-get on Linux.' >&2; exit 1; } ;;
    *) exit 1 ;;
esac

if ! command -v python3 >/dev/null; then
    if [[ "$os" == "macOS" ]]; then
        brew install python
    else
        install_apt_packages python3
    fi
fi
python3 --version

if ! python3 -m pip --version; then
    if [[ "$os" == "Linux" ]]; then
        install_apt_packages python3-pip
    else
        python3 -m ensurepip --upgrade
    fi
    python3 -m pip --version
fi

pretty_print "Setting up Jupyter Notebook"
cd -- "$(dirname -- "$0")"
if ! python3 -m venv .venv; then
    [[ "$os" == "Linux" ]] || exit 1
    install_apt_packages python3-venv
    python3 -m venv .venv
fi
.venv/bin/python -m pip install notebook
.venv/bin/jupyter notebook --version

if [[ "$os" == "macOS" ]]; then
    brew doctor
fi
