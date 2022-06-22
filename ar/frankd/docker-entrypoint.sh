#!/usr/bin/env bash

set -e

if [ -S /var/run/docker.sock ]; then
  sudo chown root:frank /var/run/docker.sock
fi

if [ -d /var/data ]; then
  sudo chown root:frank /var/data/* >/dev/null 2>&1 || true
  sudo chmod 770 /var/data/* >/dev/null 2>&1 || true
fi

if ! command -v gh-repos >/dev/null 2>&1; then
  gh-repos
fi

exec "$@"
