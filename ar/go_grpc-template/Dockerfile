# syntax = docker/dockerfile:1.2
ARG GO_VERSION=1.17
FROM --platform=${BUILDPLATFORM} golang:${GO_VERSION}-buster AS compiler
ENV CGO_ENABLED=0
ENV PATH="/go/bin:$PATH"
WORKDIR /app
RUN rm -f /etc/apt/apt.conf.d/docker-clean
RUN --mount=type=cache,target=/var/cache/apt set -ex; apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends \
      --assume-yes protobuf-compiler ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && protoc --version \
    && go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.27.1 \
    && go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.1.0 \
    && go install github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway@v1.16.0;

FROM compiler AS base
COPY go.* .
RUN --mount=type=cache,target=/go/pkg/mod set -ex; go mod download;

FROM base AS builder
ARG TARGETOS
ARG TARGETARCH
RUN --mount=target=.,readwrite \
    --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build set -ex; \
    for item in $(find /app/proto -type f -name "*.proto"); do \
      protoc --proto_path=/app/proto --proto_path=/app/third_party \
        --go_out=/app/proto --go_opt=paths=source_relative \
        --go-grpc_out=/app/proto --go-grpc_opt=paths=source_relative \
        --grpc-gateway_out=/app/proto --grpc-gateway_opt=paths=source_relative \
        ${item}; \
    done; \
    GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
      go build -o /tmp/server /app/cmd/main.go;

FROM debian:buster-slim AS image
COPY --from=builder /tmp/server /usr/bin/server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY docker-entrypoint.sh /
ARG GROUPID=1000
ARG GROUPNAME=frank
ARG USERID=1000
ARG USERNAME=frank
RUN set -ex; \
    groupadd -g ${GROUPID} ${GROUPNAME} \
      && useradd -M -d /app -s /bin/bash -u ${USERID} -g ${GROUPNAME} ${USERNAME} \
      && chown ${USERID}:${GROUPID} /usr/bin/server /docker-entrypoint.sh; \
    chmod +x /usr/bin/server /docker-entrypoint.sh;
EXPOSE 50051 8080
WORKDIR /app
USER ${USERID}:${GROUPID}
ENTRYPOINT ["/docker-entrypoint.sh"]
STOPSIGNAL SIGTERM
CMD []

FROM scratch AS minimal
COPY --from=builder /tmp/server /usr/bin/server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
EXPOSE 50051 8080
WORKDIR /tmp
STOPSIGNAL SIGTERM
CMD ["/usr/bin/server"]
