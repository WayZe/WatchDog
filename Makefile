PROJECT_NAME = watchdog
DOCKER_RUN = docker run -it --rm --name $(PROJECT_NAME)

build:
	docker build -t $(PROJECT_NAME) -f $(shell pwd)/docker/Dockerfile .

start:
	$(DOCKER_RUN) -v "$(shell pwd)":"/opt" $(PROJECT_NAME) start

%:
	@:
