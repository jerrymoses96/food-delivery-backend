from django.contrib import admin
from .models import Location, Restaurant, MenuItem

# Register your models here


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city',)  # Customize the displayed columns if needed


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'opening_time',
                    'closing_time')  # Customize as needed
    search_fields = ('name', 'owner__username')  # Add search fields if desired


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price')  # Customize as needed
    # Add search fields if desired
    search_fields = ('name', 'restaurant__name')
