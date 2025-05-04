
from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.home, name='home'),
    path('author/', views.author, name='author'),
    path('publisher/', views.publisher, name='publisher'),
    path('books/', views.books, name='books'),

]
