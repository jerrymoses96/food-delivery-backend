from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email',
                    'is_normal_user', 'is_restaurant_owner']
    search_fields = ['username', 'email']


admin.site.register(User, UserAdmin)
