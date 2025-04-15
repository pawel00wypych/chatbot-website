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

# Instalacja zależności Python
WORKDIR /chatbot-website

# Kopiowanie aplikacji backendowej
COPY --from=backend /chatbot-website /chatbot-website
COPY requirements.txt .

# Instalowanie zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie builda frontendowego do katalogu static
COPY --from=frontend /chatbot_frontend/build /chatbot_website/static

# Ekspozycja portów
EXPOSE 8000

# Uruchomienie aplikacji Django za pomocą Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "chatbot_backend.asgi:application"]
