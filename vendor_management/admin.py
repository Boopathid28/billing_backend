from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(VendorLedgerType)
class VendorLedgerTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'vendor_ledger_type',
        'created_at',
        'created_by',
    )
    list_filter = ('vendor_ledger_type', 'created_at', 'created_by', )