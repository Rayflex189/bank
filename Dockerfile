# Use official slim Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV DJANGO_SUPPRESS_PROMPTS=true
ENV CLOUDINARY_URL=${CLOUDINARY_URL}

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY wealthbridge/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install additional packages
RUN pip install pillow django-cloudinary-storage

# Copy the full Django project
COPY wealthbridge/ /app/

# Run icon creation script
RUN if [ -f scripts/create_icons.py ]; then \
        echo "📱 Creating app icons..."; \
        python scripts/create_icons.py; \
        echo "✅ Icons created successfully!"; \
    else \
        echo "⚠️  No icon creation script found, skipping..."; \
    fi

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose port
EXPOSE 8088

# Start server with Gunicorn
CMD ["gunicorn", "wealthbridge.wsgi:application", "--bind", "0.0.0.0:8088"]
