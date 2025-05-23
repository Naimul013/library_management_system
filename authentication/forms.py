from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

class ProfileForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    profile_picture = forms.ImageField(required=True)
    phone_number = PhoneNumberField(region='BD')
    address = forms.CharField(max_length=100,required=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','email','password1','password2','phone_number','address','profile_picture']

    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('Email already exists')
        return email
    
    def save(self,commit = True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField( max_length=50, required=False)
    password = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['username','password']
