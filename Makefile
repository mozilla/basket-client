all: help

clean:
	rm -rf basket_client.egg-info build/ dist/

test:
	hatch run tox

lint:
	hatch run lint:all

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean         to remove all build, test, coverage and Python artifacts"
	@echo "  test          to run tests on every Python version with tox"
	@echo "  lint          to run all linters"


.PHONY: all clean test lint