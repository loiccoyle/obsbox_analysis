venv:
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

update_dependencies:
	pip freeze > requirements.txt

.PHONY: venv update_dependencies
