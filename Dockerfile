# Use official slim Python image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV DJANGO_SUPPRESS_PROMPTS=true
ENV DJANGO_SUPERUSER_USERNAME=MrDarius
ENV DJANGO_SUPERUSER_PASSWORD=me12sleep
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com

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

# Create a startup script that runs migrations, creates superuser, then starts Gunicorn
RUN echo '#!/bin/bash\n\
echo "Running database migrations..."\n\
python manage.py migrate --no-input\n\
echo "Creating superuser if not exists..."\n\
python manage.py shell << EOF\n\
from django.contrib.auth import get_user_model\n\
User = get_user_model()\n\
if not User.objects.filter(username="MrDarius").exists():\n\
    User.objects.create_superuser("MrDarius", "admin@example.com", "me12sleep")\n\
    print("Superuser MrDarius created")\n\
else:\n\
    print("Superuser MrDarius already exists")\n\
EOF\n\
echo "Starting Gunicorn..."\n\
exec gunicorn wealthbridge.wsgi:application --bind 0.0.0.0:8088\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8088

# Default command (will be overridden by Fly.io's release_command)
CMD ["gunicorn", "wealthbridge.wsgi:application", "--bind", "0.0.0.0:8088"]
