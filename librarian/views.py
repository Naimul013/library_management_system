from django.shortcuts import render,redirect
from library_management.models import *
from library_management.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
# Create your views here.
def is_librarian(user):
    
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'librarian' or user.profile.role == 'admin'

@login_required
@user_passes_test(is_librarian)
def dashboard(request):
    librarian = request.user
    profile = Profile.objects.get(user= librarian)
    context = {'profile':profile}
    return render(request,'librarian/dashboard.html',context)
@login_required
@user_passes_test(is_librarian)
def member_profile(request):
    user = request.user
    role = user.profile.role
    print(role)
    print(request.path)
    member_profile = Profile.objects.filter(role= 'member')
    librarian_profile = Profile.objects.filter(role = 'librarian')
    if request.path == '/librarian/memberprofile/':
        if role == 'librarian' or role == 'admin':
            template = 'librarian/member_profile.html'
    elif request.path == '/librarian/librarianprofile/':
        if role == 'admin':
            template = 'librarian/librarian_profile.html'
    
    context = {'profile':member_profile,'librarian_profile':librarian_profile}
    return render(request,template,context)

def member_details(request,user_id):
    user = get_object_or_404(User,id = user_id)
    current_borrow_details = BorrowBook.objects.filter(member = user,returned = False)
    previous_borrow_details = BorrowBook.objects.filter(member = user, returned = True)
    context = {'borrow':current_borrow_details,'user':user,"borrowed":previous_borrow_details}
    return render(request,'librarian/member_details.html',context)

def adding_book(request):
    if request.method == 'POST':
        form = AddingBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book')
    else:
        form = AddingBookForm()
    context = {'form':form}
    return render(request,'librarian/add_book.html',context)