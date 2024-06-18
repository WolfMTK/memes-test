# API service to S3

# Description

### A small API for interacting with S3

# Local startup

1. Install the virtual environment: `python -m venv venv` (linux)

2. Export the required variables (see .env.example)

3. Start the application: `uvicorn --factory minio_app.main:create_app`
