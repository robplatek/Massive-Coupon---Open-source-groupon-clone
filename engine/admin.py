# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *

class AdvertiserAdmin(admin.ModelAdmin):
    """admin class"""

class ProductCategoryAdmin(admin.ModelAdmin):
    """admin class"""

class DealAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ( 'title', )
    }


class ProfileAdmin(admin.ModelAdmin):
    """admin class"""

class EmailSubAdmin(admin.ModelAdmin):
   """admin class"""

class CouponAdmin(admin.ModelAdmin):
    """admin class"""
    list_display = ['user', 'deal', 'status']
    list_filter = ('user', 'deal')
    list_per_page = 100
    search_fields = ['user', 'deal']


class CityAdmin(admin.ModelAdmin):
    """admin class"""
    list_display = ['name', 'province', 'is_active']
    list_per_page = 100
    search_fields = ['name']
    prepopulated_fields = {
        'slug': ( 'name', )
    }


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Deal, DealAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(EmailSubscribe, EmailSubAdmin)
