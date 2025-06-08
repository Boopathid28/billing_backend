from django.contrib import admin

from .models import OldGoldLedger


@admin.register(OldGoldLedger)
class OldGoldLedgerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'vendor_details',
        'entry_date',
        'old_ledger_entry_type',
        'touch',
        'weight',
        'refference_number',
        'created_by',
    )
    list_filter = ('vendor_details', 'entry_date')
