from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Transaction, UserLink, UserProfile, TransactionAdmin

# Register your models here.

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(UserLink)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
