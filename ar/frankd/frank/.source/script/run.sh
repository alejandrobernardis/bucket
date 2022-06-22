#!/usr/bin/env bash

set -e

# no...
NO_CLEAN=${NO_CLEAN:-0}
NO_CLONE=${NO_CLONE:-0}
NO_BUILD=${NO_BUILD:-0}
NO_TAG=${NO_TAG:-0}
NO_PUSH=${NO_PUSH:-0}
NO_CONFIGMAP=${NO_CONFIGMAP:-0}
NO_SECRETS=${NO_SECRETS:-0}
NO_DEPLOY=${NO_DEPLOY:-0}
# only...
ONLY_CLONE=${ONLY_CLONE:-0}
ONLY_BUILD=${ONLY_BUILD:-0}
ONLY_PUSH=${ONLY_PUSH:-0}
ONLY_DEPLOY=${ONLY_DEPLOY:-0}
ONLY_ARTIFACTS=${ONLY_ARTIFACTS:-0}
# deploy
REPLICAS=${REPLICAS:-3}
PORTS=${PORTS:-0}
NETWORK=${NETWORK:-services}
DEBUG_MODE=${DEBUG_MODE:-0}
PRUNE=${PRUNE:-0}
GLOBAL=${GLOBAL:-0}
# internal
CURDIR=$(dirname "${0}")
_actions=0

# load help
source "${CURDIR}/help.sh"
[ "$#" -eq '0' ] && help

# actions
declare -a repos=()
declare -a steps=()

# deploy
function run() {
  # variables
  local x r s
  # helpers
  for x in $(find ${CURDIR} -type d -regextype grep -regex ".*/[0-9]\{2\}$"); do
    for y in ${x}/*; do source ${y}; done
  done
  # boot
  boot && required
  # debug
  if [ "$DEBUG_MODE" -eq 1 ]; then set -x; else set +x; fi
  # services
  for r in ${!repos[@]}; do
    r=${repos[${r}]}
    hello "${r}"
    for s in ${!steps[@]}; do
      s=${steps[${s}]}
      command_exists "${s}" || break
      hello_task "${s}"
      ${s} ${r}
      [ "$?" -eq '0' ] || break
    done
  done
}

# arguments
shopt -s extglob
while [ "$#" -gt '0' ]; do
  case "${1}" in
    # no
    --no-clean|-Q) NO_CLEAN=1;;
    --no-clone|-C) NO_CLONE=1;;
    --no-build|-B) NO_BUILD=1;;
    --no-tag|-T) NO_TAG=1;;
    --no-push|-P) NO_PUSH=1;;
    --no-configmap|-M) NO_CONFIGMAP=1;;
    --no-secrets|-S) NO_SECRETS=1;;
    --no-deploy|-D) NO_DEPLOY=1;;
    # only
    --only-clone|-c) ONLY_CLONE=1;;
    --only-build|-b) ONLY_BUILD=1;;
    --only-push|-s) ONLY_PUSH=1;;
    --only-deploy|-d) ONLY_DEPLOY=1;;
    --only-artifacts|-a) ONLY_ARTIFACTS=1;;
    # custom
    --replica|-r) shift; REPLICAS=${1};;
    --network|-n) shift; NETWORK=${1};;
    --ports|-p) shift; PORTS=${1};;
    --global|-g) GLOBAL=1;;
    # debug
    --debug|-x) DEBUG_MODE=1;;
    --no-debug|-X) DEBUG_MODE=0;;
    --prune|-q) PRUNE=1;;
    # services
    # - - changeme -> jb_repos - -
    jb_platform-*) repos+=(${1}); ((_actions+=1));;
    # - - changeme -> ms_repos - -
    ms_platform-*) repos+=(${1}); ((_actions+=1));;
    # - - changeme -> sr_repos (expose) - -
    @(sr|gw)_platform-*) repos+=(${1}); ((_actions+=1));;
    @(go|py)_*-template) repos=(${1}); ((_actions+=1));;
    *) ;;
  esac
  shift
done

# help
[ "${_actions}" -eq '0' ] && help

# steps
[ "${NO_CLEAN}"       -eq '1' ] || steps+=(clean_cache)
[ "${NO_CLONE}"       -eq '1' ] || steps+=(fetch_repo)
[ "${NO_BUILD}"       -eq '1' ] || steps+=(build_image)
[ "${NO_TAG}"         -eq '1' ] || steps+=(tag_image)
[ "${NO_PUSH}"        -eq '1' ] || steps+=(push_image)
[ "${NO_CONFIGMAP}"   -eq '1' ] || steps+=(make_configmap)
[ "${NO_SECRETS}"     -eq '1' ] || steps+=(make_secrets)
steps+=(make_stack)
[ "${NO_DEPLOY}"      -eq '1' ] || steps+=(deploy)

# only
[ "${ONLY_CLONE}"     -eq '0' ] || steps=(fetch_repo)
[ "${ONLY_BUILD}"     -eq '0' ] || steps=(build_image)
[ "${ONLY_PUSH}"      -eq '0' ] || steps=(push_image)
[ "${ONLY_DEPLOY}"    -eq '0' ] || steps=(deploy)
[ "${ONLY_ARTIFACTS}" -eq '0' ] || steps=(make_configmap make_secrets make_stack)

# run
run
