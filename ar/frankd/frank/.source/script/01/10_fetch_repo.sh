#!/usr/bin/env bash

function fetch_repo() {
  local r=${1}
  local u=$(get_repo_url ${r})
  local d=$(get_repo_path ${r})
  if [ ! -d "${d}" ]; then
    yes | git clone --recursive --single-branch \
      --config=core.eol=lf \
      --config=core.autocrlf=false \
      --config=fsck.zeroPaddedFilemode=ignore \
      --config=fetch.fsck.zeroPaddedFilemode=ignore \
      --config=receive.fsck.zeroPaddedFilemode=ignore \
      --config=rebase.autoStash=true \
      --branch=${GH_BRANCH} \
      --depth=1 \
      "${u}" "${d}"
  else
    local g="git --git-dir=${d}/.git --work-tree=${d}"
    if $($g remote get-url --push origin | grep "$(get_repo_service)" >/dev/null); then
      $g remote set-url origin "${u}"
      $g pull --rebase --stat --recurse-submodules origin ${GH_BRANCH}
    else
      rm -fr "${d}" && fetch_repo ${r}
    fi
  fi
}
