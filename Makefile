PROJECT_NAME = watchdog
PERIODIC_NAME = periodic
DOCKER_RUN = docker run -it --rm --name $(PROJECT_NAME) --env-file=.env
HEROKU_PROJECT = registry.heroku.com/exchangewatchdog

build:
	docker build -t $(PROJECT_NAME) -f $(shell pwd)/docker/Dockerfile .

start:
	$(DOCKER_RUN) --link redis_watchdog:redis_watchdog -v "$(shell pwd)":"/opt" $(PROJECT_NAME)

remove_api:
	heroku container:rm $(PROJECT_NAME)

remove_periodic:
	heroku container:rm $(PERIODIC_NAME)

deploy_api:
	docker build -t $(HEROKU_PROJECT)/$(PROJECT_NAME) -f $(shell pwd)/docker/Dockerfile.api .
	docker push $(HEROKU_PROJECT)/$(PROJECT_NAME)
	heroku container:release $(PROJECT_NAME)
	heroku ps:scale $(PROJECT_NAME)=1

deploy_periodic:
	docker build -t $(HEROKU_PROJECT)/$(PERIODIC_NAME) -f $(shell pwd)/docker/Dockerfile.periodic .
	docker push $(HEROKU_PROJECT)/$(PERIODIC_NAME)
	heroku container:release $(PERIODIC_NAME)
	heroku ps:scale $(PERIODIC_NAME)=1

envs_heroku:
	heroku config:set $$(cat .env | sed '/^$$/d; /#[[:print:]]*$$/d')

redis:
	docker run --rm --name redis_watchdog -d redis:6.0.8-alpine

%:
	@:
