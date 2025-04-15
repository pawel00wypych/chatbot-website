# ==== frontend build ====
FROM node:18 AS frontend
WORKDIR /chatbot_frontend
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

# Install Nginx
RUN apt-get update && apt-get install -y nginx gettext

WORKDIR /chatbot-website

# Copy entire app and requirements
COPY --from=backend /chatbot-website /chatbot-website
COPY requirements.txt .

# Install Python dependencies (including Daphne)
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install twisted[http2,tls]

# Copy frontend build
COPY --from=frontend /chatbot_frontend/build /usr/share/nginx/html

# Copy Nginx config
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Expose ports
EXPOSE 80
EXPOSE 8000

# Start everything
CMD sh -c "envsubst '\$PORT' < /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/default.conf && \
           daphne --access-log -b 127.0.0.1 -p 8000 chatbot_backend.asgi:application & \
           cat /etc/nginx/conf.d/default.conf   nginx -g 'daemon off;'"
