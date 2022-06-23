#!/usr/bin/env bash

function clean_cache() {
  local p=$(get_cache_path ${1})
  find "${p}" -type f -regex '.+\.tmp$' -exec rm -f {} \; &>/dev/null
  echo ${p}
}
