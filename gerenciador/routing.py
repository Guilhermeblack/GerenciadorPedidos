from django.conf import urls
from gerenciador.consumers import StateConsumer

websocket_urlpatterns = [
    urls.url(r'^ws/stt/(?P<pedido>\w+)/$', StateConsumer.as_asgi()),
]