PYPI_SERVER = pypitest

.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test:
	@tox

.PHONY: local-test
local-test:
	@tox --skip-missing-interpreters

.PHONY: release
release: sdist wheel clean ## Package and upload release
	@echo "+ $@"
	@twine upload -r $(PYPI_SERVER) dist/*

.PHONY: sdist
sdist: clean ## Build sdist distribution
	@echo "+ $@"
	@pipenv run python setup.py sdist
	@ls -l dist

.PHONY: wheel
wheel: clean ## Build bdist_wheel distribution
	@echo "+ $@"
	@pipenv run python setup.py bdist_wheel
	@ls -l dist

.PHONY: clean
clean: ## Remove all artifacts 
	@echo "+ $@"

requirements-dev.txt: Pipfile.lock ## Generate requirements file for developing from Pipenv.
	@echo "+ $@"
	@pipenv lock --requirements --dev > requirements-dev.txt

requirements.txt: Pipfile.lock ## Generate requirements file from Pipenv
	@echo "+ $@"
	@pipenv lock --requirements > requirements.txt
