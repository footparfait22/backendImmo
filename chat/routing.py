from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # On capture l'ID de la conversation dans l'URL
    re_path(r'ws/chat/(?P<conversation_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]