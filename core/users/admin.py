from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'date_joined']
    fieldsets = (
        (None, {'fields': ('username', 'password', 'plans')}),

        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, CustomUserAdmin)
