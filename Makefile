ifeq (run, $(firstword $(MAKECMDGOALS)))
  run_args := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
  $(eval $(run_args):;@true)
endif

help: ## Show help
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-10s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'

install: ## Install the application
	virtualenv --no-site-packages --distribute .env
	. .env/bin/activate
	pip install -r requirements.txt

run: ## Run the application
	.env/bin/python2 scanner.py $(run_args)

.PHONY:help install run
.DEFAULT_GOAL=help
SHELL:=/bin/bash
