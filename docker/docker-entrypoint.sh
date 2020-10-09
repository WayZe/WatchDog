#!/usr/bin/env sh
case "$1" in
  start)
    python3 app/api.py
    ;;
    *)
    exec "$@"
esac
