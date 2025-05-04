from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(BookCategory)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(Book)
