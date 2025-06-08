from django.db import models
from customer.models import Customer
from accounts.models import *
from settings.models import StatusTable
from tagging.models import TaggedItems,StoneWeightType,RateType
from masters.models import TaxDetails,Metal,Purity,StoneDetails
from product.models import Item,SubItem,CalculationType,WeightType,StockType
from billing.models import BillingType

# Create your models here.

class BillingBackupDetails(models.Model):

    bill_no=models.CharField(max_length=20,verbose_name="Bill Number",unique=True,null=True,blank=True)
    bill_type=models.ForeignKey(BillingType,verbose_name="Bill Type",on_delete=models.PROTECT,null=True,blank=True)
    bill_date=models.DateTimeField(verbose_name="Bill Date",null=True,blank=True)
    customer_details=models.ForeignKey(Customer,verbose_name="Customer Details",on_delete=models.PROTECT)
    customer_mobile=models.CharField(max_length=10,verbose_name="Customer Mobile",null=True)
    total_amount=models.FloatField(max_length=50,verbose_name="Total Amount",default=0.0)
    gst_amount=models.FloatField(max_length=50,verbose_name="GST Amount",default=0.0)
    advance_amount=models.FloatField(max_length=50,verbose_name="Advance Amount",default=0.0)
    discount_amount=models.FloatField(max_length=50,verbose_name="Discount Amount",default=0.0)
    exchange_amount=models.FloatField(max_length=50,verbose_name="Exchange Amount",default=0.0)
    chit_amount=models.FloatField(max_length=50,verbose_name="Chit Amount",default=0.0)
    payable_amount=models.FloatField(max_length=50,verbose_name="Payable Amount",default=0.0)
    cash_amount=models.FloatField(max_length=50,verbose_name="Cash amount",default=0.0)
    card_amount=models.FloatField(max_length=50,verbose_name="Card amount",default=0.0)
    account_transfer_amount=models.FloatField(max_length=50,verbose_name="Account transfer amount",default=0.0)
    upi_amount=models.FloatField(max_length=50,verbose_name="UPI amount",default=0.0)
    paid_amount=models.FloatField(max_length=50,verbose_name="Paid Amount",default=0.0)
    branch = models.ForeignKey(Branch,verbose_name="Branch",null=True,blank=True,on_delete=models.PROTECT)
    created_by=models.ForeignKey(User,verbose_name="Created By",related_name="billingbackup_created_by",on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(verbose_name="Created At",null=True,blank=True)
    modified_by=models.ForeignKey(User,verbose_name="Modified By",related_name="billingbackup_modified_by",on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at=models.DateTimeField(verbose_name="Modified At",null=True,blank=True)

    class Meta:
        db_table = 'billing_backup_detail'
        verbose_name = 'billing_backup_detail'
        verbose_name_plural = 'billing_backup_details'

    def __str__(self) -> str:
        return f"{self.bill_no}"
    
class BillingBackupTagItems(models.Model):

    billing_details=models.ForeignKey(BillingBackupDetails,verbose_name="Billing Details",on_delete=models.CASCADE)
    billing_tag_item=models.ForeignKey(TaggedItems,verbose_name="Billing Tag Items",on_delete=models.DO_NOTHING)
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
    huid_rate=models.FloatField(max_length=50,verbose_name="Huid Rate",null=True,blank=True,default=0.0)
    flat_making_charge=models.FloatField(max_length=50,verbose_name="Flat Making Charger",null=True,blank=True,default=0.0)
    stock_type=models.ForeignKey(StockType,verbose_name="Stock Type",on_delete=models.PROTECT,default=1)
    calculation_type=models.ForeignKey(CalculationType,verbose_name="Calculation Type",on_delete=models.PROTECT,default=1)
    making_charge_calculation_type=models.ForeignKey(WeightType,verbose_name="Making Charge Calculation Type",related_name="billingbackup_making_charge_calculation",on_delete=models.PROTECT,null=True,blank=True,default=0.0)
    tax_percent=models.FloatField(max_length=50,verbose_name="Tax Percent",null=True,blank=True,default=0.0)
    additional_charges=models.FloatField(max_length=50,verbose_name="Additional Charges",null=True,blank=True,default=0.0)
    per_gram_weight_type=models.ForeignKey(WeightType,verbose_name="Per gram weight type",related_name="billingbackup_per_gram_weight_type",on_delete=models.PROTECT,null=True,blank=True,default=0.0)
    total_stone_weight=models.FloatField(max_length=50,verbose_name="Total Stone Weight",null=True,blank=True,default=0.0)
    wastage_calculation_type=models.ForeignKey(WeightType,verbose_name="Wastage Calculation Type",related_name="billingbackup_Wastage_calculation",on_delete=models.PROTECT,null=True,blank=True,default=0.0)
    total_diamond_weight=models.FloatField(max_length=50,verbose_name="Tax Diamond Weight",null=True,blank=True,default=0.0)
    gst=models.FloatField(max_length=50,verbose_name="GST",null=True,blank=True,default=0.0)
    total_rate=models.FloatField(max_length=50,verbose_name="Total Rate",null=True,blank=True,default=0.0)
    without_gst_rate=models.FloatField(max_length=50,verbose_name="Without Gst Rate",null=True,blank=True,default=0.0)
    
    class Meta:
        db_table = 'billing_backup_tagitem'
        verbose_name = 'billing_backup_tagitem'
        verbose_name_plural = 'billing_backup_tagitems'

    def __str__(self) -> str:
        return f"{self.billing_details}"
    
class BillingBackupStoneDetails(models.Model):
    billing_details=models.ForeignKey(BillingBackupDetails,verbose_name="Billing Details",on_delete=models.CASCADE)
    billing_item_details=models.ForeignKey(BillingBackupTagItems,verbose_name="Billing Item Details",on_delete=models.CASCADE)
    stone_name=models.ForeignKey(StoneDetails,verbose_name="Stone Name",on_delete=models.PROTECT)
    stone_pieces=models.IntegerField(verbose_name="Stone Pieces",null=True,blank=True)
    stone_weight=models.FloatField(max_length=50,verbose_name="Stone Weight",null=True,blank=True)
    stone_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    stone_rate=models.FloatField(max_length=50,verbose_name="Stone Rate",null=True,blank=True)
    stone_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    include_stone_weight=models.BooleanField(verbose_name="Include Stone Weight",default=True)
    total_stone_value=models.FloatField(max_length=50,verbose_name="Total Stone Value",null=True,blank=True)

    class Meta:
        db_table = 'billing_backup_stone_detail'
        verbose_name = 'billing_backup_stone_detail'
        verbose_name_plural = 'billing_backup_stone_details'

    def __str__(self) -> str:
        return f"{self.stone_pieces}"
    
class BillingBackupDiamondDetails(models.Model):
    billing_details=models.ForeignKey(BillingBackupDetails,verbose_name="Billing Details",on_delete=models.CASCADE)
    billing_item_details=models.ForeignKey(BillingBackupTagItems,verbose_name="Billing Item Details",on_delete=models.CASCADE)
    diamond_name=models.ForeignKey(StoneDetails,verbose_name="Diamond Name",on_delete=models.PROTECT)
    diamond_pieces=models.IntegerField(verbose_name="Diamond Pieces",null=True,blank=True)
    diamond_weight=models.FloatField(max_length=50,verbose_name="Diamond Weight",null=True,blank=True)
    diamond_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True)
    diamond_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    include_diamond_weight=models.BooleanField(verbose_name="Include Diamond Weight",default=True)
    total_diamond_value=models.FloatField(max_length=50,verbose_name="Total Diamond Value",null=True,blank=True)

    class Meta:
        db_table = 'billing_backup_diamond_detail'
        verbose_name = 'billing_backup_diamond_detail'
        verbose_name_plural = 'billing_backup_diamond_details'

    def __str__(self) -> str:
        return f"{self.diamond_pieces}"
    
class BillingBackupOldGold(models.Model):

    billing_details=models.ForeignKey(BillingBackupDetails,verbose_name="Billing Details",on_delete=models.CASCADE,default=1)
    item_name = models.CharField(max_length=150,verbose_name="Item Name",null=True,blank=True)
    old_metal=models.ForeignKey(Metal,verbose_name="Old Metal",on_delete=models.DO_NOTHING)
    old_gold_no=models.CharField(max_length=100,verbose_name="Oldgold Number",null=True,blank=True)
    metal_rate=models.FloatField(max_length=50,verbose_name="metal Rate",null=True,blank=True,default=0.0)
    today_metal_rate=models.FloatField(max_length=50,verbose_name="Today Metal Rate",null=True,blank=True,default=0.0)
    old_gross_weight=models.FloatField(max_length=50,verbose_name="Old Gross Weight",null=True,blank=True,default=0.0)
    old_net_weight=models.FloatField(max_length=50,verbose_name="Old Net Weight",null=True,blank=True,default=0.0)
    dust_weight = models.FloatField(max_length=50,verbose_name="Dust Weight",null=True,blank=True,default=0.0)
    old_metal_rate=models.FloatField(max_length=50,verbose_name="Old Metal Rate",null=True,blank=True,default=0.0)
    total_old_gold_value=models.FloatField(max_length=100,verbose_name="Total Old Gold Value",null=True,blank=True,default=0.0)
    purity = models.ForeignKey(Purity,verbose_name="oldgold_purity",null=True,blank=True,on_delete = models.PROTECT)
    
    class Meta:
        db_table = 'billing_backup_oldgold_detail'
        verbose_name = 'billing_backup_oldgold_detail'
        verbose_name_plural = 'billing_backup_oldgold_details'

    def __str__(self) -> str:
        return f"{self.old_metal_rate}"

class BackupBillNumber(models.Model):
    
    backupbill_number=models.CharField(max_length=50,verbose_name="Backup Bill Number",unique=True)
    user=models.OneToOneField(User,verbose_name="User",on_delete=models.CASCADE,unique=True)
    class Meta:
        db_table = 'backup_bill_number'
        verbose_name = 'backup_bill_number'
        verbose_name_plural = 'backup_bill_numbers'

    def __str__(self) -> str:
        return self.backupbill_number 

    
class BackupBillID(models.Model):
    
    backupbill_id=models.CharField(max_length=50,verbose_name="Backup Bill Id",unique=True)
    
    class Meta:
        db_table = 'backup_bill_id'
        verbose_name = 'backup_bill_id'
        verbose_name_plural = 'backup_bill_id'

    def __str__(self) -> str:
        return self.backupbill_id
    

class BackupBillSilverNumber(models.Model):
    
    backupbill_number=models.CharField(max_length=50,verbose_name="Backup Bill Number",unique=True)
    user=models.OneToOneField(User,verbose_name="User",on_delete=models.CASCADE,unique=True)
    class Meta:
        db_table = 'backup_bill_silver_number'
        verbose_name = 'backup_bill_silver_number'
        verbose_name_plural = 'backup_bill_silver_numbers'

    def __str__(self) -> str:
        return self.backupbill_number 

    
class BackupBillSilverBillID(models.Model):
    
    backupbill_id=models.CharField(max_length=50,verbose_name="Backup Bill Id",unique=True)
    
    class Meta:
        db_table = 'backup_bill_silver_id'
        verbose_name = 'backup_bill_silver_id'
        verbose_name_plural = 'backup_bill_silver_id'

    def __str__(self) -> str:
        return self.backupbill_id
    
