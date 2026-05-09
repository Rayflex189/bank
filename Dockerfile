# Use official slim Python image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV DJANGO_SUPPRESS_PROMPTS=true

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY wealthbridge/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the full Django project
COPY wealthbridge/ /app/

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose port
EXPOSE 8088

# Default command (will be overridden by Fly.io's release_command)
CMD ["gunicorn", "wealthbridge.wsgi:application", "--bind", "0.0.0.0:8088"]
