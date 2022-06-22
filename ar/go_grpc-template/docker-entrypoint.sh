#!/usr/bin/env bash

set -e
export CMD_PATH=${CMD_PATH:-/app/cmd}
export RUN_FILE=${RUN_FILE:-main.go}

_main() {
  if [ "${1}" = 'debug' ]; then
    local f_pth="${2:-${CMD_PATH}/${RUN_FILE}}"
    if [ -f "${f_pth}" ]; then
      dlv debug \
        --listen=:40000 \
        --headless=true \
        --api-version=2 \
        --log=true \
        --log-output=debugger,debuglineerr,gdbwire,lldbout \
        --accept-multiclient \
        "${f_pth}"
    else
      echo "Command not found."
      exit 1
    fi
  else
    if [ $# -eq 0 ]; then
      set -- server
    elif [ "${1:0:1}" = '+' ]; then
      shift
      set -- server "$@"
    fi
    exec "$@";
  fi
}

_main "$@"
