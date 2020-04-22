#!/bin/bash -e
case "$1" in
  start)
    python3 parser.py
    ;;
    *)
    exec "$@"
esac