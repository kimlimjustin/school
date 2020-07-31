from django.contrib import admin

# Register your models here.
from .models import User, UserType

admin.site.register(User)
admin.site.register(UserType)