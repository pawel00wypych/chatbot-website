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
COPY chatbot_website_backend/ .

# Run Django dev server (for production, use gunicorn)
CMD ["python", "chatbot_website_backend/manage.py", "runserver", "0.0.0.0:8000"]
