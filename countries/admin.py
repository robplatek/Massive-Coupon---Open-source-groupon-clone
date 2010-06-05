from django.contrib import admin
from models import *

class CountryAdmin(admin.ModelAdmin):
    """admin class"""
admin.site.register(Country, CountryAdmin)

