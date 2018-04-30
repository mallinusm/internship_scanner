ifeq (run, $(firstword $(MAKECMDGOALS)))
  run_args := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
  $(eval $(run_args):;@true)
endif

help: ## Show help
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-10s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'

install: ## Install the application
    sudo apt-get install python2 python2-pip
    sudo pip install virtualenv
	virtualenv --no-site-packages --distribute .env
	. .env/bin/activate
	pip2 install -r requirements.txt

run: ## Run the application
	.env/bin/python2 -c "from Scanner.Application import Application; Application.start()"

.PHONY:help install run
.DEFAULT_GOAL=help
SHELL:=/bin/bash
