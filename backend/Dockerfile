FROM python:3.12-slim

WORKDIR /code

# Install dependencies
COPY pyproject.toml .
RUN pip install .

# Copy application code
COPY ./backend/app /code/app
COPY ./modules /code/modules

# Command to run the API server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]