from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'authentication'
urlpatterns = [
    
    path('signup/', views.handlesignup ,name='handlesignup'),
    path('login/', views.handlelogin ,name='handlelogin'),
    path('logout/', views.handlelogout,name='handlelogout'),

    
]