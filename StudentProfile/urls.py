from django.contrib import admin
from django.urls import include, path
from . import views 
from .views import get
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('submit', views.submit),
    path('get', get, name='get_data'),
    path('delete', views.delete, name='delete_data'),
    path('update', views.update, name='update_data'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)