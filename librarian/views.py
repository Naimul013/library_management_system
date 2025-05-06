from django.shortcuts import render
from library_management.models import *
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
    profile = Profile.objects.filter(role= 'member')
    
    context = {'profile':profile}
    return render(request,'librarian/member_profile.html',context)

def member_details(request,user_id):
    user = get_object_or_404(User,id = user_id)
    current_borrow_details = BorrowBook.objects.filter(member = user,returned = False)
    previous_borrow_details = BorrowBook.objects.filter(member = user, returned = True)
    context = {'borrow':current_borrow_details,'user':user,"borrowed":previous_borrow_details}
    return render(request,'librarian/member_details.html',context)

