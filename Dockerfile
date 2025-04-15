# ==== frontend build ====
FROM node:18 AS frontend
WORKDIR /app
COPY chatbot_frontend/ .
RUN npm install
RUN npm run build

# ==== backend build ====
FROM python:3.11 AS backend
WORKDIR /chatbot-website
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput

# ==== production image ====
FROM python:3.11 AS prod

# Install Daphne + Nginx
RUN apt-get update && apt-get install -y nginx

WORKDIR /app
COPY --from=backend /chatbot-website /app
COPY --from=frontend /app/build /usr/share/nginx/html

# Copy Nginx config
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Expose both ports (80 for Nginx, 8000 for Daphne)
EXPOSE 80
EXPOSE 8000

# Start both Nginx and Daphne
CMD sh -c "nginx && daphne -b 0.0.0.0 -p 8000 chatbot_backend.asgi:application"
