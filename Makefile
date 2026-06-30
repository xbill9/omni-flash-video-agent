# Configuration - Update these or override via environment variables
GEMINI_OMNI_MODEL ?= gemini-omni-flash-preview


install:
	pip install -r requirements.txt

run:
	python server.py

test:
	python test_agent.py

lint:
	ruff check .
	ruff format --check .
	mypy .

clean:
	rm -rf __pycache__
	rm -rf .mypy*
	rm -rf .ruf*
	find . -type d -name "__pycache__" -exec rm -rf {} +


.PHONY: install run test clean 
