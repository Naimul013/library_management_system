from django.shortcuts import render
from .models import *
# Create your views here.
def home(request):
    return render(request,'library_management/home.html')

def books(request):
    books = Book.objects.all()

    all_books_data = []
    for book in books:
        data ={}
        for field in Book._meta.fields:
            if isinstance(field,models.ForeignKey):
                value = getattr(book,field.name)
                data[field.name] = value

        all_books_data.append(data)
    
        for field in Book._meta.many_to_many:
            if isinstance(field,models.ManyToManyField):
                value = getattr(book,field.name).all()
                data[field.name] = value
        all_books_data.append(data)


    context = {'books':books,'books_data':all_books_data}
    return render(request,'library_management/books.html',context)

def author(request):
    author = Author.objects.all()
    context = {'authors':author}
    return render(request,'library_management/author.html',context)


def publisher(request):
    publisher = Publisher.objects.all()
    context = {'publishers':publisher}
    return render(request,'library_management/publisher.html',context)
