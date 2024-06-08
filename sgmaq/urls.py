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
    path('register_wash/', views.register_wash, name='register_wash'),
    path('create_task/', views.create_task, name='create_task'),
    path('task_overview/', views.task_overview, name="task_overview"),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)