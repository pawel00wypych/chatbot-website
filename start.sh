#!/bin/sh

daphne -b 0.0.0.0 -p 8000 chatbot_backend.asgi:application &

nginx -g "daemon off;"
