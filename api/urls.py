from django.urls import path
from . import views
from .views import home, update_location

urlpatterns = [
    path('', views.home, name='home'),
    path('update_location/', update_location, name='home'),
]