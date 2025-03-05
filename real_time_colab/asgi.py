# real_time_colab/asgi.py
import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Ensure Django setup is complete
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_time_colab.settings')  # Fixed typo
django.setup()

# Import WebSocket URL patterns after Django setup
from real_real_time_app.routing import websocket_urlpatterns  # Correct import statement

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})