from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta, date
# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin','Admin'),
        ('librarian','Librarian'),
        ('member','Membrer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone_number = PhoneNumberField(region = 'BD',default='', blank=True)
    address = models.CharField( max_length=100,default='')
    profile_picture = models.ImageField( upload_to='profile_pics/', height_field=None, width_field=None, max_length=None,blank=True,default='')
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.user.first_name} - {self.role}" 
    


class BookCategory(models.Model):
   
    name = models.CharField( max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Publisher(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.EmailField( max_length=254)
    website = models.URLField(default='', max_length=200)

    def __str__(self):
        return self.name

class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    rating = models.DecimalField( max_digits=2, decimal_places=1)
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Reviewed by {self.user.username} for {self.book.title}"
    




class Book(models.Model):
    title = models.CharField(max_length=50)
    isbn_code = models.CharField( max_length=13, unique=True)
    category = models.ForeignKey(BookCategory,  on_delete=models.SET_NULL, blank=True, null=True)
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher,  on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField( upload_to='book_cover/', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    total_copies = models.IntegerField(default=0)
    available_copies = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    rating = models.DecimalField( max_digits=3, decimal_places=2,default=0.0)
    rating_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def update_rating(self):
        total_rating = sum([review.rating for review in self.reviews.all()])
        count = self.reviews.count()
        if count > 0:
            self.rating = total_rating/count
            self.rating_count = count
        else:
            self.rating = 0
            self.rating_count= 0

        self.save()

    def update_total_copies(self,num):
        if 0<= num <= self.total_copies:
            self.available_copies = num
            self.save()


class BorrowBook(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    allowed_date = models.IntegerField(default=14)
    due_date = models.DateField(blank=True,null=True)
    return_date = models.DateField(blank=True, null=True)
    returned = models.BooleanField(default=False)

    def is_overdue(self):
        return not self.returned and self.due_date < date.today()
    
    def mark_as_returned(self):

        
        if not self.returned:
            
            self.returned = True
            self.return_date = date.today()
            self.book.available_copies += 1
            self.book.save()
            self.save()
        
    
    def save(self,*args, **kwargs):
        if not self.pk:  #on creation only
            if self.book.available_copies < 1:
                raise ValidationError('No available copies to borrow')
            if self.allowed_date > 30:
                raise ValidationError('You are not allowed to borrow this book for more than 30 days.')
            self.borrow_date = date.today()
            self.due_date = self.borrow_date + timedelta(days=self.allowed_date)
            self.book.available_copies -= 1
            self.book.save()
        
        if self.returned and not self.return_date:
            # If the book is returned, set the return date to today's date
            self.return_date = date.today()

            # Increment available copies of the book
            self.book.available_copies += 1
            self.book.save()  # Save the book with updated available copies


        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Before deleting the Borrow record, increment the available copies of the book
        if self.book:
            if not self.returned:
                self.book.available_copies += 1
                self.book.save()  # Save the book with updated available copies
        
        # Call the parent delete method to delete the Borrow record
        super().delete(*args, **kwargs)
    

    def __str__(self):
        return f"{self.member.username} borrowed {self.book.title}"
    


        

    

    
    

    



