#!/usr/bin/env bash

function check_data() {
  local n=${1}
  local p=${2:-775}
  local g=$(id -g)
  [ -n "${n}" ] \
    || error_and_exit "Arguments not found"
  [ -d "${n}" ] \
    || $shx "mkdir -p ${n}"
  [ "$(stat -c '%g' ${n} | grep -Pw ${g})" == "${g}" ] \
    || $shx "chgrp ${g} ${n}"
  [ "$(stat -c '%a' "${n}" | grep -Pw '\d+')" -eq "${p}" ] \
    || $shx "chmod ${p} ${n}"
}

# condiciones requeridas

function required() {
  for cmd in curl docker git gh; do
    if ! command_exists $cmd; then
      error_and_exit "command ${BOLD}\"$cmd\"${RESET}${RED} not found"
    fi
  done
}

# permisos y grupos

function boot() {
  local x
  for x in \
    "${DY_ROOT}" \
    "${DY_ARTIFACTS}" \
    "${DY_CACHE}" \
    "${DY_CERTS}" \
    "${DY_CREDS}" \
    "${DY_REPOS}" \
  ; do
    check_data "${x}"
  done
}

# ejecución de comandos con privilegios

shx='sh -c'

[ "$(id -u)" -eq '0' ] || {
  if command_exists sudo; then
    shx='sudo -E sh -c'
  elif command_exists su; then
    shx='su -c'
  else
    exit 1
  fi
}
