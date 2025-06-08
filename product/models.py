from django.db import models
from accounts.models import *
from infrastructure.models import Counter
from masters.models import *


# Create your models here.
class StockType(models.Model):
    stock_type_name=models.CharField(max_length=25,verbose_name="Stock Type",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'stock_type'
        verbose_name = 'stock_type'
        verbose_name_plural = 'stock_types'

    def __str__(self) -> str:
        return self.stock_type_name


class CalculationType(models.Model):
    calculation_name=models.CharField(max_length=50,verbose_name="Calculation Name",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)
    class Meta:
        db_table = 'calculation_type'
        verbose_name = 'calculation_type'
        verbose_name_plural = 'calculation_types'

    def __str__(self) -> str:
        return self.calculation_name
    
class Measurement(models.Model):
    measurement_name=models.CharField(max_length=50,verbose_name="Measurement Name",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'measurement_detail'
        verbose_name = 'measurement_detail'
        verbose_name_plural = 'measurement_details'

    def __str__(self) -> str:
        return self.measurement_name
    
class WeightType(models.Model):
    weight_name=models.CharField(max_length=50,verbose_name="Weight Name",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'weight_type'
        verbose_name = 'weight_type'
        verbose_name_plural = 'weight_types'

    def __str__(self) -> str:
        return self.weight_name

class ItemID(models.Model):
    item_id=models.CharField(max_length=10,verbose_name="Item Id",unique=True)

    class Meta:
        db_table = 'item_id'
        verbose_name = 'item_id'
        verbose_name_plural = 'item_ids'

    def __str__(self) -> str:
        return self.item_id

class Item(models.Model):
    metal=models.ForeignKey(Metal,verbose_name="Metal",on_delete=models.PROTECT)
    purity=models.ForeignKey(Purity,verbose_name="Purity",on_delete=models.PROTECT)
    hsn_code=models.CharField(max_length=15,verbose_name="HSN Code")
    stock_type=models.ForeignKey(StockType,verbose_name="Stock Type",on_delete=models.PROTECT)
    item_id=models.CharField(max_length=10,verbose_name="Item ID",unique=True)
    # item_code=models.CharField(max_length=25,verbose_name="Item Code",unique=True)
    item_name=models.CharField(max_length=50,verbose_name="Item Name")
    calculation_type=models.ForeignKey(CalculationType,verbose_name="Calculation Type",on_delete=models.PROTECT)
    item_counter=models.ForeignKey(Counter,verbose_name="Item Counter",on_delete=models.DO_NOTHING)
    allow_zero_weight=models.BooleanField(verbose_name="Allow Zero Weight",default=False)
    item_image=models.CharField(max_length=250,verbose_name="Item Image",null=True,blank=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    huid_rate=models.FloatField(max_length=50,verbose_name="HUID Rate",default=0.0)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'item_detail'
        verbose_name = 'item_detail'
        verbose_name_plural = 'item_details'

    def __str__(self) -> str:
        return self.item_name


class FixedRate(models.Model):
    item_details=models.ForeignKey(Item,verbose_name="Item Details",on_delete=models.CASCADE)
    fixed_rate=models.FloatField(max_length=50,verbose_name="Fixed Rate",null=False,blank=False)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)
    class Meta:
        db_table = 'fixed_rate'
        verbose_name = 'fixed_rate'
        verbose_name_plural = 'fixed_rates'

    
    
class WeightCalculation(models.Model):
    item_details=models.ForeignKey(Item,verbose_name="Item Details",on_delete=models.CASCADE)
    wastage_calculation=models.ForeignKey(WeightType,related_name="item_wastage_calculation",verbose_name="Wastage Calculation",on_delete=models.PROTECT)
    wastage_percent=models.FloatField(max_length=25,verbose_name="item_Wastage Percentage",null=False,blank=False)
    flat_wastage=models.FloatField(max_length=25,verbose_name="Flat Wastage",null=False,blank=False)
    making_charge_calculation=models.ForeignKey(WeightType,related_name="making_charge_calculation",verbose_name="Making Charge Calculation",on_delete=models.PROTECT)
    making_charge_gram=models.FloatField(max_length=25,verbose_name="Making Charge per Gram",null=False,blank=False)
    flat_making_charge=models.FloatField(max_length=25,verbose_name="Flat Making Charge",null=False,blank=False)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)
    class Meta:
        db_table = 'weight_calculation'
        verbose_name = 'weight_calculation'
        verbose_name_plural = 'weight_calculations'

    
    def __str__(self) -> str:
        return self.item_details.item_name
    
class PerGramRate(models.Model):
    item_details=models.ForeignKey(Item,verbose_name="Item Details",on_delete=models.CASCADE)
    per_gram_rate=models.FloatField(max_length=25,verbose_name="Per Gram Rate",null=False,blank=False)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)


    class Meta:
        db_table = 'per_gram_rate'
        verbose_name = 'per_gram_rate'
        verbose_name_plural = 'per_gram_rates'

    
    def __str__(self) -> str:
        return self.item_details.item_name
    
class PerPiece(models.Model):
    item_details=models.ForeignKey(Item,verbose_name="Item Details",on_delete=models.CASCADE)
    min_per_piece_rate = models.FloatField(verbose_name="Min Per Piece Rate",default=0.0,null=False,blank=False)
    per_piece_rate = models.FloatField(verbose_name="Per Piece Rate",default=0.0,null=False,blank=False)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)


    class Meta:
        db_table = 'per_piece'
        verbose_name = 'per_piece'
        verbose_name_plural = 'per_piece'

    
    def __str__(self) -> str:
        return self.item_details.item_name

