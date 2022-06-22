#!/usr/bin/env bash

set -e

PRUNE=${FRANKD_PRUNE:-0}
REMOTE=${FRANKD_REMOTE:-%remote%}

_CURDIR=$(dirname $0)

function docker-remote() {
  docker -H ${REMOTE} "$@"
}

function is_global() {
  if [[ "%global%" -eq '1' ]]; then
    echo "--mode global"
  else
    echo "--mode replicated"
    echo "--replicas %replicas%"
  fi
}

function find_secrets() {
  local line f n s

  function c() {
    echo $(docker-remote secret ls \
      --quiet --filter "label=app.frank.secret=${1}" \
    )
  }

  while IF='' read -r -u7 line; do
    f=${line/*=}
    n="$(basename ${f})"
    s="$(c ${n})"
    if [[ "${PRUNE}" -eq '1' && -n "${s}" ]]; then
      docker-remote secret rm "${s}" >/dev/null
    fi
    if [ -z "$(c ${n})" ]; then
      docker-remote secret create \
        --label app.frank.secret="${n}" \
        ${n} "${_CURDIR}/.secrets${f}" \
      >/dev/null
    fi
    if [ -n "$(c ${n})" ]; then
      echo "--secret source=${n},target=${f},uid=0,gid=0,mode=0444"
    fi
  done 7< <(grep -P '\.(key|crt)' "${_CURDIR}/config.map");
}

function deploy() {

  if [[ -n "${RG_USERNAME}" && -n "${RG_PASSWORD}" ]]; then
    docker-remote login -u ${RG_USERNAME} -p ${RG_PASSWORD} %registry% >/dev/null 2>&1
  fi

  if [ -z "$(docker-remote network ls --quiet --filter label=app.frank.network=%network%)" ]; then
    docker-remote network create \
        --label=app.frank.network="%network%" \
        --driver overlay \
      %network% >/dev/null;
  fi

  local s="$(docker-remote service ls --quiet --filter label=app.frank.image=%image%)"
  local c="$(docker-remote config ls --quiet --filter label=app.frank.image=%image%)"

  if [ "${PRUNE}" -eq '1' ]; then
    if [ -n "${s}" ]; then
      docker-remote service rm ${s} >/dev/null; s='';
    fi
    if [ -n "${c}" ]; then
      docker-remote config rm ${c} >/dev/null; c='';
    fi
  fi

  if [[ -r ${_CURDIR}/config.map ]]; then

    if [ -z "${c}" ]; then
      docker-remote config create \
          --label=app.frank.image="%image%" \
          --label=app.frank.tag="%tag%" \
          --label=app.frank.commit="%commit%" \
          --label=app.frank.createdat="%datetime%" \
        %namespace%-%service% "${_CURDIR}/config.map" >/dev/null;
    fi

    if [ -n "${s}" ]; then
      docker-remote service update \
          --defrank \
          --with-registry-auth \
          --label-add=app.frank.image="%image%" \
          --label-add=app.frank.tag="%tag%" \
          --label-add=app.frank.commit="%commit%" \
          --label-add=app.frank.updatedat="%datetime%" \
          --publish-add %ports% \
          --image %registry%/%repository%/%image%:%tag% \
          $(is_global) \
        %namespace%-%service%  >/dev/null;
    else
      docker-remote service create \
          --defrank \
          --with-registry-auth \
          --name %namespace%-%service% \
          --hostname %namespace%-%service% \
          --restart-condition on-failure \
          --update-delay 10s \
          --update-parallelism 2 \
          --label=app.frank.image="%image%" \
          --label=app.frank.tag="%tag%" \
          --label=app.frank.commit="%commit%" \
          --label=app.frank.createdat="%datetime%" \
          --label=app.frank.hostname="%service%" \
          --label=app.frank.port="%ports%" \
          --publish %ports% \
          --env ENV_FILE=%configmap% \
          --config source=%namespace%-%service%,target=%configmap%,mode=0755,uid=0,gid=0 \
          --network %network% \
          --constraint node.role==worker \
          $(is_global) \
          $(find_secrets) \
        %registry%/%repository%/%image%:%tag% >/dev/null;
    fi

    printf '\033[34m\n* SERVICE\n\033[37m'
    docker-remote service ls \
      --filter label=app.frank.image="%image%" \
      --format '# ID: {{.ID}}\n# Name: {{.Name}}\n# Image: {{.Image}}\n# Ports: {{.Ports}}';

    printf '\033[34m\n* CONFIG\n\033[37m'
    docker-remote config ls \
      --filter label=app.frank.image="%image%" \
      --filter label=app.frank.commit="%commit%" \
      --format "table# {{.ID}}\t{{.Name}}\t{{.CreatedAt}}";

    printf '\033[34m\n* STATUS\n\033[37m' && sleep 3
    docker-remote service ps \
      --filter label=app.frank.image="%image%" \
      --format "table# {{.ID}}\t{{.Name}}\t{{.Node}}\t{{.CurrentState}}" \
      %namespace%-%service%;

    printf '\n\033[33m Done.\n'
    printf '\n\033[m'

  else

    echo >&2 "\033[31m(e) %service% -> no exite el config-map.\033[m"
    exit 1

  fi

}

while [ "$#" -gt '0' ]; do
  case "${1}" in
    --prune|-p) PRUNE=1;;
    *) ;;
  esac
  shift
done

[ "$?" -ne 0 ] || deploy
