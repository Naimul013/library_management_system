from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'librarian'
urlpatterns = [
    
    path('', views.dashboard ,name='dashboard'),
    path('memberprofile/', views.member_profile ,name='member_profile'),
    path('member_details/<str:user_id>/', views.member_details ,name='member_details'),

    

    
]