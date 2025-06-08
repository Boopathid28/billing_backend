from django.contrib import admin

from .models import *

@admin.register(StoneWeightType)
class StoneWeightTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'weight_name',
        'is_active',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
    )
    list_filter = ('is_active', 'created_at', 'created_by', 'modified_at')


@admin.register(EntryType)
class EntryTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'entry_name',
        'is_active',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
    )
    list_filter = ('is_active', 'created_at', 'created_by', 'modified_at')


@admin.register(RateType)
class RateTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type_name',
        'is_active',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
    )
    list_filter = ('is_active', 'created_at', 'created_by', 'modified_at')


@admin.register(LotID)
class LotIDAdmin(admin.ModelAdmin):
    list_display = ('id', 'lot_number')



@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'branch',
        'lot_number',
        'entry_date',
        'entry_type',
        'designer_name',
        'invoice_number',
        'total_pieces',
        'total_netweight',
        'hallmark_number',
        'hallmark_center',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
    )
    list_filter = (
        'entry_date',
        'branch',
        'entry_type',
        'designer_name',
        'created_at',
        'created_by',
        'modified_at',
    )


@admin.register(LotItem)
class LotItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'lot_details',
        'item_details',
        'bulk_tag',
        'tag_type',
        'pieces',
        'tag_count',
        'gross_weight',
        'net_weight',
        'tag_weight',
        'cover_weight',
        'loop_weight',
        'other_weight',
        'remark',
    )
    list_filter = (
        'lot_details',
        'item_details',
        'bulk_tag',
        'tag_type',
    )


@admin.register(LotItemStone)
class LotItemStoneAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'lot_details',
        'lot_item',
        'stone_name',
        'stone_pieces',
        'stone_weight',
        'stone_rate',
        'stone_rate_type',
    )
    list_filter = (
        'lot_details',
        'lot_item',
        'stone_name',
        'stone_rate_type',
    )


@admin.register(LotItemDiamond)
class LotItemDiamondAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'lot_details',
        'lot_item',
        'diamond_name',
        'diamond_pieces',
        'diamond_weight',
        'diamond_rate',
        'diamond_rate_type',
    )
    list_filter = (
        'lot_details',
        'lot_item',
        'diamond_name',
        'diamond_rate_type',
    )