# META ]--------------------------------------------------------------------------------------------
.PHONY: help.stub help
help.stub: help

RED="\033[91m"
END="\033[0m"

help:
	@echo "help         Display this message."
	@echo "run          Generate a pinwheel tiling fractal"
	@echo "test         Run testing suite."
	@echo "clean        Standardize repository."
	@echo "deps         Install dependencies."

# EXAMPLES ]----------------------------------------------------------------------------------------
.PHONY: run
run:
	python main.py 3

# CORE ]--------------------------------------------------------------------------------------------
.PHONY: test clean deps

test:
	black --check .
	pylint *.py

clean:
	black .

deps:
	pip install -r requirements.txt
