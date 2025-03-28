# chat/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import myapp.routing  # Import your app's routing configuration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        myapp.routing.websocket_urlpatterns
    ),
})
