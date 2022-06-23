# syntax = docker/dockerfile:1.2
ARG PY_VERSION=3.9 \
    GH_PROTOCOL=ssh
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
ARG GH_ACCESS_TOKEN=

FROM compiler AS builder
COPY . .
RUN --mount=type=cache,target=/root/.local set -ex; \
    poetry export --no-interaction --no-ansi --format requirements.txt --output /app/requirements.txt \
      && pip wheel --no-cache-dir --wheel-dir /wheels -r /app/requirements.txt;

FROM builder AS deps-ssh
RUN mkdir -p -m 0600 ~/.ssh; ssh-keyscan github.com > ~/.ssh/known_hosts;
RUN --mount=type=ssh pip wheel --no-cache-dir --wheel-dir /wheels;

FROM builder AS deps-https
RUN pip wheel --no-cache-dir --wheel-dir /wheels;

FROM deps-${GH_PROTOCOL} AS deps

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
    chmod +x /docker-entrypoint.sh /app/bin/*;
USER $USERID:$GROUPID
RUN set -ex; \
    pip install --user --no-cache /wheels/* \
      && rm -fr `find /app -name __pycache__` \
      && pip list -v;
EXPOSE 8000 8080
ENTRYPOINT ["/docker-entrypoint.sh"]
STOPSIGNAL SIGTERM
CMD []
