from django.contrib import admin

from .models import TransferStatus, TransferType, TransferItem, TransferItemDetails, ReceivedItem, ReceivedItemDetails, ReturnItem, ReturnItemDetails

@admin.register(TransferStatus)
class TransferStatusAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status_name',
        'status_comments',
        'status_bgcolor',
        'status_color',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
    )
    list_filter = ('created_at', 'created_by', 'modified_at')
    date_hierarchy = 'created_at'


@admin.register(TransferType)
class TransferTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status_name',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
    )
    list_filter = ('created_at', 'created_by', 'modified_at')
    date_hierarchy = 'created_at'


@admin.register(TransferItem)
class TransferItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'transfer_date',
        'required_date',
        'transfer_from',
        'transfer_to',
        'stock_authority',
        'transfer_status',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
    )
    list_filter = (
        'transfer_date',
        'required_date',
        'transfer_from',
        'transfer_to',
        'stock_authority',
        'transfer_status',
        'created_at',
        'created_by',
        'modified_at',
    )
    date_hierarchy = 'created_at'


@admin.register(TransferItemDetails)
class TransferItemDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'transfer_itemid',
        'tagitems_id',
        'tag_number',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
    )
    list_filter = (
        'transfer_itemid',
        'tagitems_id',
        'created_at',
        'created_by',
        'modified_at',
    )
    date_hierarchy = 'created_at'


@admin.register(ReceivedItem)
class ReceivedItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'transfer_itemid',
        'received_date',
        'transfer_status',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
    )
    list_filter = (
        'transfer_itemid',
        'received_date',
        'transfer_status',
        'created_at',
        'created_by',
        'modified_at',
    )
    date_hierarchy = 'created_at'


@admin.register(ReceivedItemDetails)
class ReceivedItemDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'received_itemid',
        'transfer_itemid',
        'tagitems_id',
        'tag_number',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
    )
    list_filter = (
        'received_itemid',
        'transfer_itemid',
        'tagitems_id',
        'created_at',
        'created_by',
        'modified_at',
    )
    date_hierarchy = 'created_at'


@admin.register(ReturnItem)
class ReturnItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'transfer_itemid',
        'return_date',
        'reason',
        'transfer_status',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
    )
    list_filter = (
        'transfer_itemid',
        'return_date',
        'transfer_status',
        'created_at',
        'created_by',
        'modified_at',
    )
    date_hierarchy = 'created_at'


@admin.register(ReturnItemDetails)
class ReturnItemDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'return_itemid',
        'transfer_itemid',
        'tagitems_id',
        'tag_number',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
    )
    list_filter = (
        'return_itemid',
        'transfer_itemid',
        'tagitems_id',
        'created_at',
        'created_by',
        'modified_at',
    )
    date_hierarchy = 'created_at'

