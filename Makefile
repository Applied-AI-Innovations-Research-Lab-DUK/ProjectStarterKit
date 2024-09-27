install:
	poetry install

test:
	pytest tests/

run:
	poetry run python src/sample_project/main.py

docker-build:
	docker build -t sample_project:latest .

docker-run:
	docker run -p 8000:8000 sample_project:latest

compose-up:
	docker-compose up -d

compose-down:
	docker-compose down
