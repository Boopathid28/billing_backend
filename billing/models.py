from django.db import models
from customer.models import Customer
from accounts.models import *
from settings.models import StatusTable,PaymentStatus
from tagging.models import TaggedItems,StoneWeightType,RateType
from masters.models import TaxDetails,Metal,Purity,StoneDetails,GSTType, CashCounter
from product.models import Item,SubItem,CalculationType,WeightType,StockType
from organizations.models import *
from old_gold_management.models import *
from advance_payment.models import *
from suspense_management.models import *
from payment_management.models import *

class BillingType(models.Model):
    bill_type = models.CharField(max_length=50,verbose_name="Bill Type",unique=True)

    class Meta:
        db_table = 'bill_type'
        verbose_name = 'bill_type'
        verbose_name_plural = 'bill_types'

    def __str__(self) -> str:
        return self.bill_type

class EstimateDetails(models.Model):

    estimate_no=models.CharField(max_length=100,verbose_name="Estimate Number",unique=True)
    bill_type=models.ForeignKey(BillingType,verbose_name="Bill Type",on_delete=models.PROTECT,null=True,blank=True)
    estimation_date=models.DateTimeField(verbose_name="Estimation Date")
    customer_details=models.ForeignKey(Customer,verbose_name="Customer Details",on_delete=models.PROTECT)
    total_amount=models.FloatField(max_length=100,verbose_name="Total Amount",default=0.0)
    discount_percentage=models.FloatField(max_length=50,verbose_name="Discount Percentage",default=0.0,null=True,blank=True)
    discount_amount=models.FloatField(max_length=50,verbose_name="Discount Amount",default=0.0)
    chit_amount=models.FloatField(max_length=50,verbose_name="Chit Amount",default=0.0,null=True,blank=True)
    salereturn_amount=models.FloatField(max_length=50,verbose_name="Salereturn Amount",default=0.0)
    exchange_amount=models.FloatField(max_length=50,verbose_name="Exchange Amount",default=0.0)
    gst_type=models.ForeignKey(GSTType,verbose_name="GST Type",null=True,blank=True,on_delete=models.PROTECT,default=1)
    gst_percentage=models.FloatField(max_length=50,verbose_name="GST Percentage",default=0.0,null=True,blank=True)
    gst_amount=models.FloatField(max_length=50,verbose_name="GST Amount",default=0.0)
    payable_amount=models.FloatField(max_length=50,verbose_name="Payable Amount",default=0.0,null=True,blank=True)
    advance_amount=models.FloatField(max_length=50,verbose_name="Advance Amount",default=0.0,null=True,blank=True)
    balance_amount=models.FloatField(max_length=50,verbose_name="Balance Amount",default=0.0,null=True,blank=True)
    round_off_amount=models.FloatField(max_length=50,verbose_name="Round Off Amount",default=0.0,null=True,blank=True)
    is_billed=models.BooleanField(verbose_name="Is Billed",default=False)
    sale_return_type=models.IntegerField(verbose_name="Sale Return Type",null=True,blank=True)
    branch = models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.PROTECT)  
    created_by=models.ForeignKey(User,verbose_name="Created By",related_name="estimation_created_by",on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(verbose_name="Created At",null=True,blank=True)
    modified_by=models.ForeignKey(User,verbose_name="Modified By",related_name="estimation_modified_by",on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at=models.DateTimeField(verbose_name="Modified At",null=True,blank=True)

    class Meta:
        db_table = 'estimation_detail'
        verbose_name = 'estimation_detail'
        verbose_name_plural = 'estimation_details'

    def __str__(self) -> str:
        return self.estimate_no
    
class EstimationTagItems(models.Model):

    estimation_details=models.ForeignKey(EstimateDetails,verbose_name="Estimation Details",on_delete=models.CASCADE)
    estimation_tag_item=models.ForeignKey(TaggedItems,verbose_name="Estimation Tag Items",on_delete=models.DO_NOTHING)
    tag_number=models.IntegerField(verbose_name="Tag Number",null=True,blank=True,default=0)
    item_details=models.ForeignKey(Item,verbose_name="Item Details",on_delete=models.PROTECT,default=1)
    sub_item_details=models.ForeignKey(SubItem,verbose_name="SubItem Details",on_delete=models.PROTECT,default=1)
    metal=models.ForeignKey(Metal,verbose_name="Metal",on_delete=models.PROTECT,default=1)
    net_weight=models.FloatField(max_length=50,verbose_name="Net weight",null=True,blank=True,default=0.0)
    gross_weight=models.FloatField(max_length=50,verbose_name="Gross Weight",null=True,blank=True,default=0.0)
    pieces=models.IntegerField(verbose_name="Pieces",null=True,blank=True)
    total_pieces=models.IntegerField(verbose_name="Total Pieces",null=True,blank=True,default=0.0)
    rate=models.FloatField(max_length=50,verbose_name="Estimation Metal Rate",null=True,blank=True,default=0.0)
    stone_rate=models.FloatField(max_length=50,verbose_name="Stone Rate",null=True,blank=True,default=0.0)
    huid_rate=models.FloatField(max_length=50,verbose_name="Huid Rate",null=True,blank=True,default=0.0)
    diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True,default=0.0)
    wastage_percentage=models.FloatField(max_length=50,verbose_name="Wastage Percent",null=True,blank=True,default=0.0)
    flat_wastage=models.FloatField(max_length=50,verbose_name="Flat Wastage",null=True,blank=True,default=0.0)
    making_charge=models.FloatField(max_length=50,verbose_name="Making Charger Per Gram",null=True,blank=True,default=0.0)
    flat_making_charge=models.FloatField(max_length=50,verbose_name="Flat Making Charger",null=True,blank=True,default=0.0)
    stock_type=models.ForeignKey(StockType,verbose_name="Stock Type",on_delete=models.PROTECT,default=1)
    calculation_type=models.ForeignKey(CalculationType,verbose_name="Calculation Type",on_delete=models.PROTECT,default=1)
    making_charge_calculation_type=models.ForeignKey(WeightType,verbose_name="Making Charge Calculation Type",related_name="Making_charge_calculation",on_delete=models.PROTECT,null=True,blank=True,default=0.0)
    gst_percent=models.FloatField(max_length=50,verbose_name="Tax Percent",null=True,blank=True,default=0.0)
    additional_charges=models.FloatField(max_length=50,verbose_name="Additional Charges",null=True,blank=True,default=0.0)
    per_gram_weight_type=models.ForeignKey(WeightType,verbose_name="Per gram weight type",related_name="per_gram_weight_type",on_delete=models.PROTECT,null=True,blank=True,default=0.0)
    total_stone_weight=models.FloatField(max_length=50,verbose_name="Total Stone Weight",null=True,blank=True,default=0.0)
    wastage_calculation_type=models.ForeignKey(WeightType,verbose_name="Wastage Calculation Type",related_name="Wastage_calculation",on_delete=models.PROTECT,null=True,blank=True,default=0.0)
    total_diamond_weight=models.FloatField(max_length=50,verbose_name="Tax Diamond Weight",null=True,blank=True,default=0.0)
    gst=models.FloatField(max_length=50,verbose_name="GST",null=True,blank=True,default=0.0)
    total_amount=models.FloatField(max_length=50,verbose_name="Total Rate",null=True,blank=True,default=0.0)
    with_gst_total_rate=models.FloatField(max_length=50,verbose_name="Without Gst Rate",null=True,blank=True,default=0.0)
    employee_id = models.ForeignKey(Staff,verbose_name="Employee Id",null=True,blank=True,on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'estimation_tag_value'
        verbose_name = 'estimation_tag_value'
        verbose_name_plural = 'estimation_tag_values'

    def __str__(self) -> str:
        return f"{self.estimation_details}"
    
class EstimationOldGold(models.Model):

    estimation_details=models.ForeignKey(EstimateDetails,verbose_name="Estimation Details",on_delete=models.CASCADE,default=1)
    old_gold_no=models.CharField(max_length=100,verbose_name="Oldgold Number")
    old_metal = models.ForeignKey(Metal,verbose_name="Metal",on_delete=models.PROTECT)
    old_gross_weight = models.FloatField(verbose_name="Old Gross Weight",default=0.0)
    old_reduce_weight = models.FloatField(verbose_name="Old Reduce Weight",default=0.0)
    old_rate = models.FloatField(verbose_name="Old Rate",default=0.0)
    old_touch = models.FloatField(verbose_name="Old Touch",default=0.0)
    old_dust_weight = models.FloatField(verbose_name="Old Dust Weight",default=0.0)
    old_net_weight = models.FloatField(verbose_name="Old Net Weight",default=0.0)
    old_amount = models.FloatField(verbose_name="Old Amount",default=0.0)
    gst_amount = models.FloatField(verbose_name="GST Amount",default=0.0)
    total_amount = models.FloatField(verbose_name="Total Amount",default=0.0)
    employee_id = models.ForeignKey(Staff,verbose_name="Employee Id",null=True,blank=True,on_delete=models.PROTECT)

    class Meta:
        db_table = 'estimation_old_gold_value'
        verbose_name = 'estimation_old_gold_value'
        verbose_name_plural = 'estimation_old_gold_values'

    def __str__(self) -> str:
        return self.old_gold_no
    
    
class EstimationStoneDetails(models.Model):
    estimation_details=models.ForeignKey(EstimateDetails,verbose_name="Estimate Details",on_delete=models.CASCADE)
    estimation_item_details=models.ForeignKey(EstimationTagItems,verbose_name="Estimation Item Details",on_delete=models.CASCADE)
    stone_name=models.ForeignKey(StoneDetails,verbose_name="Stone Name",on_delete=models.PROTECT)
    stone_pieces=models.IntegerField(verbose_name="Stone Pieces",null=True,blank=True)
    stone_weight=models.FloatField(max_length=50,verbose_name="Stone Weight",null=True,blank=True)
    stone_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    stone_rate=models.FloatField(max_length=50,verbose_name="Stone Rate",null=True,blank=True)
    stone_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    include_stone_weight=models.BooleanField(verbose_name="Include Stone Weight",default=True)
    total_stone_value=models.FloatField(max_length=50,verbose_name="Total Stone Value",null=True,blank=True)

    class Meta:
        db_table = 'estimation_item_stone'
        verbose_name = 'estimation_item_stone'
        verbose_name_plural = 'estimation_item_stones'

    def __str__(self) -> str:
        return self.stone_pieces
    

class EstimationDiamondDetails(models.Model):
    estimation_details=models.ForeignKey(EstimateDetails,verbose_name="Estimate Details",on_delete=models.CASCADE)
    estimation_item_details=models.ForeignKey(EstimationTagItems,verbose_name="Estimation Item Details",on_delete=models.CASCADE)
    diamond_name=models.ForeignKey(StoneDetails,verbose_name="Diamond Name",on_delete=models.PROTECT)
    diamond_pieces=models.IntegerField(verbose_name="Diamond Pieces",null=True,blank=True)
    diamond_weight=models.FloatField(max_length=50,verbose_name="Diamond Weight",null=True,blank=True)
    diamond_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True)
    diamond_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    include_diamond_weight=models.BooleanField(verbose_name="Include Diamond Weight",default=True)
    total_diamond_value=models.FloatField(max_length=50,verbose_name="Total Diamond Value",null=True,blank=True)

    class Meta:
        db_table = 'estimation_item_diamond'
        verbose_name = 'estimation_item_diamond'
        verbose_name_plural = 'estimation_item_diamonds'

    def __str__(self) -> str:
        return self.diamond_pieces

class EstimationOldPurchaseDetails(models.Model):
    
    estimation_details = models.ForeignKey(EstimateDetails,verbose_name="Estimation Details",on_delete=models.CASCADE)
    old_purchase_details = models.ForeignKey(OldGoldBillDetails,verbose_name="Old Purchase Details",on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'estimation_old_purchase_details'
        verbose_name = 'estimation_old_purchase_details'
        verbose_name_plural = 'estimation_old_purchase_details'
        
    def __str__(self) -> str:
        return self.estimation_details.estimate_no
    
class EstimationAdvanceDetails(models.Model):
    
    estimation_details = models.ForeignKey(EstimateDetails,verbose_name="Estimation Details",on_delete=models.CASCADE)
    advance_details = models.ForeignKey(AdvanceDetails,verbose_name="Advance Details",on_delete=models.PROTECT)
    redeem_weight = models.FloatField(verbose_name="Redeem Weight",default=0.0)
    redeem_metal_rate = models.FloatField(verbose_name="Redeem Metal Rate",default=0.0)
    redeem_metal_value = models.FloatField(verbose_name="Redeem Metal Value",default=0.0)
    redeem_amount = models.FloatField(verbose_name="Redeem Amount",default=0.0)
    total_amount = models.FloatField(verbose_name="Total Amount",default=0.0)
    
    class Meta:
        db_table = 'estimation_advance_details'
        verbose_name = 'estimation_advance_details'
        verbose_name_plural = 'estimation_advance_details'
        
    def __str__(self) -> str:
        return self.estimation_details.estimate_no
    

class EstimationChitDetails(models.Model):
    
    estimation_details = models.ForeignKey(EstimateDetails,verbose_name="Estimation Details",on_delete=models.CASCADE)
    scheme_account_number = models.CharField(max_length=150,verbose_name="Scheme Account Number")
    scheme_weight = models.FloatField(verbose_name="Scheme Weight",default=0.0)
    scheme_amount = models.FloatField(verbose_name="Scheme Amount",default=0.0)
    bonus_amount = models.FloatField(verbose_name="Bonus Amount",default=0.0)
    total_amount = models.FloatField(verbose_name="Total Amount",default=0.0)
    
    class Meta:
        db_table = 'estimation_chit_details'
        verbose_name = 'estimation_chit_details'
        verbose_name_plural = 'estimation_chit_details'
        
    def __str__(self) -> str:
        return self.estimation_details.estimate_no
    

# class BillingDetails(models.Model):

#     estimation_details=models.JSONField(default=list,null=True)
#     bill_type=models.ForeignKey(BillingType,verbose_name="Bill Type",on_delete=models.PROTECT,null=True,blank=True)
#     bill_no=models.CharField(max_length=20,verbose_name="Bill Number",unique=True,null=True,blank=True)
#     bill_date=models.DateTimeField(verbose_name="Bill Date",null=True,blank=True)
#     customer_details=models.ForeignKey(Customer,verbose_name="Customer Details",on_delete=models.PROTECT)
#     customer_mobile=models.CharField(max_length=10,verbose_name="Customer Mobile",null=True)
#     branch = models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT,null=True,blank=True)
#     cash_counter=models.ForeignKey(CashCounter,verbose_name="Cash counter",on_delete=models.PROTECT,null=True,blank=True)
#     is_issued=models.BooleanField(verbose_name="Is issued",default=False)
#     created_by=models.ForeignKey(User,verbose_name="Created By",related_name="billing_created_by",on_delete=models.DO_NOTHING)
#     payment_status=models.ForeignKey(PaymentStatus,verbose_name="Payment Status",on_delete=models.PROTECT,null=True,blank=True,default=1)
#     created_at=models.DateTimeField(verbose_name="Created At",null=True,blank=True)
#     modified_by=models.ForeignKey(User,verbose_name="Modified By",related_name="billing_modified_by",on_delete=models.DO_NOTHING,null=True,blank=True)
#     modified_at=models.DateTimeField(verbose_name="Modified At",null=True,blank=True)

#     class Meta:
#         db_table = 'billing_detail'
#         verbose_name = 'billing_detail'
#         verbose_name_plural = 'billing_details'

#     def __str__(self) -> str:
#         return self.bill_no
    
# class BillingTagItems(models.Model):

#     billing_details=models.ForeignKey(BillingDetails,verbose_name="Billing Details",on_delete=models.CASCADE)
#     billing_tag_item=models.ForeignKey(TaggedItems,verbose_name="Billing Tag Items",on_delete=models.DO_NOTHING)
#     tag_number=models.IntegerField(verbose_name="Tag Number",null=True,blank=True,default=0)
#     item_details=models.ForeignKey(Item,verbose_name="Item Details",on_delete=models.PROTECT,default=1)
#     sub_item_details=models.ForeignKey(SubItem,verbose_name="SubItem Details",on_delete=models.PROTECT,default=1)
#     metal=models.ForeignKey(Metal,verbose_name="Metal",on_delete=models.PROTECT,default=1)
#     net_weight=models.FloatField(max_length=50,verbose_name="Net weight",null=True,blank=True,default=0.0)
#     gross_weight=models.FloatField(max_length=50,verbose_name="Gross Weight",null=True,blank=True,default=0.0)
#     tag_weight=models.FloatField(max_length=50,verbose_name="Tag Weight",null=True,blank=True,default=0.0)
#     cover_weight=models.FloatField(max_length=50,verbose_name="Tag Weight",null=True,blank=True,default=0.0)
#     loop_weight=models.FloatField(max_length=50,verbose_name="Tag Weight",null=True,blank=True,default=0.0)
#     other_weight=models.FloatField(max_length=50,verbose_name="Tag Weight",null=True,blank=True,default=0.0)
#     pieces=models.IntegerField(verbose_name="Pieces",null=True,blank=True)
#     total_pieces=models.IntegerField(verbose_name="Total Pieces",null=True,blank=True,default=0.0)
#     rate=models.FloatField(max_length=50,verbose_name="Estimation Metal Rate",null=True,blank=True,default=0.0)
#     stone_rate=models.FloatField(max_length=50,verbose_name="Stone Rate",null=True,blank=True,default=0.0)
#     huid_rate=models.FloatField(max_length=50,verbose_name="Huid Rate",null=True,blank=True,default=0.0)
#     diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True,default=0.0)
#     wastage_percentage=models.FloatField(max_length=50,verbose_name="Wastage Percent",null=True,blank=True,default=0.0)
#     flat_wastage=models.FloatField(max_length=50,verbose_name="Flat Wastage",null=True,blank=True,default=0.0)
#     making_charge=models.FloatField(max_length=50,verbose_name="Making Charger Per Gram",null=True,blank=True,default=0.0)
#     flat_making_charge=models.FloatField(max_length=50,verbose_name="Flat Making Charger",null=True,blank=True,default=0.0)
#     stock_type=models.ForeignKey(StockType,verbose_name="Stock Type",on_delete=models.PROTECT,default=1)
#     calculation_type=models.ForeignKey(CalculationType,verbose_name="Calculation Type",on_delete=models.PROTECT,default=1)
#     making_charge_calculation_type=models.ForeignKey(WeightType,verbose_name="Making Charge Calculation Type",related_name="billing_Making_charge_calculation",on_delete=models.PROTECT,null=True,blank=True,default=0.0)
#     tax_percent=models.FloatField(max_length=50,verbose_name="Tax Percent",null=True,blank=True,default=0.0)
#     additional_charges=models.FloatField(max_length=50,verbose_name="Additional Charges",null=True,blank=True,default=0.0)
#     per_gram_weight_type=models.ForeignKey(WeightType,verbose_name="Per gram weight type",related_name="billing_per_gram_weight_type",on_delete=models.PROTECT,null=True,blank=True,default=0.0)
#     total_stone_weight=models.FloatField(max_length=50,verbose_name="Total Stone Weight",null=True,blank=True,default=0.0)
#     wastage_calculation_type=models.ForeignKey(WeightType,verbose_name="Wastage Calculation Type",related_name="billing_Wastage_calculation",on_delete=models.PROTECT,null=True,blank=True,default=0.0)
#     total_diamond_weight=models.FloatField(max_length=50,verbose_name="Tax Diamond Weight",null=True,blank=True,default=0.0)
#     gst=models.FloatField(max_length=50,verbose_name="GST",null=True,blank=True,default=0.0)
#     total_rate=models.FloatField(max_length=50,verbose_name="Total Rate",null=True,blank=True,default=0.0)
#     without_gst_rate=models.FloatField(max_length=50,verbose_name="Without Gst Rate",null=True,blank=True,default=0.0)
#     is_returned = models.BooleanField(verbose_name="Returned",default=False)
#     employee_id = models.ForeignKey(Staff,verbose_name="Employee Id",null=True,blank=True,on_delete=models.PROTECT)
    
#     class Meta:
#         db_table = 'billing_tag_value'
#         verbose_name = 'billing_tag_value'
#         verbose_name_plural = 'billing_tag_values'

#     def __str__(self) -> str:
#         return f"{self.billing_details}"
    
# class BillingStoneDetails(models.Model):
#     billing_details=models.ForeignKey(BillingDetails,verbose_name="Billing Details",on_delete=models.CASCADE)
#     billing_item_details=models.ForeignKey(BillingTagItems,verbose_name="Billing Item Details",on_delete=models.CASCADE)
#     stone_name=models.ForeignKey(StoneDetails,verbose_name="Stone Name",on_delete=models.PROTECT)
#     stone_pieces=models.IntegerField(verbose_name="Stone Pieces",null=True,blank=True)
#     stone_weight=models.FloatField(max_length=50,verbose_name="Stone Weight",null=True,blank=True)
#     stone_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
#     stone_rate=models.FloatField(max_length=50,verbose_name="Stone Rate",null=True,blank=True)
#     stone_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
#     include_stone_weight=models.BooleanField(verbose_name="Include Stone Weight",default=True)
#     total_stone_value=models.FloatField(max_length=50,verbose_name="Total Stone Value",null=True,blank=True)

#     class Meta:
#         db_table = 'billing_item_stone'
#         verbose_name = 'billing_item_stone'
#         verbose_name_plural = 'billing_item_stones'

#     def __str__(self) -> str:
#         return self.stone_pieces
    
# class BillingDiamondDetails(models.Model):
#     billing_details=models.ForeignKey(BillingDetails,verbose_name="Billing Details",on_delete=models.CASCADE)
#     billing_item_details=models.ForeignKey(BillingTagItems,verbose_name="Billing Item Details",on_delete=models.CASCADE)
#     diamond_name=models.ForeignKey(StoneDetails,verbose_name="Diamond Name",on_delete=models.PROTECT)
#     diamond_pieces=models.IntegerField(verbose_name="Diamond Pieces",null=True,blank=True)
#     diamond_weight=models.FloatField(max_length=50,verbose_name="Diamond Weight",null=True,blank=True)
#     diamond_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
#     diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True)
#     diamond_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
#     include_diamond_weight=models.BooleanField(verbose_name="Include Diamond Weight",default=True)
#     total_diamond_value=models.FloatField(max_length=50,verbose_name="Total Diamond Value",null=True,blank=True)

#     class Meta:
#         db_table = 'billing_item_diamond'
#         verbose_name = 'billing_item_diamond'
#         verbose_name_plural = 'billing_item_diamonds'

#     def __str__(self) -> str:
#         return self.diamond_pieces
    
# class BillingOldGold(models.Model):

#     billing_details=models.ForeignKey(BillingDetails,verbose_name="Billing Details",on_delete=models.CASCADE,default=1)
#     item_name = models.CharField(max_length=150,verbose_name="Item Name",null=True,blank=True)
#     old_metal=models.ForeignKey(Metal,verbose_name="Old Metal",on_delete=models.DO_NOTHING)
#     old_gold_no=models.CharField(max_length=100,verbose_name="Oldgold Number")
#     metal_rate=models.FloatField(max_length=50,verbose_name="metal Rate",null=True,blank=True,default=0.0)
#     today_metal_rate=models.FloatField(max_length=50,verbose_name="Today Metal Rate",null=True,blank=True,default=0.0)
#     old_gross_weight=models.FloatField(max_length=50,verbose_name="Old Gross Weight",null=True,blank=True,default=0.0)
#     old_net_weight=models.FloatField(max_length=50,verbose_name="Old Net Weight",null=True,blank=True,default=0.0)
#     dust_weight = models.FloatField(max_length=50,verbose_name="Dust Weight",null=True,blank=True,default=0.0)
#     old_metal_rate=models.FloatField(max_length=50,verbose_name="Old Metal Rate",null=True,blank=True,default=0.0)
#     total_old_gold_value=models.FloatField(max_length=100,verbose_name="Total Old Gold Value",null=True,blank=True,default=0.0)
#     purity = models.ForeignKey(Purity,verbose_name="oldgold_purity",null=True,blank=True,on_delete = models.PROTECT)
#     is_transfered = models.BooleanField(verbose_name="Tranfer Status", default=False)

#     class Meta:
#         db_table = 'billing_old_gold_value'
#         verbose_name = 'billing_old_gold_value'
#         verbose_name_plural = 'billing_old_gold_values'

#     def __str__(self) -> str:
#         return self.old_metal_rate


class BillingDetails(models.Model):
    # estimation_details=models.JSONField(default=list,null=True)
    bill_type=models.ForeignKey(BillingType,verbose_name="Bill Type",on_delete=models.PROTECT,null=True,blank=True)
    bill_id = models.CharField(max_length=150,verbose_name="Bill ID",unique=True)
    bill_date = models.DateTimeField(verbose_name="Bill Date")
    customer_details = models.ForeignKey(Customer,verbose_name="Customer Details",on_delete=models.PROTECT)
    total_amount = models.FloatField(verbose_name="Total Amount",default=0.0)
    gst_type = models.ForeignKey(GSTType,verbose_name="Gst Type",default=1,on_delete=models.PROTECT)
    gst_amount = models.FloatField(verbose_name="GST Amount",default=0.0)
    discount_amount = models.FloatField(verbose_name="Discount Amount",default=0.0)
    roundoff_amount = models.FloatField(verbose_name="Roundoff Amount",default=0.0)
    payable_amount = models.FloatField(verbose_name="Payable Amount",default=0.0)
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name="Created at",null=True,blank=True)
    created_by = models.ForeignKey(User,verbose_name="Created by",null=True,blank=True,on_delete=models.PROTECT)
        
    class Meta:
        db_table = 'billing_details'
        verbose_name = 'billing_details'
        verbose_name_plural = 'billing_details'
        
    def __str__(self) -> str:
        return self.bill_id
    
class BillingEstimationDetails(models.Model):
    
    billing_details = models.ForeignKey(BillingDetails,verbose_name="Billing Details",on_delete=models.CASCADE)
    # estimation_details = models.ForeignKey(EstimateDetails,verbose_name="Estimation Details",on_delete=models.PROTECT)
    estimation_details=models.JSONField(default=list,null=True)
    
    class Meta:
        db_table = 'billing_estimation_details'
        verbose_name = 'billing_estimation_details'
        verbose_name_plural = 'billing_estimation_details'
        
    def __str__(self) -> str:
        return self.billing_details.bill_id
    
class BillingParticularDetails(models.Model):
    
    billing_details = models.ForeignKey(BillingDetails,verbose_name="Billing Details",on_delete=models.CASCADE)
    tag_details = models.ForeignKey(TaggedItems,verbose_name="Tag Details",on_delete=models.PROTECT)
    rate = models.FloatField(verbose_name="Rate",default=0.0)
    pieces = models.IntegerField(verbose_name="Pieces",default=0)
    gross_weight = models.FloatField(verbose_name="Gross Weight",default=0.0)
    # reduce_weight = models.FloatField(verbose_name="Reduce Weight",default=0.0)
    net_weight = models.FloatField(verbose_name="Net Weight",default=0.0)
    wastage_percent = models.FloatField(verbose_name="Wastage Percent",default=0.0)
    flat_wastage = models.FloatField(verbose_name="Flat Wastage",default=0.0)
    making_charge_per_gram = models.FloatField(verbose_name="Making Charge Per Gram",default=0.0)
    flat_making_charge = models.FloatField(verbose_name="Flat Making Charge",default=0.0)
    stone_amount = models.FloatField(verbose_name="Stone Amount",default=0.0)
    diamond_amount = models.FloatField(verbose_name="Diamond Amount",default=0.0)
    huid_amount = models.FloatField(verbose_name="Huid Amount",default=0.0)
    total_amount = models.FloatField(verbose_name="Total Amount",default=0.0)
    gst_percent = models.FloatField(verbose_name="Gst Percent",default=0.0,null=True,blank=True)
    gst_amount = models.FloatField(verbose_name="Gst Amount",default=0.0)
    payable_amount = models.FloatField(verbose_name="Payable Amount",default=0.0)
    
    class Meta:
        db_table = 'billing_particulars'
        verbose_name = 'billing_particulars'
        verbose_name_plural = 'billing_particulars'
        
    def __str__(self) -> str:
        return self.billing_details.bill_id
    
class BillingParticularStoneDetails(models.Model):
    
    billing_particular_details = models.ForeignKey(BillingParticularDetails,verbose_name="Billing Particular Details",on_delete=models.CASCADE)
    stone_name = models.ForeignKey(StoneDetails,verbose_name="Stone Details",on_delete=models.PROTECT)
    stone_pieces = models.IntegerField(verbose_name="Stone Pieces",default=0)
    stone_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT,default=1)
    stone_weight = models.FloatField(verbose_name="Stone Weight",default=0.0)
    stone_rate=models.FloatField(max_length=50,verbose_name="Stone Rate",null=True,blank=True)
    stone_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT,default=1)
    stone_amount = models.FloatField(verbose_name="Stone Amount",default=0.0)
    include_stone_weight=models.BooleanField(verbose_name="Include Stone Weight",default=True)

    class Meta:
        db_table = 'billing_particulars_stone'
        verbose_name = 'billing_particulars_stone'
        verbose_name_plural = 'billing_particulars_stone'
        
    def __str__(self) -> str:
        return self.billing_particular_details.billing_details.bill_id
    
