from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [    
    path('', views.index, name="index"),
    path('', views.index, name="about"),
    path('', views.index, name="signin"),
    path('', views.index, name="signup"),

] 