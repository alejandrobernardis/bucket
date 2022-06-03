#syntax=docker/dockerfile:1.2
ARG PY_VERSION=3.10
ARG PY_PATCH=.4

FROM --platform=linux/amd64 python:${PY_VERSION}${PY_PATCH}-bullseye AS base
ARG PY_VERSION
ARG PY_PATCH
ARG COMMIT=0

LABEL \
  app.aysa.prmgt.lang=python \
  app.aysa.prmgt.lang.version=${PY_VERSION} \
  app.aysa.prmgt.lang.patch=${PY_PATCH} \
  app.aysa.prmgt.commit=${COMMIT} \
  app.aysa.prmgt.os=debian

RUN rm -f /etc/apt/apt.conf.d/docker-clean
RUN --mount=type=cache,target=/var/cache/apt \
  apt-get update; \
  DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --assume-yes \
    ca-certificates git make unzip; \
  rm -rf /var/lib/apt/lists/*;