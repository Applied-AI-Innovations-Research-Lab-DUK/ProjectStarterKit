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
CMD ["poetry", "run", "python", "src/sample_project/main.py"]
