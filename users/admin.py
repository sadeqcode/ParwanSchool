from django.contrib import admin
from .models import profile
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = profile
    search_fields = ('email', 'user_name', 'first_name',)
    list_filter = ('email', 'user_name', 'first_name', 'is_teacher', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name', 'birth_date', 'phone_number')}),
        ('Permissions', {'fields': ('is_teacher', 'is_staff', 'is_active')}),
        ('Personal', {'fields': ('profile_pic', 'about',)}),
    )
    formfield_overrides = {
        profile.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name', "birth_date",
                       'phone_number', 'profile_pic', 'password1', 'password2',
                       'is_teacher', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(profile, UserAdminConfig)
