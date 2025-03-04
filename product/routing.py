from django.urls import re_path
from services.websocket import StoreConsumer

websocket_urlpatterns = [
    re_path(r'ws/socket-server/',StoreConsumer.as_asgi() )
]