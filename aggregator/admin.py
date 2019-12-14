from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _

from aggregator import models
from aggregator.models import User


@admin.register(models.Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ['bid_id', 'bid_date', 'region', 'area', 'title', 'start_price']
    search_fields = ['conditions', 'customer_info', 'title', 'bid_id']
    list_filter = ['bid_date']


@admin.register(models.SearchWord)
class LotAdmin(admin.ModelAdmin):
    list_display = ['word', 'user']
    search_fields = ['word']


@admin.register(User)
class SimpleUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'uid'),
        }),
    )

    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)