class BillingParticularsDiamondDetails(models.Model):
    
    billing_particular_details = models.ForeignKey(BillingParticularDetails,verbose_name="Billing Particular Details",on_delete=models.CASCADE)
    diamond_name = models.ForeignKey(StoneDetails,verbose_name="Diamond Details",on_delete=models.PROTECT)
    diamond_pieces = models.IntegerField(verbose_name="Diamond Pieces",default=0)
    diamond_weight=models.FloatField(max_length=50,verbose_name="Diamond Weight",null=True,blank=True)
    diamond_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT,default=1)
    diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True)
    diamond_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT,default=1)
    diamond_amount = models.FloatField(verbose_name="Diamond Amount",default=0.0)
    include_diamond_weight=models.BooleanField(verbose_name="Include Stone Weight",default=True)
    
    class Meta:
        db_table = 'billing_particulars_diamond'
        verbose_name = 'billing_particulars_diamond'
        verbose_name_plural = 'billing_particulars_diamond'
        
    def __str__(self) -> str:
        return self.billing_particular_details.billing_details.bill_id
    
class BillingPaymentDetails(models.Model):
    
    billing_details = models.ForeignKey(BillingDetails,verbose_name="Billing Details",on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=150,verbose_name="Payment ID",unique=True)
    payment_date = models.DateTimeField(verbose_name="Payment Date")
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    created_by = models.ForeignKey(User,verbose_name="Created by",null=True,blank=True,on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'billing_payment_details'
        verbose_name = 'billing_payment_details'
        verbose_name_plural = 'billing_payment_details'
        
    def __str__(self) -> str:
        return self.billing_details.bill_id
    
class BillPaymentDenominationDetails(models.Model):
    
    payment_details = models.ForeignKey(BillingPaymentDetails,verbose_name="Bill Payment Details",on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMenthod,verbose_name="Payment Method",default=1,on_delete=models.PROTECT)
    payment_provider = models.ForeignKey(PaymentProviders,verbose_name="Payment Provider",null=True,blank=True,on_delete=models.PROTECT)
    paid_amount = models.FloatField(verbose_name="Paid Amount",default=0.0)
    remark = models.CharField(max_length=150,verbose_name="Remark",null=True,blank=True)
    
    class Meta:
        db_table = 'billing_payment_denominations'
        verbose_name = 'billing_payment_denominations'
        verbose_name_plural = 'billing_payment_denominations'
        
    def __str__(self) -> str:
        return self.payment_details.payment_id
    
    
class BillingExchangeDetails(models.Model):
    
    payment_details = models.ForeignKey(BillingPaymentDetails,verbose_name="Bill Payment Details",on_delete=models.CASCADE)
    old_purchase_details = models.OneToOneField(OldGoldBillDetails,verbose_name="Old Purchase Details",on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'billing_exchange_details'
        verbose_name = 'billing_exchange_details'
        verbose_name_plural = 'billing_exchange_details'
        
    def __str__(self) -> str:
        return self.payment_details.payment_id
    
class BillingAdvanceDetails(models.Model):
    
    payment_details = models.ForeignKey(BillingPaymentDetails,verbose_name="Bill Payment Details",on_delete=models.CASCADE)
    advance_details = models.ForeignKey(AdvanceDetails,verbose_name="Advance Details",on_delete=models.PROTECT)
    redeem_weight = models.FloatField(verbose_name="Redeem Weight",default=0.0)
    redeem_metal_rate = models.FloatField(verbose_name="Redeem Metal Rate",default=0.0)
    redeem_metal_value = models.FloatField(verbose_name="Redeem Metal Value",default=0.0)
    redeem_amount = models.FloatField(verbose_name="Redeem Amount",default=0.0)
    total_amount = models.FloatField(verbose_name="Total Amount",default=0.0)
    
    class Meta:
        db_table = 'billing_advance_details'
        verbose_name = 'billing_advance_details'
        verbose_name_plural = 'billing_advance_details'
        
    def __str__(self) -> str:
        return self.payment_details.payment_id 
    
    
class BillingChitDetails(models.Model):
    
    payment_details = models.ForeignKey(BillingPaymentDetails,verbose_name="Bill Payment Details",on_delete=models.CASCADE)
    scheme_account_number = models.CharField(max_length=150,verbose_name="Scheme Account Number")
    total_amount = models.FloatField(verbose_name="Total Amount",default=0.0)
    
    class Meta:
        db_table = 'billing_chit_details'
        verbose_name = 'billing_chit_details'
        verbose_name_plural = 'billing_chit_details'
        
    def __str__(self) -> str:
        return self.payment_details.payment_id
    
class BillingSuspenseDetails(models.Model):
    
    payment_details = models.ForeignKey(BillingPaymentDetails,verbose_name="Bill Payment Details",on_delete=models.CASCADE)
    suspense_details = models.ForeignKey(SuspenseDetails,verbose_name="Suspense_details",on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'billing_suspense_details'
        verbose_name = 'billing_suspense_details'
        verbose_name_plural = 'billing_suspense_details'
        
    def __str__(self) -> str:
        return self.payment_details.payment_id
    
class EstimationSaleReturnItems(models.Model):
    estimation_details=models.ForeignKey(EstimateDetails,verbose_name="Estimation Details",on_delete=models.CASCADE)
    bill_details = models.ForeignKey(BillingDetails,verbose_name="Bill Details",on_delete=models.CASCADE,null=True,blank=True)
    return_items=models.ForeignKey(BillingParticularDetails,verbose_name="Return Items",on_delete=models.CASCADE,null=True,blank=True)
    tag_number=models.IntegerField(verbose_name="Tag Number",null=True,blank=True)
    item_details=models.ForeignKey(Item,verbose_name="Item Details",on_delete=models.PROTECT)
    sub_item_details=models.ForeignKey(SubItem,verbose_name="SubItem Details",on_delete=models.PROTECT)
    metal=models.ForeignKey(Metal,verbose_name="Metal",on_delete=models.PROTECT)
    net_weight=models.FloatField(max_length=50,verbose_name="Net weight",null=True,blank=True,default=0.0)
    gross_weight=models.FloatField(max_length=50,verbose_name="Gross Weight",null=True,blank=True,default=0.0)
    tag_weight=models.FloatField(max_length=50,verbose_name="Tag Weight",null=True,blank=True,default=0.0)
    cover_weight=models.FloatField(max_length=50,verbose_name="Tag Weight",null=True,blank=True,default=0.0)
    loop_weight=models.FloatField(max_length=50,verbose_name="Tag Weight",null=True,blank=True,default=0.0)
    other_weight=models.FloatField(max_length=50,verbose_name="Tag Weight",null=True,blank=True,default=0.0)
    pieces=models.IntegerField(verbose_name="Pieces",null=True,blank=True)
    total_pieces=models.IntegerField(verbose_name="Total Pieces",null=True,blank=True,default=0.0)
    rate=models.FloatField(max_length=50,verbose_name="Estimation Metal Rate",null=True,blank=True,default=0.0)
    stone_rate=models.FloatField(max_length=50,verbose_name="Stone Rate",null=True,blank=True,default=0.0)
    diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True,default=0.0)
    wastage_percentage=models.FloatField(max_length=50,verbose_name="Wastage Percent",null=True,blank=True,default=0.0)
    flat_wastage=models.FloatField(max_length=50,verbose_name="Flat Wastage",null=True,blank=True,default=0.0)
    making_charge=models.FloatField(max_length=50,verbose_name="Making Charger Per Gram",null=True,blank=True,default=0.0)
    flat_making_charge=models.FloatField(max_length=50,verbose_name="Flat Making Charger",null=True,blank=True,default=0.0)
    stock_type=models.ForeignKey(StockType,verbose_name="Stock Type",on_delete=models.PROTECT,default=1)
    calculation_type=models.ForeignKey(CalculationType,verbose_name="Calculation Type",on_delete=models.PROTECT)
    making_charge_calculation_type=models.ForeignKey(WeightType,verbose_name="Making Charge Calculation Type",related_name="estimation_return_Making_charge_calculation",on_delete=models.PROTECT,null=True,blank=True)
    tax_percent=models.FloatField(max_length=50,verbose_name="Tax Percent",null=True,blank=True,default=0.0)
    additional_charges=models.FloatField(max_length=50,verbose_name="Additional Charges",null=True,blank=True,default=0.0)
    per_gram_weight_type=models.ForeignKey(WeightType,verbose_name="Per gram weight type",related_name="estimation_return_per_gram_weight_type",on_delete=models.PROTECT,null=True,blank=True)
    total_stone_weight=models.FloatField(max_length=50,verbose_name="Total Stone Weight",null=True,blank=True,default=0.0)
    wastage_calculation_type=models.ForeignKey(WeightType,verbose_name="Wastage Calculation Type",related_name="estimation_return_Wastage_calculation",on_delete=models.PROTECT,null=True,blank=True)
    total_diamond_weight=models.FloatField(max_length=50,verbose_name="Tax Diamond Weight",null=True,blank=True,default=0.0)
    gst=models.FloatField(max_length=50,verbose_name="GST",null=True,blank=True,default=0.0)
    total_rate=models.FloatField(max_length=50,verbose_name="Total Rate",null=True,blank=True,default=0.0)
    without_gst_rate=models.FloatField(max_length=50,verbose_name="Without Gst Rate",null=True,blank=True,default=0.0)
    huid_rate=models.FloatField(max_length=50,verbose_name="Huid Rate",null=True,blank=True,default=0.0)
    
    class Meta:
        db_table = 'estimation_sale_return'
        verbose_name = 'estimation_sale_return'
        verbose_name_plural = 'estimation_sale_returns'

    def __str__(self) -> str:
        return self.estimation_details.estimate_no
    
class EstimationReturnStoneDetails(models.Model):
    estimation_details=models.ForeignKey(EstimateDetails,verbose_name="Estimation Details",on_delete=models.CASCADE)
    estimation_return_item=models.ForeignKey(EstimationSaleReturnItems,verbose_name="Estimation Return Item",on_delete=models.CASCADE)
    stone_name=models.ForeignKey(StoneDetails,verbose_name="Stone Name",on_delete=models.PROTECT)
    stone_pieces=models.IntegerField(verbose_name="Stone Pieces",null=True,blank=True)
    stone_weight=models.FloatField(max_length=50,verbose_name="Stone Weight",null=True,blank=True)
    stone_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    stone_rate=models.FloatField(max_length=50,verbose_name="Stone Rate",null=True,blank=True)
    stone_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    include_stone_weight=models.BooleanField(verbose_name="Include Stone Weight",default=True)
    total_stone_value=models.FloatField(max_length=50,verbose_name="Total Stone Value",null=True,blank=True)

    class Meta:
        db_table = 'estimation_return_stone'
        verbose_name = 'estimation_return_stone'
        verbose_name_plural = 'estimation_return_stones'

    def __str__(self) -> str:
        return self.stone_pieces
    
class EstimationReturnDiamondDetails(models.Model):
    estimation_details=models.ForeignKey(EstimateDetails,verbose_name="Estimation Details",on_delete=models.CASCADE)
    estimation_return_item=models.ForeignKey(EstimationSaleReturnItems,verbose_name="Estimation Return Item",on_delete=models.CASCADE)
    diamond_name=models.ForeignKey(StoneDetails,verbose_name="Diamond Name",on_delete=models.PROTECT)
    diamond_pieces=models.IntegerField(verbose_name="Diamond Pieces",null=True,blank=True)
    diamond_weight=models.FloatField(max_length=50,verbose_name="Diamond Weight",null=True,blank=True)
    diamond_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True)
    diamond_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    include_diamond_weight=models.BooleanField(verbose_name="Include Diamond Weight",default=True)
    total_diamond_value=models.FloatField(max_length=50,verbose_name="Total Diamond Value",null=True,blank=True)

    class Meta:
        db_table = 'estimation_return_diamond'
        verbose_name = 'estimation_return_diamond'
        verbose_name_plural = 'estimation_return_diamonds'

    def __str__(self) -> str:
        return self.diamond_pieces
    
class EstimationApproval(models.Model):

    estimation_details=models.ForeignKey(EstimateDetails,verbose_name="Estimation Details",on_delete=models.CASCADE,default=1)
    estimation_status=models.ForeignKey(StatusTable,verbose_name="Estimation Status",on_delete=models.CASCADE,default=1)
    approved_at=models.DateTimeField(verbose_name="Approved At",null=True,blank=True)
    approved_by=models.ForeignKey(User,verbose_name="Approved by",on_delete=models.DO_NOTHING)
       
    class Meta:
        db_table = 'estimation_approval'
        verbose_name = 'estimation_approval'
        verbose_name_plural = 'estimation_approvals'

    def __str__(self) -> str:
        return self.estimation_details
    
    
class BillingSaleReturnItems(models.Model):
    billing_details=models.ForeignKey(BillingDetails,verbose_name="Estimation Details",related_name='new_bill_details',on_delete=models.CASCADE)
    return_bill_details = models.ForeignKey(BillingDetails,verbose_name="Bill Details",related_name='old_bill_details',on_delete=models.PROTECT)
    return_items=models.ForeignKey(BillingParticularDetails,verbose_name="Return Items",on_delete=models.CASCADE)
    tag_number=models.IntegerField(verbose_name="Tag Number",null=True,blank=True,default=0)
    item_details=models.ForeignKey(Item,verbose_name="Item Details",on_delete=models.PROTECT,default=1)
    sub_item_details=models.ForeignKey(SubItem,verbose_name="SubItem Details",on_delete=models.PROTECT,default=1)
    metal=models.ForeignKey(Metal,verbose_name="Metal",on_delete=models.PROTECT,default=1)
    net_weight=models.FloatField(max_length=50,verbose_name="Net weight",null=True,blank=True,default=0.0)
    gross_weight=models.FloatField(max_length=50,verbose_name="Gross Weight",null=True,blank=True,default=0.0)
    tag_weight=models.FloatField(max_length=50,verbose_name="Tag Weight",null=True,blank=True,default=0.0)
    cover_weight=models.FloatField(max_length=50,verbose_name="Tag Weight",null=True,blank=True,default=0.0)
    loop_weight=models.FloatField(max_length=50,verbose_name="Tag Weight",null=True,blank=True,default=0.0)
    other_weight=models.FloatField(max_length=50,verbose_name="Tag Weight",null=True,blank=True,default=0.0)
    pieces=models.IntegerField(verbose_name="Pieces",null=True,blank=True)
    total_pieces=models.IntegerField(verbose_name="Total Pieces",null=True,blank=True,default=0.0)
    rate=models.FloatField(max_length=50,verbose_name="Estimation Metal Rate",null=True,blank=True,default=0.0)
    stone_rate=models.FloatField(max_length=50,verbose_name="Stone Rate",null=True,blank=True,default=0.0)
    diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True,default=0.0)
    wastage_percentage=models.FloatField(max_length=50,verbose_name="Wastage Percent",null=True,blank=True,default=0.0)
    flat_wastage=models.FloatField(max_length=50,verbose_name="Flat Wastage",null=True,blank=True,default=0.0)
    making_charge=models.FloatField(max_length=50,verbose_name="Making Charger Per Gram",null=True,blank=True,default=0.0)
    flat_making_charge=models.FloatField(max_length=50,verbose_name="Flat Making Charger",null=True,blank=True,default=0.0)
    stock_type=models.ForeignKey(StockType,verbose_name="Stock Type",on_delete=models.PROTECT,default=1)
    calculation_type=models.ForeignKey(CalculationType,verbose_name="Calculation Type",on_delete=models.PROTECT,default=1)
    making_charge_calculation_type=models.ForeignKey(WeightType,verbose_name="Making Charge Calculation Type",related_name="billing_return_Making_charge_calculation",on_delete=models.PROTECT,null=True,blank=True,default=0.0)
    tax_percent=models.FloatField(max_length=50,verbose_name="Tax Percent",null=True,blank=True,default=0.0)
    additional_charges=models.FloatField(max_length=50,verbose_name="Additional Charges",null=True,blank=True,default=0.0)
    per_gram_weight_type=models.ForeignKey(WeightType,verbose_name="Per gram weight type",related_name="billing_return_per_gram_weight_type",on_delete=models.PROTECT,null=True,blank=True,default=0.0)
    total_stone_weight=models.FloatField(max_length=50,verbose_name="Total Stone Weight",null=True,blank=True,default=0.0)
    wastage_calculation_type=models.ForeignKey(WeightType,verbose_name="Wastage Calculation Type",related_name="billing_return_Wastage_calculation",on_delete=models.PROTECT,null=True,blank=True,default=0.0)
    total_diamond_weight=models.FloatField(max_length=50,verbose_name="Tax Diamond Weight",null=True,blank=True,default=0.0)
    gst=models.FloatField(max_length=50,verbose_name="GST",null=True,blank=True,default=0.0)
    total_rate=models.FloatField(max_length=50,verbose_name="Total Rate",null=True,blank=True,default=0.0)
    without_gst_rate=models.FloatField(max_length=50,verbose_name="Without Gst Rate",null=True,blank=True,default=0.0)
    huid_rate=models.FloatField(max_length=50,verbose_name="Huid Rate",null=True,blank=True,default=0.0)
    

    class Meta:
        db_table = 'billing_sale_return'
        verbose_name = 'billing_sale_return'
        verbose_name_plural = 'billing_sale_returns'

    def __str__(self) -> str:
        return self.billing_details
    
