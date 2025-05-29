.PHONY: axonius_dir install playwright test all

# Allow override from command line like: make test CONTAINER_NAME=my_container
CONTAINER_NAME ?=

# Detect if we should run in container
ifeq ($(CONTAINER_NAME),)
    CMD_PREFIX =
else
    CMD_PREFIX = docker exec $(CONTAINER_NAME)
endif

axonius_dir:
	@if [ "$$(basename $$(pwd))" != "axonius" ]; then \
		mkdir -p axonius; \
	fi

install: axonius_dir
	@echo "Installing dependencies..."
	$(CMD_PREFIX) pip install -r requirements.txt

playwright: install
	@echo "Installing Playwright dependencies..."
	$(CMD_PREFIX) python -m playwright install --with-deps

test: playwright
	@echo "Running tests..."
	$(CMD_PREFIX) pytest -s -v

all: test
