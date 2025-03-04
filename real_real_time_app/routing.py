# real_real_time_app/routing.py

from django.urls import re_path
from .consumers import CodeCollabConsumer

websocket_urlpatterns = [
    re_path(r'ws/code/$', CodeCollabConsumer.as_asgi()),
]
