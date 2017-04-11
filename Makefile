.PHONY: all test install clean

all:
	@echo Available targets: install, test

install:
	pip install -U -r requirements.txt -e .

test:
	@[ -z $$VIRTUAL_ENV ] && echo 'Acticate gcalendar virtualenv.' || python -m unittest discover
