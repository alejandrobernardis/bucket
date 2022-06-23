#!/usr/bin/env make

# === variables ================================================================
# .user
UID=$(shell id -u)
GID=$(shell id -g)

# .py
PY_VERSION=3.9

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
SSH_PATH:=${PWD}/.ssh
TPY_PATH:=${PWD}/third_party

# .docker
TARGET="image"
PLATFORM="linux/amd64"
PROGRESS="plain"
WORKDIR=/app
COMPILER_IMAGE="py-compiler:local"

# .github
GH_IMAGE_DST:="${GH_IMAGE}:v$(shell date +'%Y.%m.%d')-rc"

# === functions ================================================================
define f_build
	@docker buildx build $(1) \
	  --file $(2) \
	  --platform ${PLATFORM} \
	  --progress ${PROGRESS} \
	  --ssh default="${SSH_PATH}/id_rsa_1636457559" \
	  --build-arg PY_VERSION=${PY_VERSION} \
	  --build-arg PY_CORE=${PY_CORE} \
	  --build-arg GH_ACCESS_TOKEN=${GH_ACCESS_TOKEN} \
	  --build-arg GH_PROTOCOL=${GH_PROTOCOL} \
	  --tag $(3) \
	  --target $(4) $(5)
endef

# === build ====================================================================
.PHONY: build
build: ## Compile service (alias `b`)
	$(call f_build,${SRC_PATH},${DOCKERFILE},${IMAGE_LCL},${TARGET},${BUILD_ARGS})
.PHONY: b
b: build
.PHONY: build-no-cache
build-no-cache: ## Compile service without cache (alias `bnc`)
	$(call f_build,${SRC_PATH},${DOCKERFILE},${IMAGE_LCL},${TARGET},--no-cache)
.PHONY: bnc
bnc: build-no-cache
.PHONY: build-compiler
build-compiler: ## Make compiler (COMPILER_IMAGE)
	$(call f_build,${SRC_PATH},${DOCKERFILE},${COMPILER_IMAGE},compiler,${BUILD_ARGS})

# === run ======================================================================
check-deps: ## List of dependencies
	$(run_cmd) ${IMAGE_LCL} pip list -v
run_cmd:=@docker run --rm -ti

# === deps =====================================================================
.PHONY: core-uninstall
core-uninstall: ## Uninstall Core Framework
	pip uninstall -y core
.PHONY: core-shh
core-ssh: core-uninstall ## Install Core Framework via SSH
	pip install -U git+ssh://git@${PY_CORE}
.PHONY: core-https
core-https: core-uninstall ## Install Core Framework via HTTPS
	pip install -U git+https://${GH_ACCESS_TOKEN}@${PY_CORE};
.PHONY: venv
venv: ## Make virtualenv
	@python -m virtualenv .venv

# === clean ====================================================================
.PHONY: clean
clean: ## Cleans generated files
	@sudo rm -f ${PWD}/certs/*
	@sudo rm -fr ${PWD}/.cache ${PWD}/.data
	@docker buildx prune -f

# === first ====================================================================
.PHONY: first
first: venv dotenv build-compiler build-no-cache ## Creates compiler and tries to compile the project (start here)
	@chmod 600 ${SSH_PATH}/*
.PHONY: dotenv
dotenv: ## Creates (dot)env file
	@cp -f ${PWD}/example.env ${PWD}/.env

# === help =====================================================================
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' ${PWD}/Makefile | awk \
	  'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: h
h: help
