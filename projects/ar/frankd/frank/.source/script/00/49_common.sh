#!/usr/bin/env bash

# ------------------------------------------------------------------------------

function error_and_exit() {
  local m=${1:-'Not controlled'}
  local c=${2:-1}
  echo >&2 "${YELLOW_BULLET}${RED}(e) ${m}.${RESET}"
  [ "${c}" -eq '0' ] || exit ${c}
}

function hello() {
  local l=' # ---------------------------------------------------------------------------- # '
  echo "${RED}${BOLD}${l}"
  echo " > ${1}"
  echo "${l}${RESET}"
}

function hello_task() {
  echo " > ${GREEN}${BOLD}${1}${RESET}"
}

function command_exists() {
  command -v "$@" >/dev/null 2>&1
}

function _mk_path() {
  [ -d ${1} ] || mkdir -p ${1}
  chmod ${2:-'770'} ${1}
  echo ${1}
}

# ------------------------------------------------------------------------------

function get_repo_path() {
  echo "${DY_REPOS}/${1}"
}

function get_repo_env_path() {
  echo "$(get_repo_path ${1})/.env"
}

function get_cache_path() {
  _mk_path "${DY_CACHE}/${1}"
}

function get_artifacts_path() {
  local r=${1}
  _mk_path "${DY_ARTIFACTS}/${r}/$(get_commit ${r})"
}

function get_repo_service() {
  echo "$(grep -oP "${GL_HOST}|${GH_HOST}" "${DY_REPOS_LIST}" | head -1)"
}

function get_repo_url() {
  local r=${1}
  local s=$(get_repo_service)
  if [[ "${GH_PROTOCOL}" == "https" ]]; then
    if [[ "${s}" =~ ${GH_HOST} ]]; then
      echo "https://${GH_ACCESS_TOKEN}@${GH_HOST}/${GH_ORGANIZATION}/${r}.git"
    else
      echo "https://${GL_DEPLOY_USERNAME}:${GL_DEPLOY_TOKEN}@${GL_HOST}/${GL_GROUP_PATH}/${r}.git"
    fi
  else
    if [[ "${s}" =~ ${GH_HOST} ]]; then
      echo "git@${GH_HOST}:${GH_ORGANIZATION}/${r}.git"
    else
      echo "git@${GL_HOST}:${GL_GROUP_PATH}/${r}.git"
    fi
  fi
}

# ------------------------------------------------------------------------------

function get_library() {
  echo "${RG_HOST}/${RG_REPOSITORY}/${1}"
}

function get_commit() {
  local r=${1}
  local o="$(get_cache_path ${r})/commit.tmp"
  if [ ! -s "${o}" ]; then
    local s=$(get_repo_path ${r})
    echo "$(git --git-dir="${s}/.git" --work-tree="${s}" rev-parse --short HEAD)" > ${o}
  fi
  cat ${o}
}

function get_tag() {
  local r=${1}
  local o="$(get_cache_path ${r})/tag.tmp"
  if [ ! -s "${o}" ]; then
    echo "v$(date +'%Y.%-m.%-d').$(get_commit ${r})" > ${o}
  fi
  cat ${o}
}

function get_image() {
  echo "$(get_library ${1}):$(get_tag ${1})"
}

function get_image_latest() {
  echo "$(get_library ${1}):latest"
}

# ------------------------------------------------------------------------------

function _get_project_value() {
  echo $(sed -n "s|^${2}=\(.*\)|\1|p" $(get_repo_env_path ${1}))
}

function get_project() {
  _get_project_value ${1} 'PROJECT_NAME'
}

function get_port() {
  _get_project_value ${1} 'PROJECT_PORT'
}

# ------------------------------------------------------------------------------

function get_namespace() {
  case ${1} in
    gw_*) echo 'gwy';;
    jb_*) echo 'jbs';;
    ms_*) echo 'msv';;
    sr_*) echo 'srv';;
       *) echo 'pfm';;
  esac
}
