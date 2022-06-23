#!/usr/bin/env bash

HISTSIZE=1000
HISTFILESIZE=0
HISTCONTROL=ignoreboth

alias c='clear'
alias cl='clear;ls'
alias cpl='clear;pwd;ls'
alias :q='exit'
alias reload='exec $SHELL -l'
alias cp='cp -i'
alias rm='rm -i'
alias mv='mv -i'
alias mkdir='mkdir -p'

list() {
  local ls_opts='-lv --classify --group-directories-first --human-readable'
  local ls_opts=$ls_opts' --color=always'
  alias l="ls $ls_opts"
  alias ll=l
  alias l.="ls -d $ls_opts .*"
  alias la="ls -A $ls_opts"
  alias lr="ls -tR $ls_opts"
  alias lt="ls -t $ls_opts"
  alias lrt="ls -1crt $ls_opts"
  alias lrta="ls -1crta $ls_opts"
  alias lh="ls -at $ls_opts |head -15"
  alias lsa="ls -a $ls_opts"
  unset ls_opts
} && list && unset -f list

dotted() {
  local dots='.'; local under='_'; local parents='';
  for _ in {1..7}; do
    dots+='.'; under+='_'; parents+='../';
    alias $dots="cd $parents"
    alias $under="cd $parents; pwd; ls"
  done
  unset dots under parents
} && dotted && unset -f dotted

up() {
  local value=$1
  if [[ "$value" == '' ]]; then
    cd ..
  elif ! [[ "$value" =~ ^[0-9]+$ ]]; then
    echo 'Argument must be a number'
  elif ! [[ "$value" -gt '0' ]]; then
    echo 'Argument must be positive'
  else
    for _ in $(seq 1 "$value"); do
      cd ..
    done
  fi
}

PS1=' \[\033[01;34m\]\w\[\033[00m\]\[\033[01;32m\]:\[\033[00m\] '

if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    source /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    source /etc/bash_completion
  fi
fi
