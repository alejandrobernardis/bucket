#!/usr/bin/env bash

function deploy() {
  local x y
  local r=${1}
  [ "${DEBUG_MODE}" -eq '0' ] || x='-x'
  [ "${PRUNE}"      -eq '0' ] || y='--prune'
  sh -c "RG_USERNAME=${RG_USERNAME} RG_PASSWORD=${RG_PASSWORD} \
    bash ${x} $(get_artifacts_path ${r})/service.sh ${y}"
}
