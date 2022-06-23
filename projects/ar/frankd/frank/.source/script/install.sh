#!/usr/bin/env bash

set -e
shx='sh -c'

[ "$(id -u)" -eq '0' ] || {
  if command -v sudo >/dev/null; then
    shx='sudo -E sh -c'
  elif command -v su >/dev/null; then
    shx='su -c'
  else
    exit 1
  fi
}

_curdir="$(dirname ${BASH_SOURCE[0]})"

function _install() {
  local d="${_curdir}/../${1}"
  $shx "chmod +x ${d}/*"
  for x in ${d}/*; do
    $shx "ln -vfsr ${x} /usr/local/bin/$(basename ${x})"
  done
}

printf '\033[34m > creación de links...\033[m\n'
_install 'tool'
_install 'bin'

printf '\033[32m Done.\033[m\n'
