#syntax=docker/dockerfile:1.2
ARG GO_VERSION=1.18
ARG GO_PATCH=.2

FROM --platform=linux/amd64 golang:${GO_VERSION}${GO_PATCH}-bullseye AS base
ARG GO_VERSION
ARG GO_PATCH
ARG COMMIT=0

LABEL \
  app.aysa.prmgt.lang=go \
  app.aysa.prmgt.lang.version=${GO_VERSION} \
  app.aysa.prmgt.lang.patch=${GO_PATCH} \
  app.aysa.prmgt.commit=${COMMIT} \
  app.aysa.prmgt.os=debian

RUN rm -f /etc/apt/apt.conf.d/docker-clean
RUN --mount=type=cache,target=/var/cache/apt \
  apt-get update; \
  DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --assume-yes \
    ca-certificates git make unzip; \
  rm -rf /var/lib/apt/lists/*;