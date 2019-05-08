# META ]--------------------------------------------------------------------------------------------
.PHONY: help.stub help
help.stub: help

RED="\033[91m"
END="\033[0m"

help:
	@echo "help         Display this message."
	@echo "run          Generate a pinwheel tiling."
	@echo "rect         Generate a pinwheel tiling as a rectangular mural."
	@echo "profile      Profile Code."
	@echo "test         Run testing suite."
	@echo "clean        Standardize repository."
	@echo "deps         Install dependencies."

# EXAMPLES ]----------------------------------------------------------------------------------------
.PHONY: run rect
run:
	time python main.py 6

rect:
	time python main.py 6 --rectangle y

# CORE ]--------------------------------------------------------------------------------------------
.PHONY: test clean deps

profile:
	python -m cProfile -s cumtime main.py 4 > profile_stats
	head -100 profile_stats

test:
	black --check .
	pylint *.py src

clean:
	black .
	-rm profile_stats

deps:
	pip install -r requirements.txt
