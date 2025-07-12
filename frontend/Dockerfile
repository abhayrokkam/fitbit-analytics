FROM python:3.12-slim

# Working Directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install .

# Copy application code
COPY frontend/dashboard.py .

# Expose the Streamlit port
EXPOSE 8501

# Command to run the dashboard
CMD ["streamlit", "run", "dashboard.py"]