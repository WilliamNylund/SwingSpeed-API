from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'is_staff', 'is_active')
    list_filter = ('username', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'age', 'gender', 'height', 'handicap', 'lefty', 'date_created', 'profile_picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    readonly_fields = ('date_created',)
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(User, UserAdmin)