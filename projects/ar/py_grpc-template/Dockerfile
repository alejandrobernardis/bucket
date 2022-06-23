# syntax = docker/dockerfile:1.2
ARG PY_VERSION=3.9
FROM --platform=${BUILDPLATFORM} python:${PY_VERSION}-buster AS compiler
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PATH=/root/bin:/root/.local/bin:$PATH
RUN rm -f /etc/apt/apt.conf.d/docker-clean; \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache;
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt set -ex; \
    apt-get update \
      && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends \
        --assume-yes ca-certificates curl gcc git uuid-dev openssh-client \
      && rm -rf /var/lib/apt/lists/*; \
    python -m pip install --upgrade --no-cache-dir pip poetry \
        grpcio-tools googleapis-common-protos;

FROM compiler AS deps
COPY . .
RUN --mount=type=cache,target=/root/.local set -ex; \
    for item in `find /app/src -type f -name "*.proto"`; do \
        python -m grpc_tools.protoc \
            --proto_path=/app/src \
            --proto_path=/app/third_party \
            --python_out=/app/src \
            --grpc_python_out=/app/src \
        $item; \
    done; \
    poetry export --no-interaction --no-ansi --format requirements.txt --output /app/requirements.txt \
      && pip wheel --no-cache-dir --wheel-dir /wheels -r /app/requirements.txt;

# service
FROM python:${PY_VERSION}-slim-buster AS image
WORKDIR /app
ARG GROUPID=1000 \
    GROUPNAME=frank \
    USERID=1000 \
    USERNAME=frank
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PYTHONPATH=/app:/app/proto:$PYTHONPATH \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PATH=/app/bin:/app/.local/bin:$PATH
COPY docker-entrypoint.sh /
COPY --from=deps --chown=$USERID:$GROUPID /app/src/ .
COPY --from=deps --chown=$USERID:$GROUPID /wheels /wheels
COPY --from=deps /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
RUN set -ex; \
    groupadd -g $GROUPID $GROUPNAME \
      && useradd -M -d /app -s /bin/bash -u $USERID -g $GROUPNAME $USERNAME \
      && chown --recursive $USERID:$GROUPID /app; \
    chmod +x /docker-entrypoint.sh;
USER $USERID:$GROUPID
RUN pip install --user --no-cache /wheels/* \
      && rm -fr `find /app -name __pycache__`;
EXPOSE 50051 8080 8000 5000
ENTRYPOINT ["/docker-entrypoint.sh"]
STOPSIGNAL SIGTERM
CMD []
