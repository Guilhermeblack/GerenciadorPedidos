from django.conf.urls import url
from gerenciador.consumers import StateConsumer
from django.urls import re_path


websocket_urlpatterns = [
    url(r'^ws/stt/(?P<loja>\w+)/$', StateConsumer.as_asgi()),
]