class BillingReturnStoneDetails(models.Model):
    billing_details=models.ForeignKey(BillingDetails,verbose_name="Estimation Details",on_delete=models.CASCADE)
    billing_return_item=models.ForeignKey(BillingSaleReturnItems,verbose_name="Estimation Return Item",on_delete=models.CASCADE)
    stone_name=models.ForeignKey(StoneDetails,verbose_name="Stone Name",on_delete=models.PROTECT)
    stone_pieces=models.IntegerField(verbose_name="Stone Pieces",null=True,blank=True)
    stone_weight=models.FloatField(max_length=50,verbose_name="Stone Weight",null=True,blank=True)
    stone_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    stone_rate=models.FloatField(max_length=50,verbose_name="Stone Rate",null=True,blank=True)
    stone_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    include_stone_weight=models.BooleanField(verbose_name="Include Stone Weight",default=True)
    total_stone_value=models.FloatField(max_length=50,verbose_name="Total Stone Value",null=True,blank=True)

    class Meta:
        db_table = 'billing_return_stone'
        verbose_name = 'billing_return_stone'
        verbose_name_plural = 'billing_return_stones'

    def __str__(self) -> str:
        return f"{self.stone_pieces}"
    
class BillingReturnDiamondDetails(models.Model):
    billing_details=models.ForeignKey(BillingDetails,verbose_name="Estimation Details",on_delete=models.CASCADE)
    billing_return_item=models.ForeignKey(BillingSaleReturnItems,verbose_name="Estimation Return Item",on_delete=models.CASCADE)
    diamond_name=models.ForeignKey(StoneDetails,verbose_name="Diamond Name",on_delete=models.PROTECT)
    diamond_pieces=models.IntegerField(verbose_name="Diamond Pieces",null=True,blank=True)
    diamond_weight=models.FloatField(max_length=50,verbose_name="Diamond Weight",null=True,blank=True)
    diamond_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True)
    diamond_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    include_diamond_weight=models.BooleanField(verbose_name="Include Diamond Weight",default=True)
    total_diamond_value=models.FloatField(max_length=50,verbose_name="Total Diamond Value",null=True,blank=True)

    class Meta:
        db_table = 'billing_return_diamond'
        verbose_name = 'billing_return_diamond'
        verbose_name_plural = 'billing_return_diamonds'

    def __str__(self) -> str:
        return  f"{self.diamond_pieces}"
    

