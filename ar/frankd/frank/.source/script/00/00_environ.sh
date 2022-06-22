#!/usr/bin/env bash

# env-file
function load_env() {
  local x f='frankdrc'
  for x in \
    "${HOME}/.${f}" \
    "${HOME}/.frankd/${f}" \
    "${HOME}/.config/${f}" \
    "${HOME}/.config/frankd/${f}" \
    "/etc/frankd/${f}" \
    ".${f}" \
    "../.${f}" \
    "../../.${f}" \
  ; do
    [ ! -r "${x}" ] && continue
    source "${x}"
    return
  done
  printf '\033[31m >>> Environment file not found <<< \033[m\n'; exit 1;
} && load_env

# deploy
DY_ROOT=${DY_ROOT:-'/var/data'}
DY_ARTIFACTS=${DY_ARTIFACTS:-"${DY_ROOT}/artifacts"}
DY_CACHE=${DY_CACHE:-"${DY_ROOT}/cache"}
DY_CERTS=${DY_CERTS:-"${DY_ROOT}/certs"}
DY_CREDS=${DY_CREDS:-"${DY_ROOT}/creds"}
DY_REPOS=${DY_REPOS:-"${DY_ROOT}/repos"}

# files
DY_REPOS_LIST=${DY_REPOS_LIST:-"${DY_CACHE}/repos.list"}

# repos
DY_CMD_REPOS=${DY_CMD_REPOS:-'gh-repos'}

# docker
DK_REMOTE=${DK_REMOTE:-'ssh://m1.prv.frank.com'}

# registry
RG_HOST=${RG_HOST:-'rg.prv.frank.com:5000'}
RG_REPOSITORY=${RG_REPOSITORY:-'frank'}
RG_USERNAME=${RG_USERNAME:-'devops'}
RG_PASSWORD=${RG_PASSWORD:-}

# github
GH_HOST=${GH_HOST:-'github.com'}
GH_PROTOCOL=${GH_PROTOCOL:-'https'}
GH_USERNAME=${GH_USERNAME:-'frank'}
GH_ACCESS_TOKEN=${GH_ACCESS_TOKEN:-}
GH_ORGANIZATION=${GH_ORGANIZATION:-'frank'}
GH_BRANCH=${GH_BRANCH:-'develop'}
GH_JSON_LIMIT=${GH_JSON_LIMIT:-199}
GH_JSON_TEMPLATE=${GH_JSON_TEMPLATE:-'id,isEmpty,isTemplate,nameWithOwner,name,owner,parent,sshUrl,updatedAt,url'}
[ -n "${GH_ACCESS_TOKEN}" ] || GH_PROTOCOL=ssh

# gitlab
GL_HOST=${GL_HOST:-'gitlab.com'}
GL_API=${GL_API:-"https://${GL_HOST}/api/v4"}
GL_DEPLOY_USERNAME=${GL_DEPLOY_USERNAME:-'frank-ro'}
GL_DEPLOY_TOKEN=${GL_DEPLOY_TOKEN:-}
GL_ACCESS_TOKEN=${GL_ACCESS_TOKEN:-}
GL_GROUP_ID=${GL_GROUP_ID:-51657347}
GL_GROUP_PATH=${GL_GROUP_PATH:-'frank'}

# colors
BLACK=$(printf '\033[30m')
RED=$(printf '\033[31m')
GREEN=$(printf '\033[32m')
YELLOW=$(printf '\033[33m')
BLUE=$(printf '\033[34m')
MAGENTA=$(printf '\033[35m')
CYAN=$(printf '\033[36m')
GRAY=$(printf '\033[37m')
NORMAL=$(printf '\033[0m')
BOLD=$(printf '\033[1m')
RESET=$(printf '\033[m')

# bat
export BAT_DEFAULT_OPTS='--color always --plain --number --theme 1337'

# fzf
export FZF_DEFAULT_PROMPT='▸:'
export FZF_DEFAULT_POINTER='▸'
export FZF_DEFAULT_MARKER='✕'
export FZF_DEFAULT_OPTS='
  --color dark
  --color "preview-bg:232"
  --color fg:240,bg:232,hl:230,fg+:215,bg+:235,hl+:229,border:236,gutter:233
  --color spinner:150,info:150,header:246
  --color prompt:039,pointer:215,marker:204
  --prompt " '${FZF_DEFAULT_PROMPT}' "
  --pointer " '${FZF_DEFAULT_POINTER}'"
  --marker "'${FZF_DEFAULT_MARKER}' "
  --preview-window hidden
  --bind "?:toggle-preview"'
export FZF_COMPLETION_TRIGGER=','
export FZF_BAT_DEFAULT_OPTS="bat ${BAT_DEFAULT_OPTS}"
