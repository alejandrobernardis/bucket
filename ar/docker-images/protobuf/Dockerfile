#syntax=docker/dockerfile:1.2
ARG GO_VERSION=1.18
ARG GO_PATCH=.2

FROM --platform=linux/amd64 docker.pkg.github.com/aysa-prmgt/docker-images/go:v${GO_VERSION}${GO_PATCH} AS base
ARG GO_VERSION
ARG GO_PATCH
ARG PB_VERSION=3.20
ARG PB_PATCH=.1
ARG PB_GEN_VERSION=1.28
ARG PB_GEN_GRPC_VERSION=1.2
ARG COMMIT=0

LABEL \
  app.aysa.prmgt.lang=go \
  app.aysa.prmgt.lang.version=${GO_VERSION} \
  app.aysa.prmgt.lang.patch=${GO_PATCH} \
  app.aysa.prmgt.pb=protoc \
  app.aysa.prmgt.pb.version=${PB_VERSION} \
  app.aysa.prmgt.pb.patch=${PB_PATCH} \
  app.aysa.prmgt.commit=${COMMIT} \
  app.aysa.prmgt.os=debian

RUN \
  wget -O /tmp/pb.zip https://github.com/protocolbuffers/protobuf/releases/download/v${PB_VERSION}${PB_PATCH}/protoc-${PB_VERSION}${PB_PATCH}-linux-x86_64.zip; \
  unzip /tmp/pb.zip -d /usr; \
  rm -f /tmp/pb.zip;
RUN --mount=type=cache,target=/go/pkg/mod \
  go install google.golang.org/protobuf/cmd/protoc-gen-go@v${PB_GEN_VERSION}; \
  go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v${PB_GEN_GRPC_VERSION}; \
