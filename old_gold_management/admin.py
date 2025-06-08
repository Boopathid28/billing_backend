from django.contrib import admin

from .models import OldGoldBillDetails, OldGoldItemDetails


@admin.register(OldGoldBillDetails)
class OldGoldBillDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'old_gold_bill_number',
        'customer_details',
        'old_gold_weight',
        'old_gold_pieces',
        'old_gold_amount',
        'is_billed',
        'refference_number',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
        'branch',
       
    )
    list_filter = (
        'customer_details',
        'is_billed',
        'created_at',
        'modified_at',
        'branch',
    )


@admin.register(OldGoldItemDetails)
class OldGoldItemDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'old_bill_details',
        'old_metal',
        'old_gross_weight',
        'old_reduce_weight',
        'old_touch',
        'old_rate',
        'old_dust_weight',
        'old_net_weight',
        'old_amount',
        'total_amount',
    )
    list_filter = ('old_bill_details', 'old_metal')