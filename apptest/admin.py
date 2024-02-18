from django.contrib import admin
from .models import *

# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    fields = ['username', 'email', 'password']
