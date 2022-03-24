from django.conf import urls
from Atendgb.consumers import StateConsumer

websocket_urlpatterns = [
    urls.url(r'^ws/state/(?P<room_code>\w+)/$', StateConsumer.as_asgi()),
]