# Simple makefile

PYTHON ?= python
NOSETESTS ?= nosetests

all: clean

clean:
	find . -name "*.pyc" | xargs rm -f

test: clean build
	$(NOSETESTS)

trailing-spaces: 
	find -name "*.py" | xargs sed 's/^M$$//'
