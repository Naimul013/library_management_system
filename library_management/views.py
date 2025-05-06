from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.db.models import Q
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


def borrow_book(request,isbn_code):
    book = Book.objects.get(isbn_code= isbn_code)
    
    if request.method == "POST":
        form = BorrowBookForm(request.POST)
        form.instance.member = request.user
        form.instance.book = book
        if form.is_valid():
            try:
                borrow = form.save(commit = False)
                
                
                borrow.borrow_date = date.today()
                borrow.due_date = borrow.borrow_date + timedelta(days= borrow.allowed_date)
                try:
                    borrow.full_clean()

                    borrow.save()
                    messages.success(request,"You borrowed the book")
                    return redirect('books')
                except ValidationError as e:
                    messages.error(request,str(e))

            except ValidationError as e:
                messages.error(request,str(e))
                return redirect('books')   
    else:
        form = BorrowBookForm()

    context = {'books':book, 'forms':form}
    return render(request,'library_management/borrow.html',context)

def return_book(request, isbn_code):
    borrow = get_object_or_404(BorrowBook,member= request.user,book__isbn_code= isbn_code,returned = False)
    borrow.mark_as_returned()
    
    messages.success(request,"The book has been returned")
    return redirect('books')

 
def filtering(request):
    query = request.GET.get('q','')
    category = request.GET.get('category','')
    books = Book.objects.all()
    
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__first_name__icontains=query)| Q(author__last_name__icontains=query)| Q(isbn_code__icontains= query)
        )
    if category:
        books = books.filter(category__name__icontains= category)

    paginator = Paginator(books,10)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1  # Default to the first page if page is not provided
    
    try:
        page_obj = paginator.get_page(page_number)  # Get the current page object
    except Exception as e:
        # If there is any error, you can log it or handle it appropriately
        page_obj = Paginator.get_page(1)

    all_books_data = []
    for book in page_obj:
        data ={}
        for field in Book._meta.fields:
            if isinstance(field,models.ForeignKey):
                value = getattr(book,field.name)
                data[field.name] = value

        
    
        for field in Book._meta.many_to_many:
            if isinstance(field,models.ManyToManyField):
                value = getattr(book,field.name).all()
                data[field.name] = value
        all_books_data.append(data)
    
    context = {'page_obj':page_obj,"books_data":all_books_data}
    return render(request,'library_management/book_list.html',context)
            
