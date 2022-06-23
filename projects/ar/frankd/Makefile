#!/usr/bin/env make

# --- variables ----------------------------------------------------------------

# .user
UID=$(shell id -u)
GID=$(shell id -g)

# .env
PWD=$(CURDIR)
ENV_FILE:=${PWD}/example.env
ifneq ("$(wildcard ${PWD}/.env)","")
	ENV_FILE:=${PWD}/.env
endif
$(eval include ${ENV_FILE})
$(eval export sed 's/=.*//' ${ENV_FILE})

# .paths
DOCKERFILE:=${PWD}/Dockerfile
SRC_PATH:=${PWD}

# .docker
TARGET="image"
PLATFORM="linux/amd64"
PROGRESS="plain"
IMAGE_PRD=${RG_HOST}/public/${PROJECT_NAME}:latest

# --- targets ----------------------------------------------------------------
.PHONY: run r
run: ## Just run (alias: `r`)
	@docker run --rm --user frank -ti \
	  -v ${SSH_PATH}:/home/frank/.ssh:ro \
	  -v ${CONFIG_PATH}:/home/frank/.frankdrc:ro \
	  -v ${DATA_PATH}:/var/data:rw \
	  -v /var/run/docker.sock:/var/run/docker.sock \
	  -e DOCKER_GROUP_ID=${GROUP_ID} \
	  -e GH_ACCESS_TOKEN=${GH_ACCESS_TOKEN} \
	  -e GH_PROTOCOL=${GH_PROTOCOL} \
	  ${IMAGE_LCL}
r: run

.PHONY: run-first rf
run-first: build frankdrc run ## Build image, create config file and run (alias: `rf`)
rf: run-first

.PHONY: build-run br
build-run: build run ## Build image and run (alias: `be`)
br: build-run

.PHONY: build b
build: ## Build image (alias: `b`)
	$(call f_build,${SRC_PATH},${DOCKERFILE},${IMAGE_LCL},${TARGET},${BUILD_ARGS})
b: build

.PHONY: build-no-cache bnc
build-no-cache: ## Build non cache image (alias: `bnc`)
	$(call f_build,${SRC_PATH},${DOCKERFILE},${IMAGE_LCL},${TARGET},--no-cache)
bnc: build-no-cache

.PHONY: push p
push: ## Push image to registry (alias: `p`)
	docker tag ${IMAGE_LCL} ${IMAGE_PRD}
	docker push ${IMAGE_PRD}
p: push

.PHONY: frankdrc
frankdrc: ## Create the frankd configuration from the example
	@cp -f ${PWD}/example.env ${CONFIG_PATH}

.PHONY: install
install: ## Install frankd
	@sudo cp -f ${PWD}/bin/frankd /usr/local/bin/frankd
	@sudo chmod +x /usr/local/bin/frankd

.PHONY: uninstall
uninstall: ## Uninstall frankd
	@sudo rm -f /usr/local/bin/frankd

# ============================================================================ #
# === hidden ================================================================= #
# ============================================================================ #
.PHONY: help h
help:
	@printf '\n \033[33mCommand `$(PROJECT_NAME)` help - \033[m\n\n'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' ${PWD}/Makefile | awk \
	  'BEGIN {FS = ":.*?## "}; {printf "\033[37m + \033[34m%-20s\033[37m %s\n", $$1, $$2}'
	@printf '\n\033[m'
h: help

# --- functions ----------------------------------------------------------------
define f_build
	@docker buildx build $(1) \
	  --file $(2) \
	  --platform ${PLATFORM} \
	  --progress ${PROGRESS} \
	  --build-arg GH_ACCESS_TOKEN=${GH_ACCESS_TOKEN} \
	  --build-arg GH_PROTOCOL=${GH_PROTOCOL} \
	  --tag $(3) \
	  --target $(4) $(5)
endef
