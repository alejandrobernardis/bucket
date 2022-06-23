#!/usr/bin/env bash

set -e
export ENV_FILE=${ENV_FILE:-'.env'}
export ENV_MODULE=${ENV_MODULE:-'service'}

_main() {
  if [ $# -eq 0 ]; then
    set -- python -m "${ENV_MODULE}"
  elif [ "${1:0:1}" = '+' ]; then
    shift
    set -- python -m "${ENV_MODULE}" "$@"
  fi
  exec "$@";
}

_main "$@"
