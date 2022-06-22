# syntax=docker/dockerfile:1.2
FROM debian:11-slim AS base

# fix
RUN rm -f /etc/apt/apt.conf.d/docker-clean; \
  echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' \
    > /etc/apt/apt.conf.d/keep-cache \
;

# deps
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
  apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --assume-yes \
    ca-certificates curl gcc git uuid-dev openssh-client make zsh sudo \
  && rm -rf /var/lib/apt/lists/* \
;

# github cli
RUN gh_version='2.9.0'; \
curl -fsSL https://github.com/cli/cli/releases/download/v${gh_version}/gh_${gh_version}_linux_amd64.tar.gz \
    -o /tmp/gh_${gh_version}_linux_amd64.tar.gz \
  && tar xfvz /tmp/gh_${gh_version}_linux_amd64.tar.gz -C /tmp \
  && mv /tmp/gh_${gh_version}_linux_amd64/bin/gh /usr/local/bin/gh \
  && chmod +x /usr/local/bin/gh \
;

# micro
RUN mc_version='2.0.10'; \
curl -fsSL https://github.com/zyedidia/micro/releases/download/v${mc_version}/micro-${mc_version}-linux64.tar.gz \
    -o /tmp/micro-${mc_version}-linux64.tar.gz \
  && tar xfvz /tmp/micro-${mc_version}-linux64.tar.gz -C /tmp \
  && mv /tmp/micro-${mc_version}/micro /usr/local/bin/micro \
  && yes | rm -fr /tmp/micro-${mc_version}* \
  && chmod +x /usr/local/bin/micro \
; \
for x in gotham-colors comment editorconfig filemanager quoter jump detectindent; do \
  micro -plugin install ${x}; \
done \
;

# build x
RUN bx_version='0.8.2'; \
mkdir -p /usr/local/lib/docker/cli-plugins \
  && curl -fsSL https://github.com/docker/buildx/releases/download/v${bx_version}/buildx-v${bx_version}.linux-amd64 \
    -o /usr/local/lib/docker/cli-plugins/docker-buildx \
  && chmod +x /usr/local/lib/docker/cli-plugins/docker-buildx \
;

# completions
RUN mkdir -p /usr/local/share/zsh/site-functions; \
gh completion -s zsh > /usr/local/share/zsh/site-functions/_gh; \
curl -L https://raw.githubusercontent.com/docker/cli/v20.10.7/contrib/completion/zsh/_docker -o /usr/local/share/zsh/site-functions/_docker; \
curl -L https://raw.githubusercontent.com/docker/compose/1.29.2/contrib/completion/zsh/_docker-compose -o /usr/local/share/zsh/site-functions/_docker-compose;

# docker
COPY --from=docker:dind /usr/local/bin/docker /usr/local/bin/

# clean
RUN rm -fr /tmp/*

# user
FROM base AS user
COPY docker-entrypoint.sh /docker-entrypoint
RUN chmod +x /docker-entrypoint;
RUN useradd --create-home --user-group frank \
  && echo "%frank ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers.d/99-NOPASSWD; \
     echo "Defaults !env_reset" > /etc/sudoers.d/00-ENV-RESET \
;
USER frank
WORKDIR /home/frank
STOPSIGNAL SIGTERM
ENTRYPOINT ["/docker-entrypoint"]
CMD ["zsh", "--login"]

# custom
FROM user AS image
COPY --chown=frank:frank frank /home/frank
RUN make -C /home/frank/.source install
