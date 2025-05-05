from django.shortcuts import render
from library_management.models import *
# Create your views here.
def member_dashboard(request):
    member = request.user
    profile = Profile.objects.get(user= member)
    current_borrow = BorrowBook.objects.filter(member = member,returned = False)
    borrowing_history = BorrowBook.objects.filter(member= member, returned = True)

    context = {'profile':profile,'current_borrow':current_borrow,'borrowing_history':borrowing_history}
    return render(request,"member_dashboard/dashboard.html",context)