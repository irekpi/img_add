from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from img_upload.models import Image, Plan

admin.site.register(Image)
admin.site.register(Plan)




# TODO
# noqa This part of code should be in separate User App (because in normal situation we would like to have ability to make changes in USER model)
admin.site.unregister(User)


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'date_joined']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Permissions'), {
            'fields': ('is_active', 'groups'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, CustomUserAdmin)
