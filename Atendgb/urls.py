from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from GerenciadorPedidos.gerenciador import views

app_name = 'gerenciador'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path('vend/', include('gerenciador.urls', namespace='vend')),
    path('loguin', views.loguin, name='loguin'),
    path('logout', views.logoutuser, name='logout'),
    path('feed', views.feed, name='feed'),
    path('ped', views.ped, name='pedidos'),
    # path('adm', views.adm, name='adm'),
    path('cardapio', views.cardapio, name='cardapio')
]
