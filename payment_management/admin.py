from django.contrib import admin
from .models import *

class PaymentMethodAdmin(admin.ModelAdmin):

    list_display = ['payment_method_name', 'color', 'bg_color']

    list_editable = ['color', 'bg_color']

admin.site.register(PaymentMenthod, PaymentMethodAdmin)

class PaymentProviderAdmin(admin.ModelAdmin):

    list_display = ['payment_provider_name', 'payment_method']

admin.site.register(PaymentProviders, PaymentProviderAdmin)

class PaymentModuleAdmin(admin.ModelAdmin):

    list_display = ['module_name']

admin.site.register(PaymentModule, PaymentModuleAdmin)