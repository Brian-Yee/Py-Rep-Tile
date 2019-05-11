# META ]--------------------------------------------------------------------------------------------
.PHONY: help.stub help
help.stub: help

RED="\033[91m"
END="\033[0m"

help:
	@echo "help         Display this message."
	@echo "pinwheel     Generate a pinwheel tiling."
	@echo "sphinx       Generate a sphinx tiling."
	@echo "test         Run testing suite."
	@echo "clean        Standardize repository."
	@echo "deps         Install dependencies."

# EXAMPLES ]----------------------------------------------------------------------------------------
.PHONY: pinwheel sphinx
pinwheel:
	time python main.py pinwheel 4

sphinx:
	time python main.py sphinx 4

# CORE ]--------------------------------------------------------------------------------------------
.PHONY: test clean deps

test:
	black --check .
	pylint *.py src

clean:
	black .
	-rm profile_stats

deps:
	pip install -r requirements.txt
