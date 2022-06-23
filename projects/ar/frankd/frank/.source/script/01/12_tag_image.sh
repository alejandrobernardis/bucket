#!/usr/bin/env bash

function tag_image() {
  local x
  local r=${1}
  local l=$(get_library ${r})
  for x in $(get_tag ${r}) latest; do
    x="${l}:${x}"
    docker tag "${r}:local" ${x}
    [ $? -eq 0 ] || return 1
    echo ${x}
  done
}
