#!/usr/bin/env make

UID=$(shell id -u)
GID=$(shell id -g)
PWD=$(CURDIR)

ENV_FILE:=${PWD}/example.env
ifneq ("$(wildcard ${PWD}/.env)","")
	ENV_FILE:=${PWD}/.env
endif
$(eval include ${ENV_FILE})
$(eval export sed 's/=.*//' ${ENV_FILE})

IMAGES=go node protobuf python

# -
.PHONY: all build push login
all: login
	$(call f_action)
build:
	$(call f_action,build)
push:
	$(call f_action,push)
login:
	@docker login -u ${GH_USERNAME} -p ${GH_ACCESS_TOKEN} ${GH_IMAGE_REGISTRY}

# -
define f_action
	@$(foreach var,$(IMAGES),make -C $(var) $(1);)
endef
