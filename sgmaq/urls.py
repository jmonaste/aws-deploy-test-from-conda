from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [    
    path('', views.index, name="index"),
    path('', views.about, name="about"),
    path('', views.signin, name="signin"),
    path('', views.signup, name="signup"),
    path('', views.signout, name="signout"),

] 