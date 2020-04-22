PROJECT_NAME = watchdog
PROJECT_WATCHDOG_PATH ?= $(shell pwd)
DOCKER_RUN = docker run -it --rm --name $(PROJECT_NAME)

build:
	docker build -t $(PROJECT_NAME) $(PROJECT_WATCHDOG_PATH)

start:
	$(DOCKER_RUN) $(PROJECT_NAME) start

%:
	@: