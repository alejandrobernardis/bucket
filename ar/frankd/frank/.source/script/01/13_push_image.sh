#!/usr/bin/env bash

function push_image() {
  local x
  local r=${1}
  local l=$(get_library ${r})
  for x in $(get_tag ${r}) latest; do
    docker push -q "${l}:${x}"
    [ $? -eq 0 ] || return 1
  done
}
