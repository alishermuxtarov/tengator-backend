from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _

from aggregator import models
from aggregator.models import User


class LotFileInline(admin.TabularInline):
    model = models.LotFile
    extra = 0


@admin.register(models.Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ['bid_id', 'bid_date', 'region', 'area', 'title', 'start_price']
    search_fields = ['conditions', 'customer_info', 'title', 'bid_id']
    list_filter = ['bid_date']
    inlines = [LotFileInline]


@admin.register(models.SearchWord)
class SearchWordAdmin(admin.ModelAdmin):
    list_display = ['word', 'user']
    search_fields = ['word']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']
    search_fields = ['title']


@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'id']
    search_fields = ['title']
    list_filter = ['category']


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']
    search_fields = ['title']


@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['title', 'region', 'id']
    search_fields = ['title']
    list_filter = ['region']


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


