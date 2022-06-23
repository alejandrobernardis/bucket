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
COMPILER_IMAGE="py-pb-compiler:local"

# .github
GH_IMAGE_DST:="${GH_IMAGE}:v$(shell date +'%Y.%m.%d')-rc"

# === functions ================================================================
define f_build
	@docker buildx build $(1) \
	  --file $(2) \
	  --platform ${PLATFORM} \
	  --progress ${PROGRESS} \
	  --build-arg PY_VERSION=${PY_VERSION} \
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
.PHONY: grpc
grpc: ## Run GRPC server
	$(run_cmd) -p 50051:50051 -v ${PWD}/.env:/app/.env:ro ${IMAGE_LCL}
.PHONY: check-deps
check-deps: ## List of dependencies
	$(run_cmd) ${IMAGE_LCL} pip list -v
run_cmd:=@docker run --rm -ti

# === protobuf =================================================================
proto: ## Compile all protocols (alias `p`)
	@docker run --rm -ti -u ${UID}:${GID} -v ${SRC_PATH}:${WORKDIR}:rw ${COMPILER_IMAGE} sh -c '\
	  pth="$(WORKDIR)/src"; \
	  for item in `find $$pth -type f -name "*.proto"`; do \
	  	python -m grpc_tools.protoc \
	  	  --proto_path=$$pth \
	  	  --proto_path=/app/third_party \
	      --python_out=$$pth \
	      --grpc_python_out=$$pth \
	    $$item; \
	  done;'
.PHONY: p
p: proto
.PHONY: proto-build-compiler
proto-build-compiler: build-compiler proto ## Make compiler first and then compile all protocols

# === clean ====================================================================
.PHONY: clean
clean: ## Cleans generated files
	@find . -type f -name '*_pb2.py' -delete
	@find . -type f -name '*_pb2_grpc.py' -delete
	@sudo rm -f ${PWD}/certs/*
	@sudo rm -fr ${PWD}/.cache ${PWD}/.data
	@docker buildx prune -f

# === first ====================================================================
.PHONY: first
first: dotenv proto-build-compiler build-no-cache ## Creates compiler and tries to compile the project (start here)
	@python -m virtualenv .venv
	@poetry shell
.PHONY: dotenv
dotenv: ## Creates (dot)env file
	@cp -f ${PWD}/example.env ${PWD}/.env

# === help =====================================================================
.PHONY: help h
help:
	@printf '\n \033[33mCommand `$(PROJECT_NAME)` help - \033[m\n\n'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' ${PWD}/Makefile | awk \
	  'BEGIN {FS = ":.*?## "}; {printf "\033[37m + \033[34m%-20s\033[37m %s\n", $$1, $$2}'
	@printf '\n\033[m'
h: help
