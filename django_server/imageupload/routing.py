from . import consumers

from django.urls import path
websocket_urlpatterns = [
    path('ws/upload/', consumers.UploadConsumer.as_asgi()),
]

