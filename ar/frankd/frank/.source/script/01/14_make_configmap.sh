#!/usr/bin/env bash

function make_configmap() {
  local r=${1}
  local e=$(get_repo_env_path ${r})
  [ -s "${e}" ] || return 1
  local v line
  local o="$(get_artifacts_path ${r})/config.map"
  if [ -n "$(find "${DY_CREDS}" -type f -regex '.+\.env$')" ]; then
    for x in ${DY_CREDS}/*.env; do source ${x}; done
  fi
  local c="${DY_CREDS}/project/${r}.env"
  [ ! -s "${c}" ] || source ${c}
  > ${o}
  while IF='' read -r -u7 line; do
    if ! [[ "${line}" =~ ^(GH|GO|BUILD|IMAGE|PROJECT|PROTO|PY)_? ]]; then
      v=${line/=*}
      if [[ "${v}" =~ ^(MARIA|MONGO)_DATABASE ]]; then
        if [ -z "${OVERRIDE_DATABASE}" ]; then
          echo "${v}=${r}" >> ${o}
        else
          echo "${v}=${OVERRIDE_DATABASE}" >> ${o}
        fi
      elif [[ "${v}" =~ ^SERVICE_DEBUG ]]; then
        echo "${v}=0" >> ${o}
      elif [[ "${line}" =~ ^CFG_LOG_LEVEL\=10 ]]; then
        echo "${v}=30" >> ${o}
      elif [[ "${line}" =~ ^CFG_LOG_LEVEL\=-1 ]]; then
        echo "${v}=1" >> ${o}
      elif [[ -n "${!v}" ]]; then
        echo "${v}=${!v}" >> ${o}
      else
        echo ${line} >> ${o}
      fi
    fi
  done 7< <(grep -v '^#\|^$' ${e})
  echo ${o}
}
