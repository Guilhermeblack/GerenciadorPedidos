from django.conf.urls import url
from gerenciador.consumers import StateConsumer
from django.urls import re_path


websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<loja>\w+)/$', StateConsumer.as_asgi()),
]