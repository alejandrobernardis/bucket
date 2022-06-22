#!/usr/bin/env bash

function make_stack() {
  local r=${1}
  local n=$(get_namespace ${r})
  local P=${PORTS}
  if [ "${P}" == '0' ]; then
    case "${n}" in
      gwy) P=8080;;
      jbs) P=4000;;
      srv) P=8000;;
        *) P=50051;;
    esac
  fi
  local -A values=(
    ["%registry%"]="${RG_HOST}"
    ["%repository%"]="${RG_REPOSITORY}"
    ["%namespace%"]="${n}"
    ["%image%"]="${r}"
    ["%service%"]="${r/*_platform-}"
    ["%tag%"]="$(get_tag ${r})"
    ["%commit%"]="$(get_commit ${r})"
    ["%datetime%"]="$(date +'%FT%T%z')"
    ["%configmap%"]="/etc/server.conf"
    ["%network%"]="${NETWORK}"
    ["%ports%"]="${P}"
    ["%replicas%"]="${REPLICAS}"
    ["%remote%"]="${DK_REMOTE}"
    ["%global%"]="${GLOBAL}"
  )
  local x v=''
  for x in "${!values[@]}"; do
    v="${v} -e s|${x}|${values[${x}]}|g"
  done
  local a=$(get_artifacts_path ${r})
  local o="${a}/service.sh"
  sed ${v} "${CURDIR}/../template/service.sh" > ${o} && echo ${o}
  local l="$(dirname ${a})/latest"
  if [ "$(readlink ${l})" != "${a}" ]; then
    ln -fs ${a} ${l} && echo ${l}
  fi
}
