"""
ASGI config for chatbot_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import re_path

from chatbot_backend.chat import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
            ]
        )
    ),
})
