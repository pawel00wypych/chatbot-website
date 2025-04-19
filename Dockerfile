# Step 1: Build React frontend
FROM node:18 AS frontend

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Step 2: Build Python backend
FROM python:3.11-slim AS backend

# System deps
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev curl netcat-openbsd gcc \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Copy backend code
COPY backend/ backend/
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy built frontend into Django static root
COPY --from=frontend /app/frontend/build /app/backend/frontend_build

# Collect static
ENV DJANGO_SETTINGS_MODULE=backend.settings
WORKDIR /app/backend
RUN python manage.py collectstatic --noinput

# Step 3: Final Image with Nginx
FROM nginx:1.25-alpine

# Copy nginx config
COPY nginx/nginx-setup.conf /etc/nginx/conf.d/default.conf

# Copy Django static and media
COPY --from=backend /app/backend/staticfiles /static
COPY --from=backend /app/backend/media /media

# Copy backend app
COPY --from=backend /app/backend /app/backend

# Daphne + Entrypoint
RUN apk add --no-cache python3 py3-pip && \
    pip install "daphne" "channels" -r /app/backend/../requirements.txt

EXPOSE 80

CMD daphne -b 0.0.0.0 -p 8000 backend.asgi:application & nginx -g "daemon off;"
