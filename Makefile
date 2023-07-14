all: help

clean:
	hatch clean

test:
	hatch run test:cov

lint:
	hatch run lint:check

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean         to remove all build, test, coverage and Python artifacts"
	@echo "  test          to run tests on every Python version via hatch"
	@echo "  lint          to run all linters"


.PHONY: all clean test lint
