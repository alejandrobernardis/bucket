#!/usr/bin/env make

# === variables ================================================================
# .user
UID=$(shell id -u)
GID=$(shell id -g)

# .go
GO_VERSION=1.17

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
TPY_PATH:=${PWD}/third_party

# .docker
TARGET="image"
PLATFORM="linux/amd64"
PROGRESS="plain"
WORKDIR=/app
COMPILER_IMAGE="go-pb-compiler:local"

# .github
GH_IMAGE_DST:="${GH_IMAGE}:v$(shell date +'%Y.%m.%d')-rc"

# === functions ================================================================
define f_build
	@docker buildx build $(1) \
	  --file $(2) \
	  --platform ${PLATFORM} \
	  --progress ${PROGRESS} \
	  --build-arg GO_VERSION=${GO_VERSION} \
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
.PHONY: build-minimal
build-minimal: ## Compile service with minimal approach
	$(call f_build,${SRC_PATH},${DOCKERFILE},${IMAGE_LCL},minimal,${BUILD_ARGS})
.PHONY: build-compiler
build-compiler: ## Make compiler (COMPILER_IMAGE)
	$(call f_build,${SRC_PATH},${DOCKERFILE},${COMPILER_IMAGE},compiler,${BUILD_ARGS})

# === protobuf =================================================================
.PHONY: proto
proto: ## Compile all protocols (alias `p`)
	@docker run --rm -ti -u ${UID}:${GID} -v ${SRC_PATH}:${WORKDIR}:rw ${COMPILER_IMAGE} sh -c '\
	  pth="$(WORKDIR)/proto";\
	  for item in `find $$pth -type f -name "*.proto"`; do \
	    protoc --proto_path=$$pth --proto_path=$(WORKDIR)/third_party \
	    --go_out=$$pth --go_opt=paths=source_relative \
	    --go-grpc_out=$$pth --go-grpc_opt=paths=source_relative \
	    --grpc-gateway_out=$$pth --grpc-gateway_opt=paths=source_relative \
	    $$item; \
	  done;'
.PHONY: p
p: proto
.PHONY: proto-build-compiler
proto-build-compiler: build-compiler proto ## Make compiler first and then compile all protocols

# === local ====================================================================
.PHONY: grpc
grpc: ## Run GRPC server
	@$(cmd_local)
.PHONY: grpc-help
grpc-help: ## Run GRPC server help
	@$(cmd_local) -help
.PHONY: gateway
gateway: ## Run GATEWAY server
	@$(cmd_local) -mode=gateway
cmd_local:=go run ${PWD}/cmd/main.go -env-filename=${ENV_FILE}

# === go =======================================================================
.PHONY: tidy
tidy: ## Add missing and remove unused modules
	@go mod tidy
.PHONY: vendor
vendor: ## Make vendored copy of dependencies
	@go mod vendor
.PHONY: tidy-vendor
tidy-vendor: tidy vendor ## Add the missing modules and remove the unused ones, then make a copy of the dependencies

# === certs ====================================================================
.PHONY: certs
certs: ## Creates SSL certificates
	@bash ${PWD}/scripts/certs.sh

# === clean ====================================================================
.PHONY: clean
clean: ## Cleans go and generated files
	@go clean
	@find . -type f -name '*.pb.go' -delete
	@find . -type f -name '*.pb.gw.go' -delete
	@sudo rm -f ${PWD}/__debug_bin
	@sudo rm -f ${PWD}/certs/*
	@sudo rm -fr ${PWD}/build

# === first ====================================================================
.PHONY: first
first: dotenv proto-build-compiler build-no-cache ## Creates compiler and tries to compile the project (start here)
.PHONY: dotenv
dotenv: ## Creates (dot)env file
	@cp -f ${PWD}/example.env ${PWD}/.env
	
# === help =====================================================================
.PHONY: help
help:
	@printf '\n \033[33mProject `${PROJECT_NAME}` help - \033[m\n\n'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' ${PWD}/Makefile | awk \
	  'BEGIN {FS = ":.*?## "}; {printf "\033[37m + \033[34m%-20s\033[37m %s\n", $$1, $$2}'
	@printf '\n\033[m'
.PHONY: h
h: help

# === not documented ===========================================================
# help ... https://github.com/ktr0731/evans
.PHONY: evans-local
evans-local:
	$(evans-cmd) --host ${IP} --port 50051 -r repl
.PHONY: evans-container
evans-container:
	$(evans-cmd) --host 172.255.254.200 --port 15051 -r repl
evans-cmd:=@docker run --rm -ti alejandrobernardis/evans:latest
