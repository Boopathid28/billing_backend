from django.db import models
from masters.models import *
from product.models import *
from accounts.models import *
# Create your models here.

class FlatWastageType(models.Model):
    type_name=models.CharField(max_length=50,verbose_name="Type Name",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'flatwastage_type'
        verbose_name = 'flatwastage_type'
        verbose_name_plural = 'flatwastage_type'

    def __str__(self) -> str:
        return self.type_name

class ValueAdditionCustomer(models.Model):
    metal=models.ForeignKey(Metal,verbose_name="Metal",on_delete=models.PROTECT)
    stock_type=models.ForeignKey(StockType,verbose_name="Stock Type",on_delete=models.PROTECT)
    tag_type=models.ForeignKey(TagTypes,verbose_name="Tag Type",on_delete=models.PROTECT)
    item_details=models.ForeignKey(Item,verbose_name="Item Details",on_delete=models.PROTECT,null=True)
    sub_item_details=models.ForeignKey(SubItem,verbose_name="Sub Item Details",on_delete=models.PROTECT)
    calculation_type=models.ForeignKey(CalculationType,verbose_name="Calculation Type",on_delete=models.PROTECT)
    from_weight=models.FloatField(max_length=50,verbose_name="From Weight")
    to_weight=models.FloatField(max_length=50,verbose_name="To Weight")
    max_fixed_rate=models.FloatField(max_length=50,verbose_name="Fixed Rate",null=True,blank=True,default=0.0)
    max_wastage_percent=models.FloatField(max_length=50,verbose_name="Maximum Wastage Percent",null=True,blank=True,default=0.0)
    max_flat_wastage=models.FloatField(max_length=50,verbose_name="Maximum Flat Wastage",null=True,blank=True,default=0.0)
    max_making_charge_gram=models.FloatField(max_length=50,verbose_name="Maximum Making Charge Gram",null=True,blank=True,default=0.0)
    max_flat_making_charge=models.FloatField(max_length=50,verbose_name="Maximum Flat Making Charge",null=True,blank=True,default=0.0)
    max_per_gram_rate=models.FloatField(max_length=50,verbose_name="Maximum Per Gram Rate",null=True,blank=True,default=0.0)
    min_per_piece_rate = models.FloatField(verbose_name="Min Per Piece Rate",default=0.0)
    per_piece_rate = models.FloatField(verbose_name="Per Piece Rate",default=0.0)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'value_addition_customer'
        verbose_name = 'value_addition_customer'
        verbose_name_plural = 'value_addition_customers'

    def __str__(self) -> str:
        return self.modified_by   
    

class ValueAdditionDesigner(models.Model):
    
    designer_name = models.ForeignKey(AccountHeadDetails,verbose_name="Designer Name",on_delete=models.CASCADE,null=True,blank=True)
    metal_name=models.ForeignKey(Metal,verbose_name="Metal",on_delete=models.CASCADE)
    item_name=models.ForeignKey(Item,verbose_name="Item Details",on_delete=models.CASCADE)
    sub_item_name=models.ForeignKey(SubItem,verbose_name="Sub Item Details",on_delete=models.CASCADE)
    tag_type=models.ForeignKey(TagTypes,verbose_name="Tag Type",on_delete=models.CASCADE,null=True,blank=True)
    calculation_type=models.ForeignKey(CalculationType,verbose_name="Calculation Type",on_delete=models.PROTECT,null=True)
    purchase_fixed_rate=models.FloatField(max_length=50,verbose_name="Purchase Fixed Rate",null=True,blank=True,default=0.0)
    purchase_pergram_rate=models.FloatField(max_length=50,verbose_name="Purchase Per Gram Rate",null=True,blank=True,default=0.0)
    purchase_pergram_weight_type=models.ForeignKey(WeightType,verbose_name="Purchase Pergram Weight Type",related_name='pergram_weight_type',null=True,blank=True,on_delete=models.PROTECT)
    purchase_perpiece_rate=models.FloatField(max_length=50,verbose_name="Purchase Perpiece Rate",null=True,blank=True,default=0.0)
    purchase_touch=models.FloatField(max_length=50,verbose_name="Purchase Touch",null=True,blank=True,default=0.0)
    purchase_wastage_calculation_type=models.ForeignKey(WeightType,verbose_name="Purchase Wastage Calculation Type",related_name='wastage_calculation_type',null=True,blank=True,on_delete=models.PROTECT)
    purchase_wastage_percent=models.FloatField(max_length=50,verbose_name="Purchase Wastage Percent",null=True,blank=True,default=0.0)
    purchase_flat_wastage=models.FloatField(max_length=50,verbose_name="Purchase Flat Wastage",null=True,blank=True,default=0.0)
    purchase_making_charge_calculation_type=models.ForeignKey(WeightType,verbose_name="Purchase Making Charge Calculation Type",related_name='making_charge_calculation_type',null=True,blank=True,on_delete=models.PROTECT)
    purchase_making_charge_gram=models.FloatField(max_length=50,verbose_name="Purchase Making Charge Gram",null=True,blank=True,default=0.0)
    purchase_flat_making_charge=models.FloatField(max_length=50,verbose_name="Purchase Flat Making Charge",null=True,blank=True,default=0.0)
    retail_touch=models.FloatField(max_length=50,verbose_name="retail Touch",null=True,blank=True,default=0.0)
    retail_wastage_percent=models.FloatField(max_length=50,verbose_name="retail Wastage Percent",null=True,blank=True,default=0.0)
    retail_flat_wastage=models.FloatField(max_length=50,verbose_name="retail Flat Wastage",null=True,blank=True,default=0.0)
    retail_making_charge_gram=models.FloatField(max_length=50,verbose_name="retail Making Charge Gram",null=True,blank=True,default=0.0)
    retail_flat_making_charge=models.FloatField(max_length=50,verbose_name="retail Flat Making Charge",null=True,blank=True,default=0.0)
    vip_touch=models.FloatField(max_length=50,verbose_name="vip Touch",null=True,blank=True,default=0.0)
    vip_wastage_percent=models.FloatField(max_length=50,verbose_name="vip Wastage Percent",null=True,blank=True,default=0.0)
    vip_flat_wastage=models.FloatField(max_length=50,verbose_name="vip Flat Wastage",null=True,blank=True,default=0.0)
    vip_making_charge_gram=models.FloatField(max_length=50,verbose_name="vip Making Charge Gram",null=True,blank=True,default=0.0)
    vip_flat_making_charge=models.FloatField(max_length=50,verbose_name="vip Flat Making Charge",null=True,blank=True,default=0.0)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'value_addition_designer'
        verbose_name = 'value_addition_designer'
        verbose_name_plural = 'value_addition_designers'

    def __str__(self) -> str:
        return self.modified_by 