class MeasurementType(models.Model):
    measurement_name=models.CharField(max_length=50,verbose_name="Measurement Name",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'measurement_type'
        verbose_name = 'measurement_type'
        verbose_name_plural = 'measurement_types'

    def __str__(self) -> str:
        return self.measurement_name
    
class SubItemID(models.Model):
    sub_item_id=models.CharField(max_length=10,verbose_name="Item Id",unique=True)

    class Meta:
        db_table = 'sub_item_id'
        verbose_name = 'sub_item_id'
        verbose_name_plural = 'sub_item_ids'

    def __str__(self) -> str:
        return self.sub_item_id

class SubItem(models.Model):
    metal=models.ForeignKey(Metal,verbose_name="Metal",on_delete=models.PROTECT)
    purity=models.ForeignKey(Purity,verbose_name="Purity",on_delete=models.PROTECT)
    item_details=models.ForeignKey(Item,verbose_name="Item Details",on_delete=models.PROTECT)
    stock_type=models.ForeignKey(StockType,verbose_name="Stock Type",on_delete=models.PROTECT)
    sub_item_id=models.CharField(max_length=10,verbose_name="Sub Item ID",unique=True)
    subitem_hsn_code=models.CharField(max_length=15,verbose_name="HSN Code")
    # sub_item_code=models.CharField(max_length=25,verbose_name="Sub Item Code",unique=True)
    sub_item_name=models.CharField(max_length=50,verbose_name="Sub Item Name")
    allow_zero_weight=models.BooleanField(verbose_name="Allow Zero Weight",default=False)
    sub_item_counter=models.ForeignKey(Counter,verbose_name="Item Counter",on_delete=models.DO_NOTHING)
    calculation_type=models.ForeignKey(CalculationType,verbose_name="Calculation Type",on_delete=models.PROTECT)
    sub_item_image=models.CharField(max_length=250,verbose_name="Item Image",null=True,blank=True)
    measurement_type=models.ForeignKey(MeasurementType,verbose_name="Measurement Type",on_delete=models.PROTECT)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'sub_item_detail'
        verbose_name = 'sub_item_detail'
        verbose_name_plural = 'sub_item_details'

    def __str__(self) -> str:
        return self.sub_item_name
    

class SubItemFixedRate(models.Model):
    sub_item_details=models.ForeignKey(SubItem,verbose_name="SubItem Details",on_delete=models.CASCADE)
    fixed_rate=models.FloatField(max_length=50,verbose_name="Fixed Rate")
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)
    class Meta:
        db_table = 'subitem_fixed_rate'
        verbose_name = 'subitem_fixed_rate'
        verbose_name_plural = 'subitem_fixed_rates'


class SubItemWeightCalculation(models.Model):
    sub_item_details=models.ForeignKey(SubItem,verbose_name="SubItem Details",on_delete=models.CASCADE)
    wastage_calculation=models.ForeignKey(WeightType,related_name="subitem_wastage_calculation",verbose_name="Wastage Calculation",on_delete=models.PROTECT)
    wastage_percent=models.FloatField(max_length=25,verbose_name="Wastage Percentage")
    flat_wastage=models.FloatField(max_length=25,verbose_name="Flat Wastage")
    making_charge_calculation=models.ForeignKey(WeightType,related_name="subitem_making_charge_calculation",verbose_name="Making Charge Calculation",on_delete=models.PROTECT)
    making_charge_gram=models.FloatField(max_length=25,verbose_name="Making Charge per Gram")
    flat_making_charge=models.FloatField(max_length=25,verbose_name="Flat Making Charge")
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)
    class Meta:
        db_table = 'subitem_weight_calculation'
        verbose_name = 'subitem_weight_calculation'
        verbose_name_plural = 'subitem_weight_calculations'


class SubItemPerGramRate(models.Model):
    sub_item_details=models.ForeignKey(SubItem,verbose_name="SubItem Details",on_delete=models.CASCADE)
    per_gram_rate=models.FloatField(max_length=25,verbose_name="Per Gram Rate",null=False,blank=False)
    per_gram_weight_type=models.ForeignKey(WeightType,verbose_name="Weight Type",null=True,blank=True,on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)


    class Meta:
        db_table = 'sub_per_gram_rate'
        verbose_name = 'sub_per_gram_rate'
        verbose_name_plural = 'sub_per_gram_rates'

    
    def __str__(self) -> str:
        return self.sub_item_details.sub_item_name
    
class SubItemPerPiece(models.Model):
    item_details=models.ForeignKey(SubItem,verbose_name="SubItem Details",on_delete=models.CASCADE)
    min_per_piece_rate = models.FloatField(verbose_name="Min Per Piece Rate",default=0.0,null=False,blank=False)
    per_piece_rate = models.FloatField(verbose_name="Per Piece Rate",default=0.0,null=False,blank=False)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)


    class Meta:
        db_table = 'sub_per_piece'
        verbose_name = 'sub_per_piece'
        verbose_name_plural = 'sub_per_piece'


class RangeStock(models.Model):
    # item_details = models.ForeignKey(Item,verbose_name="Itam Details",on_delete=models.PROTECT)
    from_weight=models.FloatField(max_length=50,verbose_name="From Weight")
    to_weight=models.FloatField(max_length=50,verbose_name="To Weight")
    range_value=models.CharField(max_length=50,verbose_name="Range Values")
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)


    class Meta:
        db_table = 'range_stock'
        verbose_name = 'range_stock'
        verbose_name_plural = 'range_stocks'

    def __str__(self) -> str:
        return self.from_weight






    


