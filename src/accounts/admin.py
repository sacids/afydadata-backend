
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from accounts.models import Profile

admin.site.unregister(User)

class ProfileInline(admin.StackedInline):
    model = Profile

class UserProfileAdmin(UserAdmin):
    inlines = [ ProfileInline, ]

admin.site.register(User, UserProfileAdmin)