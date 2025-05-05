from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'member_dashboard'
urlpatterns = [
    
    path('', views.member_dashboard ,name='member_dashboard'),
    

    
]