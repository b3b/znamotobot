test:
	@tox

format:
	black znamotobot
	isort znamotobot

pip-tools:
	@pip install pip-tools

pip-install: pip-tools
	@pip install \
	-r requirements/dev.txt

pip-compile: pip-tools
	@rm -f requirements*.txt
	@pip-compile requirements/base.in
	@pip-compile requirements/dev.in

pip-sync: pip-tools
	@pip-sync requirements/*.txt


.PHONY: test format pip-tools pip-install pip-compile pip-sync
