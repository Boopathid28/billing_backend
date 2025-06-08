from django.contrib import admin

from .models import EstimateDetails, EstimationTagItems, EstimationOldGold, EstimationStoneDetails, EstimationDiamondDetails, BillingDetails, EstimationSaleReturnItems, EstimationReturnStoneDetails, EstimationReturnDiamondDetails, EstimationApproval, BillingSaleReturnItems, BillingReturnStoneDetails, BillingReturnDiamondDetails, BillNumber, BillID,BillingType


@admin.register(EstimateDetails)
class EstimateDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'estimate_no',
        'estimation_date',
        'customer_details',
        'is_billed',
        'branch',
        'created_by',
        'created_at',
        'modified_by',
        'modified_at',
    )
    list_filter = (
        'estimation_date',
        'customer_details',
        'is_billed',
        'branch',
        'created_by',
        'created_at',
        'modified_by',
        'modified_at',
    )


@admin.register(EstimationTagItems)
class EstimationTagItemsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'estimation_details',
        'estimation_tag_item',
        'tag_number',
        'item_details',
        'sub_item_details',
        'metal',
        'net_weight',
        'gross_weight',
        'pieces',
        'total_pieces',
        'rate',
        'stone_rate',
        'huid_rate',
        'diamond_rate',
        'wastage_percentage',
        'flat_wastage',
        'making_charge',
        'flat_making_charge',
        'stock_type',
        'calculation_type',
        'making_charge_calculation_type',
        'gst_percent',
        'additional_charges',
        'per_gram_weight_type',
        'total_stone_weight',
        'wastage_calculation_type',
        'total_diamond_weight',
        'gst',
        'total_amount',
        'with_gst_total_rate',
    )
    list_filter = (
        'estimation_details',
        'estimation_tag_item',
        'item_details',
        'sub_item_details',
        'metal',
        'stock_type',
        'calculation_type',
        'making_charge_calculation_type',
        'per_gram_weight_type',
        'wastage_calculation_type',
    )


# @admin.register(EstimationOldGold)
# class EstimationOldGoldAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'estimation_details',
#         'old_metal',
#         'metal_rate',
#         'today_metal_rate',
#         'old_gross_weight',
#         'old_net_weight',
#         'dust_weight',
#         'old_metal_rate',
#         'total_old_gold_value',
#     )
#     list_filter = ('estimation_details', 'old_metal')


@admin.register(EstimationStoneDetails)
class EstimationStoneDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'estimation_details',
        'estimation_item_details',
        'stone_name',
        'stone_pieces',
        'stone_weight',
        'stone_weight_type',
        'stone_rate',
        'stone_rate_type',
        'include_stone_weight',
        'total_stone_value',
    )
    list_filter = (
        'estimation_details',
        'estimation_item_details',
        'stone_name',
        'stone_weight_type',
        'stone_rate_type',
        'include_stone_weight',
    )


@admin.register(EstimationDiamondDetails)
class EstimationDiamondDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'estimation_details',
        'estimation_item_details',
        'diamond_name',
        'diamond_pieces',
        'diamond_weight',
        'diamond_weight_type',
        'diamond_rate',
        'diamond_rate_type',
        'include_diamond_weight',
        'total_diamond_value',
    )
    list_filter = (
        'estimation_details',
        'estimation_item_details',
        'diamond_name',
        'diamond_weight_type',
        'diamond_rate_type',
        'include_diamond_weight',
    )


@admin.register(BillingDetails)
class BillingDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'bill_id',
        'bill_date',
        'customer_details',
        'total_amount',
        'branch',
        'created_by',
        'created_at',
    )
    list_filter = (
        'bill_date',
        'customer_details',
        'branch',
        'created_by',
        'created_at',
    )


