FROM python:3.13.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

# Copy dependency specifications
COPY pyproject.toml .python-version uv.lock ./

# Install dependencies without building local package root
RUN uv sync --locked --no-install-project

# Copy your application code
COPY pipeline.py .

# Run script using the uv virtual environment's python
ENTRYPOINT ["uv", "run", "--no-sync", "python", "pipeline.py"]