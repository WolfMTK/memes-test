# API service to S3

# Description

### A small API for interacting with S3

# Local startup

1. Install the virtual environment: `python -m venv venv` (linux)

2. Activate the virtual environment: `. venv/bin/acivate`

3. Export the required variables (see .env.example)

4. Install dependencies: 'pip install -e .[dev]'

5. Start the application: `uvicorn --factory minio_app.main:create_app`

# Tests startup

1. Install the virtual environment: `python -m venv venv` (linux)

2. Activate the virtual environment: `. venv/bin/acivate`

3. Install dependencies: 'pip install -e .[dev]'

4. Run tests: `pytest`
