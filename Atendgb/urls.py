from django.urls import path, include
from django.contrib import admin
from gerenciador import views
from django.conf import urls, settings
from django.conf.urls.static import static

app_name = 'gerenciador'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('', include('pwa.urls')),
    path('loguin', views.loguin, name='loguin'),
    path('logout', views.logoutuser, name='logout'),
    path('feed', views.feed, name='feed'),
    path('ped', views.ped, name='pedidos'),
    path('adm', views.adm, name='administrador'),
    path('profile', views.profile, name='profile'),
    path('pedidos', views.ped, name='pedidos'),
    path('sobre', views.sobre, name='sobre'),
    # path('loguin/', include('urls', namespace='log')),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
