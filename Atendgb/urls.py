from django.urls import path
from django.contrib import admin
from gerenciador import views

app_name = 'gerenciador'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('loguin', views.loguin, name='loguin'),
    path('logout', views.logoutuser, name='logout'),
    path('feed', views.feed, name='feed'),
    path('ped', views.ped, name='pedidos'),
    path('adm', views.adm, name='administrador'),
    path('profile', views.profile, name='profile'),
    path('pedidos', views.ped, name='pedidos'),
    # path('loguin/', include('urls', namespace='log')),

    ]
