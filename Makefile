PROJECT_NAME = watchdog
DOCKER_RUN = docker run -it --rm --name $(PROJECT_NAME) --env-file=.env
HEROKU_PROJECT = registry.heroku.com/exchangewatchdog

build:
	docker build -t $(PROJECT_NAME) -f $(shell pwd)/docker/Dockerfile .

start:
	$(DOCKER_RUN) --link redis_watchdog:redis_watchdog -v "$(shell pwd)":"/opt" $(PROJECT_NAME)

remove_heroku:
	heroku container:rm $(PROJECT_NAME)

deploy_heroku:
	docker build -t $(HEROKU_PROJECT)/$(PROJECT_NAME) -f $(shell pwd)/docker/Dockerfile .
	docker push $(HEROKU_PROJECT)/$(PROJECT_NAME)
	heroku container:release $(PROJECT_NAME)
	heroku ps:scale $(PROJECT_NAME)=1

envs_heroku:
	heroku config:set $$(cat .env | sed '/^$$/d; /#[[:print:]]*$$/d')

redis:
	docker run --rm --name redis_watchdog -d redis:6.0.8-alpine

%:
	@:
