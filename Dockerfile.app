# Dockerfile.app
FROM python:3.11-slim

# Install pipenv
RUN pip install pipenv

# Set working directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /app/

# Install dependencies
RUN pipenv install --system --deploy

# Copy application code
COPY . /app/

# Expose port 8000 for the web service
EXPOSE 8000

# Start the application
CMD ["pipenv", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "src.app:app"]
