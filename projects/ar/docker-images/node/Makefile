#!/usr/bin/env make

# --- variables ----------------------------------------------------------------
UID=$(shell id -u)
GID=$(shell id -g)
PWD=$(CURDIR)

# environment
ENV_FILE:=${PWD}/../example.env
ifneq ("$(wildcard ${PWD}/../.env)","")
	ENV_FILE:=${PWD}/../.env
endif
$(eval include ${ENV_FILE})
$(eval export sed 's/=.*//' ${ENV_FILE})

# repository
REPOSITORY=${GH_IMAGE_REGISTRY}/${GH_IMAGE_REPOSITORY}
IMAGE=node
COMMIT=$(shell git describe --always)

.PHONY: all build b push p
# --- targets ------------------------------------------------------------------
all: build push
build:
	@docker buildx build ${PWD} \
	  --file ${PWD}/Dockerfile \
	  --progress plain \
	  --build-arg ND_VERSION=${ND_VERSION} \
	  --build-arg ND_PATCH=${ND_PATCH} \
	  --build-arg COMMIT=${COMMIT} \
	  --tag ${REPOSITORY}/${IMAGE}:v${ND_VERSION}${ND_PATCH}
b: build
push:
	docker push ${REPOSITORY}/${IMAGE}:v${ND_VERSION}${ND_PATCH}
p: push
