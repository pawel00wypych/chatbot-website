# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /chatbot-website

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# No CMD here — docker-compose handles it
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "chatbot_website_backend.asgi:application"]
