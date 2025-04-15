# ==== frontend build ====
FROM node:18 AS frontend
WORKDIR /app
COPY chatbot_frontend/ .
RUN npm install
RUN npm run build

# ==== backend build ====
FROM python:3.11 AS backend
WORKDIR /chatbot-website
COPY chatbot_backend/ /chatbot-website/chatbot_backend
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput
COPY . .

# ==== production image ====
FROM nginx:alpine
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Kopiuj build frontendu
COPY --from=frontend /app/build /usr/share/nginx/html

# Kopiuj statyczne pliki Django (jeśli używasz collectstatic)
COPY --from=backend /chatbot-website/static /static/

# Port domyślny Nginx
EXPOSE 80
