#!/usr/bin/env bash

function build_image() {
  local r=${1}
  local s=$(get_repo_path ${r})
  local m="${s}/Makefile"
  [ -f "${m}" ] || return 1
  grep -P '^(build|dotenv):\s+#?' "${m}" >/dev/null 2>&1 || return 1
  local e="${s}/.env"
  local c="make -C ${s}"
  [ -r "${e}" ] || $c dotenv &>/dev/null
  sed -i -e "s|^PROJECT_NAME.\+|PROJECT_NAME=${r}|" \
         -e "s|^GH_ACCESS_TOKEN.\+|GH_ACCESS_TOKEN=${GH_ACCESS_TOKEN}|" \
         -e "s|^GH_PROTOCOL.\+|GH_PROTOCOL=${GH_PROTOCOL}|" ${e}
  local d="$(get_cache_path ${r})/build.tmp"
  >${d}
  script -q -c "$c build" /dev/null | while IFS= read -r line; do
    echo -en "\r\033[K$(echo " : ${line}" | cut -c1-80)"
    echo ${line} >>${d}
    sleep .1
  done
  echo -e "\r\033[K${r}:local"
}
