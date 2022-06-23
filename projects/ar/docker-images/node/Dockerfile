#syntax=docker/dockerfile:1.2
ARG ND_VERSION=18.1
ARG ND_PATCH=.0

FROM --platform=linux/amd64 node:${ND_VERSION}${ND_PATCH}-bullseye AS base
ARG ND_VERSION
ARG ND_PATCH
ARG COMMIT=0

LABEL \
  metadata.lang=node \
  metadata.lang.version=${ND_VERSION} \
  metadata.lang.patch=${ND_PATCH} \
  metadata.commit=${COMMIT} \
  metadata.os=debian

RUN rm -f /etc/apt/apt.conf.d/docker-clean
RUN --mount=type=cache,target=/var/cache/apt \
  apt-get update; \
  DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --assume-yes \
    ca-certificates git make unzip; \
  rm -rf /var/lib/apt/lists/*;
