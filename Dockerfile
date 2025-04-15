# backend
FROM python:3.11-slim AS backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /chatbot-website

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN python manage.py collectstatic --noinput

# frontend React
FROM node:18 AS frontend

WORKDIR /chatbot_frontend
COPY chatbot_frontend/ .
RUN npm install && npm run build

# Finalny obraz – Nginx + Daphne + static files
FROM nginx:alpine

#  copy nginx
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# copy frontend
COPY --from=frontend /frontend/build /usr/share/nginx/html

COPY --from=backend /chatbot-website/static /static/

COPY --from=backend /chatbot-website /chatbot-website

# run Daphne + Nginx
COPY start.sh /start.sh
RUN chmod +x /start.sh

WORKDIR /chatbot-website

EXPOSE 80
CMD ["/start.sh"]
