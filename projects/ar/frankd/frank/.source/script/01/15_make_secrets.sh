#!/usr/bin/env bash

function make_secrets() {
  local x n o d line
  local r=${1}
  local a="$(get_artifacts_path ${r})/.secrets"
  while IF='' read -r -u7 line; do
    x=${line/*=}
    n=$(basename ${x})
    o="${a}${x}"
    d="$(dirname ${o})"
    [ -d "${d}" ] || mkdir -p ${d}
    cp -f "${DY_CERTS}${x}" ${o} && echo ${o}
  done 7< <(grep -P '\.(key|crt)' "$(get_artifacts_path ${r})/config.map")
}
