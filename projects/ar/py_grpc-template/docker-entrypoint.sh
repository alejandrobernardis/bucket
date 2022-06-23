#!/usr/bin/env bash

set -e
export ENV_FILE=${ENV_FILE:-'.env'}

_main() {
  if [ $# -eq 0 ]; then
    set -- python -m server
  elif [ "${1:0:1}" = '+' ]; then
    shift
    set -- python -m server "$@"
  fi
  exec "$@";
}

_main "$@"
