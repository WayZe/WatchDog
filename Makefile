PROJECT_NAME = watchdog
DOCKER_RUN = docker run -it --rm --name $(PROJECT_NAME)
HEROKU_PROJECT = registry.heroku.com/exchangewatchdog

build:
	docker build -t $(PROJECT_NAME) -f $(shell pwd)/docker/Dockerfile .

start: make build
	$(DOCKER_RUN) -v "$(shell pwd)":"/opt" $(PROJECT_NAME) start

deploy_heroku:
	docker build -t $(HEROKU_PROJECT)/$(PROJECT_NAME) -f $(shell pwd)/docker/Dockerfile .
	docker push $(HEROKU_PROJECT)/$(PROJECT_NAME)
	heroku container:rm $(PROJECT_NAME)
	heroku container:release $(PROJECT_NAME)
	heroku ps:scale $(PROJECT_NAME)=1

envs_heroku:
	heroku config:set $$(cat .env | sed '/^$$/d; /#[[:print:]]*$$/d')

%:
	@:
