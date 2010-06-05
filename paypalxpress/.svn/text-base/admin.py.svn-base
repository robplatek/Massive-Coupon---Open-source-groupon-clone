# -*- coding: utf-8 -*-

from django.contrib import admin
from paypal.models import PayPalResponse, PayPalResponseStatus

class PayPalResponseAdmin(admin.ModelAdmin):
    list_display = ('token',
                    'trans_id',
                    'currencycode',
                    'error_msg',
                    'charged',
                    'payment_received',
                    'status')
    list_filter = ("payment_received", "status")

admin.site.register(PayPalResponse, PayPalResponseAdmin)
admin.site.register(PayPalResponseStatus)
