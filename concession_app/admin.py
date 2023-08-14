from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from concession_app.models import *
# Register your models here.


class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone')
    list_filter = ('email', 'username', 'first_name', 'middle_name', 'last_name', 'phone')
    ordering = ('-id',)
    list_display = ('username',)
    fieldsets = (
        ("Details", {'fields': ('email', 'username', 'password','first_name','last_name', 'middle_name', 'email_verified_at', 
                                'status','is_verified', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'middle_name', 'last_name', 'password1', 'password2', 'is_staff')}
         ),
    )


admin.site.register(CustomUser, UserAdminConfig)



