from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.


def handlesignup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            if 'profile_picture' in request.FILES:
                user.profile.profile_picture = request.FILES['profile_picture']

            user.profile.role = 'member'
            user.profile.address = request.POST['address']
            user.profile.phone_number = request.POST['phone_number']
            user.profile.save()
            messages.success(request,'Registration success')
            return redirect('home')
        
    else:
        form = ProfileForm()
    
    context = {'form':form}


    return render(request,'authentication/signup.html',context)

def handlelogin(request):
    if request.method == 'POST':
        form = LoginForm(request, data= request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
  
        
       
            user = authenticate(request,username=username,password= password)
            if user is not None:
                login(request,user)
                messages.success(request,'Login Successfully')
                return redirect('home')
           

        else:
            
            messages.error(request,'user invalid')

    else:
        form = LoginForm()
    
    context = {'form':form}
    return render(request, 'authentication/handlelogin.html',context )


def handlelogout(request):
    logout(request)
    messages.success(request,'Logout successfull')
    return redirect('/auth/login')