class BillNumber(models.Model):
    bill_number=models.CharField(max_length=10,verbose_name=" Bill Number",unique=True)
    user=models.OneToOneField(User,verbose_name="User",on_delete=models.CASCADE,unique=True)
    class Meta:
        db_table = 'bill_number'
        verbose_name = 'bill_number'
        verbose_name_plural = 'bill_numbers'

    def __str__(self) -> str:
        return self.bill_number 
    
class BillID(models.Model):
    
    bill_id=models.CharField(max_length=50,verbose_name="Bill Id",unique=True)
    
    class Meta:
        db_table = 'bill_id'
        verbose_name = 'bill_id'
        verbose_name_plural = 'bill_id'

    def __str__(self) -> str:
        return self.bill_id

class SilverBillNumber(models.Model):
    
    silver_bill_number=models.CharField(max_length=10,verbose_name="Silver Bill Number",unique=True)
    user=models.OneToOneField(User,verbose_name="User",on_delete=models.CASCADE,unique=True)
    class Meta:
        db_table = 'silver_bill_number'
        verbose_name = 'silver_bill_number'
        verbose_name_plural = 'silver_bill_numbers'

    def __str__(self) -> str:
        return self.silver_bill_number 
    
class SilverBillID(models.Model):
    
    silver_bill_id=models.CharField(max_length=10,verbose_name="Silver Bill Id",unique=True)
    
    class Meta:
        db_table = 'silver_bill_id'
        verbose_name = 'silver_bill_id'
        verbose_name_plural = 'silver_bill_id'

    def __str__(self) -> str:
        return self.silver_bill_id
    
