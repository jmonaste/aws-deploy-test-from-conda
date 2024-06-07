from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [    
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('signout/', views.signout, name="logout"),

    path('tasks/', views.tasks, name="tasks"),

] 