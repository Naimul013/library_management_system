from django import forms
from .models import *
class BorrowBookForm(forms.ModelForm):
    
    class Meta:
        model = BorrowBook
        fields = ('allowed_date',)

class AddingBookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = '__all__'

    
