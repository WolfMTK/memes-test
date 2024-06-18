# A service with memes

# Description

### API with simple CRUD implementation for working with memes

# Local startup

1. Install the virtual environment: `python -m venv venv` (linux)

2. Activate the virtual environment: `. venv/bin/acivate`

3. Export the required variables (see .env.example)

4. Install dependencies: 'pip install -e .[dev]'

5. Start the application: `uvicorn --factory app.main:create_app`

# Tests startup

1. Install the virtual environment: `python -m venv venv` (linux)

2. Activate the virtual environment: `. venv/bin/acivate`

3. Run tests: `pytest`
