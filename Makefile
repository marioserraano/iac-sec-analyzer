.PHONY: install run test clean format

install:
	pip install -r requirements.txt

run:
	python run.py vulnerable.tf

test:
	pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache

format:
	black src/