class GoldEstimationNumber(models.Model):
    
    gold_estimation_number=models.CharField(max_length=10,verbose_name="Gold Estimation Number",unique=True)
    user=models.OneToOneField(User,verbose_name="User",on_delete=models.CASCADE,unique=True)
    class Meta:
        db_table = 'gold_estimation_number'
        verbose_name = 'gold_estimation_number'
        verbose_name_plural = 'gold_estimation_numbers'

    def __str__(self) -> str:
        return self.gold_estimation_number 
    
class GoldEstimationID(models.Model):
    
    gold_estimation_id=models.CharField(max_length=10,verbose_name="Gold Estimation Id",unique=True)
    
    class Meta:
        db_table = 'gold_estimation_id'
        verbose_name = 'gold_estimation_id'
        verbose_name_plural = 'gold_estimation_id'

    def __str__(self) -> str:
        return self.gold_estimation_id
    
class SilverEstimationNumber(models.Model):
    
    silver_estimation_number=models.CharField(max_length=10,verbose_name="Silver Estimation Number",unique=True)
    user=models.OneToOneField(User,verbose_name="User",on_delete=models.CASCADE,unique=True)
    class Meta:
        db_table = 'silver_estimation_number'
        verbose_name = 'silver_estimation_number'
        verbose_name_plural = 'silver_estimation_numbers'

    def __str__(self) -> str:
        return self.silver_estimation_number 
    
