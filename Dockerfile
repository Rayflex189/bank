# Use official slim Python image
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore
ENV DJANGO_SUPPRESS_PROMPTS=true

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY wealthbridge/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY wealthbridge/ /app/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8088

ENTRYPOINT ["/entrypoint.sh"]