import os
from pathlib import Path

# Define the project name
project_name = 'sample_project'

# List of directories to create
directories = [
    f'src/{project_name}/components',
    f'src/{project_name}/pipelines',
    f'src/{project_name}/utils',
    f'src/{project_name}/constants',
    f'src/{project_name}/entities',
    'config',
    'data/raw',
    'data/processed',
    'data/external',
    'docs',
    'notebooks/exploratory',
    'notebooks/experiments',
    'notebooks/production',
    'tests',
    'scripts',
    'templates',
    '.github/workflows',
]

# Files to create with sample content
files = {
    '.gitignore': """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]

# C extensions
*.so

# Distribution / packaging
.Python
env/
venv/
.build/
dist/
eggs/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.cache

# Jupyter Notebook
.ipynb_checkpoints

# Environments
.env
""",
    '.dockerignore': """
__pycache__/
*.py[cod]
env/
venv/
.idea/
.vscode/
.git/
""",
    'README.md': f"# {project_name.capitalize()}\n\nProject description goes here.",
    'LICENSE': "MIT License",
    'Dockerfile': f"""
# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY pyproject.toml poetry.lock /app/
RUN pip install --no-cache-dir poetry && poetry install --no-dev

# Copy source code
COPY src/ /app/src/

# Expose port (if running a web service)
EXPOSE 8000

# Command to run on container start
CMD ["poetry", "run", "python", "src/{project_name}/main.py"]
""",
    'docker-compose.yml': f"""
version: '3.8'
services:
  app:
    build: .
    container_name: {project_name}_app
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
  db:
    image: postgres:13
    container_name: {project_name}_db
    environment:
      - POSTGRES_USER=your_username
      - POSTGRES_PASSWORD=your_password
      - POSTGRES_DB=your_database
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
volumes:
  db_data:
""",
    'Makefile': f"""
install:
\tpoetry install

test:
\tpytest tests/

run:
\tpoetry run python src/{project_name}/main.py

docker-build:
\tdocker build -t {project_name}:latest .

docker-run:
\tdocker run -p 8000:8000 {project_name}:latest

compose-up:
\tdocker-compose up -d

compose-down:
\tdocker-compose down
""",
    'pyproject.toml': f"""
[tool.poetry]
name = "{project_name}"
version = "0.1.0"
description = "Description of your project"
authors = ["Your Name <you@example.com>"]
license = "MIT"

[tool.poetry.dependencies]
python = "^3.9"
numpy = "*"
pandas = "*"
scikit-learn = "*"
psycopg2 = "*"

[tool.poetry.dev-dependencies]
pytest = "*"
flake8 = "*"

[build-system]
requires = ["poetry>=1.0"]
build-backend = "poetry.masonry.api"
""",
    'config/config.yaml': """
default:
  data_path: data/processed/
  model_path: models/
  log_path: logs/
  database:
    host: db
    port: 5432
    user: your_username
    password: your_password
    db_name: your_database
""",
    'config/logging.yaml': """
version: 1
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    formatter: simple
    level: INFO
loggers:
  your_project_name:
    handlers: [console]
    level: INFO
    propagate: False
root:
  level: INFO
  handlers: [console]
""",
    f'src/{project_name}/__init__.py': "",
    f'src/{project_name}/main.py': f"""
import logging
from {project_name}.pipelines.train_pipeline import run_training_pipeline
from {project_name}.utils.logging import setup_logging

def main():
    setup_logging()
    logging.info("Starting the training pipeline.")
    run_training_pipeline()

if __name__ == "__main__":
    main()
""",
    f'src/{project_name}/components/__init__.py': "",
    f'src/{project_name}/components/data_ingestion.py': """
def ingest_data():
    # Placeholder for data ingestion logic
    print("Ingesting data...")
""",
    f'src/{project_name}/components/data_transformation.py': """
def transform_data():
    # Placeholder for data transformation logic
    print("Transforming data...")
""",
    f'src/{project_name}/components/model_trainer.py': """
def train_model():
    # Placeholder for model training logic
    print("Training model...")
""",
    f'src/{project_name}/components/model_evaluation.py': """
def evaluate_model():
    # Placeholder for model evaluation logic
    print("Evaluating model...")
""",
    f'src/{project_name}/pipelines/__init__.py': "",
    f'src/{project_name}/pipelines/train_pipeline.py': f"""
from {project_name}.components.data_ingestion import ingest_data
from {project_name}.components.data_transformation import transform_data
from {project_name}.components.model_trainer import train_model
from {project_name}.components.model_evaluation import evaluate_model

def run_training_pipeline():
    ingest_data()
    transform_data()
    train_model()
    evaluate_model()
""",
    f'src/{project_name}/pipelines/predict_pipeline.py': """
def run_prediction_pipeline():
    # Placeholder for prediction pipeline logic
    print("Running prediction pipeline...")
""",
    f'src/{project_name}/utils/__init__.py': "",
    f'src/{project_name}/utils/logging.py': """
import logging
import logging.config
import yaml
import os

def setup_logging(
    default_path='config/logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    Sets up logging configuration
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
""",
    f'src/{project_name}/utils/config.py': """
import yaml

def load_config(config_path='config/config.yaml'):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config
""",
    f'src/{project_name}/utils/common.py': """
def save_model(model, model_path):
    # Placeholder for saving model logic
    print(f"Saving model to {model_path}")
""",
    f'src/{project_name}/constants/__init__.py': """
# Define constants here
SEED = 42
""",
    f'src/{project_name}/entities/__init__.py': """
# Define data classes or entities here
""",
    'tests/__init__.py': "",
    'tests/test_components.py': f"""
import pytest
from {project_name}.components.data_ingestion import ingest_data

def test_ingest_data():
    # Placeholder test
    assert ingest_data() is None
""",
    'scripts/run_tests.sh': """
#!/bin/bash
pytest tests/
""",
    'scripts/build_docker.sh': f"""
#!/bin/bash
docker build -t {project_name}:latest .
""",
    'scripts/deploy.sh': """
#!/bin/bash
# Deployment script goes here
""",
    'templates/index.html': """
<!DOCTYPE html>
<html>
<head>
    <title>Welcome to Your Project</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
""",
    '.env.example': """
# Example environment variables
API_KEY=your_api_key_here
DB_HOST=db
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
""",
}

# Create directories
for dir in directories:
    Path(dir).mkdir(parents=True, exist_ok=True)

# Create files with sample content
for file_path, content in files.items():
    with open(file_path, 'w') as file:
        file.write(content.strip() + '\n')

# Make shell scripts executable
os.chmod('scripts/run_tests.sh', 0o755)
os.chmod('scripts/build_docker.sh', 0o755)
os.chmod('scripts/deploy.sh', 0o755)

print("Project structure with sample files and docker-compose.yml created successfully.")