class SilverEstimationID(models.Model):
    
    silver_estimation_id=models.CharField(max_length=10,verbose_name="Silver Estimation Id",unique=True)
    
    class Meta:
        db_table = 'silver_estimation_id'
        verbose_name = 'silver_estimation_id'
        verbose_name_plural = 'silver_estimation_id'

    def __str__(self) -> str:
        return self.silver_estimation_id
    
class MiscIssueId(models.Model):

    misc_issue_id = models.CharField(verbose_name="Misc Id", max_length=100, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', related_name='misc_issue_id_created_by', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'billing_misc_issue_id'
        verbose_name = 'billing_misc_issue_id'
        verbose_name_plural = 'billing_misc_issue_ids'

    def __str__(self) -> str:
        return self.misc_issue_id
    
class SessionMiscIssueId(models.Model):

    ses_misc_issue_id = models.OneToOneField(MiscIssueId, verbose_name='Misc Id', on_delete=models.CASCADE)
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'billing_session_misc_issue_id'
        verbose_name = 'billing_session_misc_issue_id'
        verbose_name_plural = 'billing_session_misc_issue_ids'

    def __str__(self) -> str:
        return self.ses_misc_issue_id
    
class MiscIssueDetails(models.Model):

    misc_issue_id = models.OneToOneField(MiscIssueId, verbose_name='Misc Id', on_delete=models.CASCADE)
    issue_date = models.DateField(verbose_name='Issue Date')
    branch = models.ForeignKey(Branch, verbose_name='Branch', on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, verbose_name='Customer', on_delete=models.PROTECT)
    giver_name = models.CharField(verbose_name="Giver Name", max_length=100, null=True, blank=True)
    remarks = models.CharField(verbose_name="Remarks", max_length=500, null=True, blank=True)
    total_gross_weight = models.FloatField(verbose_name='Total Gross Weight', default=0.0)
    total_net_weight = models.FloatField(verbose_name='Total Net Weight', default=0.0)
    total_pieces = models.IntegerField(verbose_name='Total Pieces', default=0)
    total_amount = models.FloatField(verbose_name='Total Amount', default=0.0)
    bill_amount = models.FloatField(verbose_name='Bill Amount', default=0.0)
    net_amount = models.FloatField(verbose_name='Net Amount', default=0.0)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', related_name='misc_issue_details_created_by', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'billing_misc_issue_detail'
        verbose_name = 'billing_misc_issue_detail'
        verbose_name_plural = 'billing_misc_issue_details'

    def __str__(self) -> str:
        return self.misc_issue_id.misc_issue_id
    
class MiscParticulars(models.Model):

    misc_issue_details = models.ForeignKey(MiscIssueDetails, verbose_name='Misc Issue', on_delete=models.CASCADE)
    tag_number = models.ForeignKey(TaggedItems, verbose_name='Tag Number', on_delete=models.PROTECT)
    pieces = models.IntegerField(verbose_name='Pieces', default=0)
    metal_rate = models.FloatField(verbose_name='Metal Rate', default=0.0)
    amount = models.FloatField(verbose_name='Amount', default=0.0)

    class Meta:
        db_table = 'billing_misc_particular'
        verbose_name = 'billing_misc_particular'
        verbose_name_plural = 'billing_misc_particulars'

    def __str__(self) -> str:
        return self.misc_issue_details.misc_issue_id.misc_issue_id