
from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.home, name='home'),
    path('author/', views.author, name='author'),
    path('publisher/', views.publisher, name='publisher'),
    path('books/', views.books, name='books'),
    path('books/<str:isbn_code>/', views.borrow_book, name='borrow_book'),
    path('return/<str:isbn_code>/', views.return_book, name='return_book'),
    path('book_list/',views.filtering,name='book_list'),

]
