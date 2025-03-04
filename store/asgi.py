"""
ASGI config for store project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Adding channel Protocol
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import product.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'https': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            product.routing.websocket_urlpatterns
        )
    )
})
