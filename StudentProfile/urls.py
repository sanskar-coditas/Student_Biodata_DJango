from django.contrib import admin
from django.urls import include, path
from . import views 
from .views import get


urlpatterns = [
    path('submit', views.submit),
    path('get', get, name='get_data'),
    path('delete', views.delete, name='delete_data'),
    path('update', views.update, name='update_data'),



]