# @admin.register(BillingParticularDetails)
# class BillingTagItemsAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'billing_details',
#         'billing_tag_item',
#         'tag_number',
#         'item_details',
#         'sub_item_details',
#         'metal',
#         'net_weight',
#         'gross_weight',
#         'tag_weight',
#         'cover_weight',
#         'loop_weight',
#         'other_weight',
#         'pieces',
#         'total_pieces',
#         'rate',
#         'stone_rate',
#         'huid_rate',
#         'diamond_rate',
#         'wastage_percentage',
#         'flat_wastage',
#         'making_charge',
#         'flat_making_charge',
#         'stock_type',
#         'calculation_type',
#         'making_charge_calculation_type',
#         'tax_percent',
#         'additional_charges',
#         'per_gram_weight_type',
#         'total_stone_weight',
#         'wastage_calculation_type',
#         'total_diamond_weight',
#         'gst',
#         'total_rate',
#         'without_gst_rate',
#         'is_returned',
#     )
#     list_filter = (
#         'billing_details',
#         'billing_tag_item',
#         'item_details',
#         'sub_item_details',
#         'metal',
#         'stock_type',
#         'calculation_type',
#         'making_charge_calculation_type',
#         'per_gram_weight_type',
#         'wastage_calculation_type',
#         'is_returned',
#     )


# @admin.register(BillingStoneDetails)
# class BillingStoneDetailsAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'billing_details',
#         'billing_item_details',
#         'stone_name',
#         'stone_pieces',
#         'stone_weight',
#         'stone_weight_type',
#         'stone_rate',
#         'stone_rate_type',
#         'include_stone_weight',
#         'total_stone_value',
#     )
#     list_filter = (
#         'billing_details',
#         'billing_item_details',
#         'stone_name',
#         'stone_weight_type',
#         'stone_rate_type',
#         'include_stone_weight',
#     )


# @admin.register(BillingDiamondDetails)
# class BillingDiamondDetailsAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'billing_details',
#         'billing_item_details',
#         'diamond_name',
#         'diamond_pieces',
#         'diamond_weight',
#         'diamond_weight_type',
#         'diamond_rate',
#         'diamond_rate_type',
#         'include_diamond_weight',
#         'total_diamond_value',
#     )
#     list_filter = (
#         'billing_details',
#         'billing_item_details',
#         'diamond_name',
#         'diamond_weight_type',
#         'diamond_rate_type',
#         'include_diamond_weight',
#     )


# @admin.register(BillingOldGold)
# class BillingOldGoldAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'billing_details',
#         'old_metal',
#         'metal_rate',
#         'today_metal_rate',
#         'old_gross_weight',
#         'old_net_weight',
#         'dust_weight',
#         'old_metal_rate',
#         'total_old_gold_value',
#     )
#     list_filter = ('billing_details', 'old_metal')


@admin.register(EstimationSaleReturnItems)
class EstimationSaleReturnItemsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'estimation_details',
        'bill_details',
        'return_items',
        'tag_number',
        'item_details',
        'sub_item_details',
        'metal',
        'net_weight',
        'gross_weight',
        'tag_weight',
        'cover_weight',
        'loop_weight',
        'other_weight',
        'pieces',
        'total_pieces',
        'rate',
        'stone_rate',
        'diamond_rate',
        'wastage_percentage',
        'flat_wastage',
        'making_charge',
        'flat_making_charge',
        'stock_type',
        'calculation_type',
        'making_charge_calculation_type',
        'tax_percent',
        'additional_charges',
        'per_gram_weight_type',
        'total_stone_weight',
        'wastage_calculation_type',
        'total_diamond_weight',
        'gst',
        'total_rate',
        'without_gst_rate',
        'huid_rate',
    )
    list_filter = (
        'estimation_details',
        'bill_details',
        'return_items',
        'item_details',
        'sub_item_details',
        'metal',
        'stock_type',
        'calculation_type',
        'making_charge_calculation_type',
        'per_gram_weight_type',
        'wastage_calculation_type',
    )


