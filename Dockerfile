FROM node:18-alpine AS frontend

WORKDIR /frontend
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend ./
RUN npm run build

# backend + frontend + nginx
FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/env \
    PATH="/env/bin:$PATH"

RUN apk update && apk add --no-cache build-base python3-dev libffi-dev

RUN python3 -m venv $VIRTUAL_ENV
WORKDIR /backend
COPY ./backend/requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./backend .

RUN apk add --no-cache nginx
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
# rm -> we want to prevent application from .conf duplicates
RUN rm -rf /etc/nginx/conf.d

COPY --from=frontend /frontend/build /var/www/frontend

EXPOSE 80

CMD sh -c "daphne -b 0.0.0.0 -p 8000 core.asgi:application & nginx -g 'daemon off;'"