@admin.register(EstimationReturnStoneDetails)
class EstimationReturnStoneDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'estimation_details',
        'estimation_return_item',
        'stone_name',
        'stone_pieces',
        'stone_weight',
        'stone_weight_type',
        'stone_rate',
        'stone_rate_type',
        'include_stone_weight',
        'total_stone_value',
    )
    list_filter = (
        'estimation_details',
        'estimation_return_item',
        'stone_name',
        'stone_weight_type',
        'stone_rate_type',
        'include_stone_weight',
    )


@admin.register(EstimationReturnDiamondDetails)
class EstimationReturnDiamondDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'estimation_details',
        'estimation_return_item',
        'diamond_name',
        'diamond_pieces',
        'diamond_weight',
        'diamond_weight_type',
        'diamond_rate',
        'diamond_rate_type',
        'include_diamond_weight',
        'total_diamond_value',
    )
    list_filter = (
        'estimation_details',
        'estimation_return_item',
        'diamond_name',
        'diamond_weight_type',
        'diamond_rate_type',
        'include_diamond_weight',
    )


@admin.register(EstimationApproval)
class EstimationApprovalAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'estimation_details',
        'estimation_status',
        'approved_at',
        'approved_by',
    )
    list_filter = (
        'estimation_details',
        'estimation_status',
        'approved_at',
        'approved_by',
    )


@admin.register(BillingSaleReturnItems)
class BillingSaleReturnItemsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'billing_details',
        'return_bill_details',
        'return_items',
        'tag_number',
        'item_details',
        'sub_item_details',
        'metal',
        'net_weight',
        'gross_weight',
        'tag_weight',
        'cover_weight',
        'loop_weight',
        'other_weight',
        'pieces',
        'total_pieces',
        'rate',
        'stone_rate',
        'diamond_rate',
        'wastage_percentage',
        'flat_wastage',
        'making_charge',
        'flat_making_charge',
        'stock_type',
        'calculation_type',
        'making_charge_calculation_type',
        'tax_percent',
        'additional_charges',
        'per_gram_weight_type',
        'total_stone_weight',
        'wastage_calculation_type',
        'total_diamond_weight',
        'gst',
        'total_rate',
        'without_gst_rate',
        'huid_rate',
    )
    list_filter = (
        'billing_details',
        'return_bill_details',
        'return_items',
        'item_details',
        'sub_item_details',
        'metal',
        'stock_type',
        'calculation_type',
        'making_charge_calculation_type',
        'per_gram_weight_type',
        'wastage_calculation_type',
    )


@admin.register(BillingReturnStoneDetails)
class BillingReturnStoneDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'billing_details',
        'billing_return_item',
        'stone_name',
        'stone_pieces',
        'stone_weight',
        'stone_weight_type',
        'stone_rate',
        'stone_rate_type',
        'include_stone_weight',
        'total_stone_value',
    )
    list_filter = (
        'billing_details',
        'billing_return_item',
        'stone_name',
        'stone_weight_type',
        'stone_rate_type',
        'include_stone_weight',
    )


@admin.register(BillingReturnDiamondDetails)
class BillingReturnDiamondDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'billing_details',
        'billing_return_item',
        'diamond_name',
        'diamond_pieces',
        'diamond_weight',
        'diamond_weight_type',
        'diamond_rate',
        'diamond_rate_type',
        'include_diamond_weight',
        'total_diamond_value',
    )
    list_filter = (
        'billing_details',
        'billing_return_item',
        'diamond_name',
        'diamond_weight_type',
        'diamond_rate_type',
        'include_diamond_weight',
    )


@admin.register(BillNumber)
class BillNumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'bill_number', 'user')
    list_filter = ('user',)


@admin.register(BillID)
class BillIDAdmin(admin.ModelAdmin):
    list_display = ('id', 'bill_id')

@admin.register(BillingType)
class BillingTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'bill_type')