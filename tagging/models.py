from django.db import models
from books.models import AccountHeadDetails
from product.models import Item,SubItem
from masters.models import *
from product.models import CalculationType
from infrastructure.models import Counter
from settings.models import StatusTable
from product.models import  WeightType
from accounts.models import *
from django.conf import settings

# Create your models here.
class StoneWeightType(models.Model):
    weight_name=models.CharField(max_length=50,verbose_name="Weight Name",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'stone_weight_type'
        verbose_name = 'stone_weight_type'
        verbose_name_plural = 'stone_weight_types'
 
    def __str__(self) -> str:
        return self.weight_name

class EntryType(models.Model):
    entry_name=models.CharField(max_length=50,verbose_name="Entry Name",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'entry_type'
        verbose_name = 'entry_type'
        verbose_name_plural = 'entry_types'
 
    def __str__(self) -> str:
        return self.entry_name

class RateType(models.Model):
    type_name=models.CharField(max_length=50,verbose_name="Entry Name",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)
 
    class Meta:
        db_table = 'rate_type'
        verbose_name = 'rate_type'
        verbose_name_plural = 'rate_type'
 
    def __str__(self) -> str:
        return self.type_name
    
class LotID(models.Model):
    lot_number=models.CharField(max_length=10,verbose_name="Lot Number",unique=True)

    class Meta:
        db_table = 'lot_id'
        verbose_name = 'lot_id'
        verbose_name_plural = 'lot_ids'

    def __str__(self) -> str:
        return self.lot_number 
    

class Lot(models.Model): 
    lot_number=models.CharField(max_length=10,verbose_name="Lot Number",unique=True,null=False,blank=False)
    entry_date=models.DateField(verbose_name="Lot Entry Date", null=False,blank=False)
    entry_type=models.ForeignKey(EntryType,verbose_name="Entry Type",on_delete=models.DO_NOTHING)
    designer_name=models.ForeignKey(AccountHeadDetails,verbose_name="Designer Name",on_delete=models.PROTECT)
    invoice_number=models.CharField(max_length=50,verbose_name="Refference Invoice Number",unique=True,null=True,blank=True)
    total_pieces=models.IntegerField(verbose_name="Total Pieces",null=True,blank=True)
    total_tag_count=models.IntegerField(verbose_name="Total Tag Count",null=True,blank=True)
    total_grossweight=models.FloatField(max_length=50,verbose_name="Total Gross Weight",null=True,blank=True)
    total_netweight=models.FloatField(max_length=50,verbose_name="Total Net Weight",null=True,blank=True)
    total_stone_pieces=models.IntegerField(verbose_name="Total Stone Pieces",null=True,blank=True)
    total_stone_weight=models.FloatField(max_length=100,verbose_name="Total Stone Weight",null=True,blank=True)
    total_stone_rate=models.FloatField(max_length=100,verbose_name="Total Stone Rate",null=True,blank=True)
    total_diamond_pieces=models.IntegerField(verbose_name="Total Diamond",null=True,blank=True)
    total_diamond_weight=models.FloatField(max_length=100,verbose_name="Total Diamond Weight",null=True,blank=True)
    total_diamond_rate=models.FloatField(max_length=100,verbose_name="Total Diamond Rate",null=True,blank=True)
    tagged_grossweight=models.FloatField(max_length=50,verbose_name="Tagged Gross Weight",null=True,blank=True,default=0.0)
    tagged_netweight=models.FloatField(max_length=50,verbose_name="Tagged Net Weight",null=True,blank=True,default=0.0)
    tagged_pieces=models.IntegerField(verbose_name="Tagged Pieces",null=True,blank=True,default=0)
    tagged_stone_pieces=models.IntegerField(verbose_name="Tagged Stone Pieces",null=True,blank=True,default=0)
    tagged_stone_weight=models.FloatField(max_length=50,verbose_name="Tagged Stone Weight",null=True,blank=True,default=0.0)
    tagged_diamond_pieces=models.IntegerField(verbose_name="Tagged Diamond Pieces",null=True,blank=True,default=0)
    tagged_diamond_weight=models.FloatField(max_length=50,verbose_name="Tagged Diamond Weight",null=True,blank=True,default=0.0)
    tagged_tag_count=models.IntegerField(verbose_name="Tagged Tag Count",null=True,blank=True,default=0.0)
    hallmark_number=models.CharField(max_length=100,verbose_name="Hallmark Number",null=True,blank=True)
    hallmark_center=models.CharField(max_length=100,verbose_name="Hallmark Center",null=True,blank=True)
    tag_status=models.ForeignKey(StatusTable,verbose_name="Tag Status",on_delete=models.PROTECT,default=settings.PENDING)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)
    branch = models.ForeignKey(Branch,related_name="tagged_branch",on_delete=models.DO_NOTHING,null=True,blank=True,default=1)


    class Meta:
        db_table = 'lot'
        verbose_name = 'lot'
        verbose_name_plural = 'lots'

    def __str__(self) -> str:
        return  self.lot_number 


class LotItem(models.Model):
    lot_details=models.ForeignKey(Lot,verbose_name="LOT Details",on_delete=models.CASCADE)
    item_details=models.ForeignKey(Item,verbose_name="Item Details",on_delete=models.PROTECT)
    subitem_details=models.ForeignKey(SubItem,verbose_name="Sub Item Details",on_delete=models.PROTECT,blank=True,null=True)
    bulk_tag=models.BooleanField(verbose_name="Bulk Tag",default=False)
    tag_type=models.ForeignKey(TagTypes,verbose_name="Tag Type",on_delete=models.PROTECT)
    pieces=models.IntegerField(verbose_name="Pieces",null=False,blank=False)
    tag_count=models.IntegerField(verbose_name="Tag Count",null=False,blank=False)
    gross_weight=models.FloatField(max_length=50,verbose_name="Gross Weight",null=False,blank=False)
    net_weight=models.FloatField(max_length=50,verbose_name="Net Weight",null=False,blank=False)
    tag_weight=models.FloatField(max_length=50,verbose_name="Tag Weight",null=False,blank=False)
    cover_weight=models.FloatField(max_length=50,verbose_name="Cover Weight",null=False,blank=False)
    loop_weight=models.FloatField(max_length=50,verbose_name="Loop Weight",null=False,blank=False)
    other_weight=models.FloatField(max_length=50,verbose_name="Other Weight",null=False,blank=False)
    tagged_grossweight=models.FloatField(max_length=50,verbose_name="Tagged Gross Weight",null=True,blank=True,default=0.0)
    tagged_netweight=models.FloatField(max_length=50,verbose_name="Tagged Net Weight",null=True,blank=True,default=0.0)
    tagged_pieces=models.IntegerField(verbose_name="Tagged Pieces",null=True,blank=True,default=0.0)
    tagged_tag_count=models.IntegerField(verbose_name="Tagged Tag Count",null=True,blank=True,default=0.0)
    item_stone_pieces=models.IntegerField(verbose_name="Item Stone Pieces",null=True,blank=True)
    item_stone_weight=models.FloatField(max_length=50,verbose_name="Item Stone Weight",null=True,blank=True)
    item_diamond_pieces=models.IntegerField(verbose_name="Item Diamond Pieces",null=True,blank=True)
    item_diamond_weight=models.FloatField(max_length=50,verbose_name="Item Diamond Weight",null=True,blank=True)
    remark=models.CharField(max_length=100,verbose_name="Remarks",null=True,blank=True)
    
    class Meta:
        db_table = 'lot_item'
        verbose_name = 'lot_item'
        verbose_name_plural = 'lot_items'

    def __str__(self) -> str:
        return f"Lot {self.lot_details}" 
    
class LotItemStone(models.Model):
    lot_details=models.ForeignKey(Lot,verbose_name="LOT Details",on_delete=models.CASCADE)
    lot_item=models.ForeignKey(LotItem,verbose_name="Lot Item Details",on_delete=models.CASCADE)
    stone_name=models.ForeignKey(StoneDetails,verbose_name="Stone Name",on_delete=models.PROTECT)
    stone_pieces=models.IntegerField(verbose_name="Stone Pieces",null=True,blank=True)
    stone_weight=models.FloatField(max_length=50,verbose_name="Stone Weight",null=True,blank=True)
    stone_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    stone_rate=models.FloatField(max_length=50,verbose_name="Stone Rate",null=True,blank=True)
    stone_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    total_stone_value=models.FloatField(max_length=50,verbose_name="Total Stone Value",null=True,blank=True)
    tagged_stone_weight=models.FloatField(max_length=50,verbose_name="Tagged Stone Weight",null=True,blank=True,default=0.0)
    tagged_stone_pieces=models.IntegerField(verbose_name="Tagged Stone Pieces",null=True,blank=True,default=0.0)
    include_stone_weight=models.BooleanField(verbose_name="Include Stone Weight",default=True)

    class Meta:
        db_table = 'lot_item_stone'
        verbose_name = 'lot_item_stone'
        verbose_name_plural = 'lot_item_stones'

    def __str__(self) -> str:
        return self.stone_name.stone_name
    

class LotItemDiamond(models.Model):
    lot_details=models.ForeignKey(Lot,verbose_name="LOT Details",on_delete=models.CASCADE)
    lot_item=models.ForeignKey(LotItem,verbose_name="Lot Item Details",on_delete=models.CASCADE)
    diamond_name=models.ForeignKey(StoneDetails,verbose_name="Diamond Name",on_delete=models.PROTECT)
    diamond_pieces=models.IntegerField(verbose_name="Diamond Pieces",null=True,blank=True)
    diamond_weight=models.FloatField(max_length=50,verbose_name="Diamond Weight",null=True,blank=True)
    diamond_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True)
    diamond_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    total_diamond_value=models.FloatField(max_length=50,verbose_name="Total Diamond Value",null=True,blank=True)
    tagged_diamond_weight=models.FloatField(max_length=50,verbose_name="Tagged Diamond Weight",null=True,blank=True,default=0.0)
    tagged_diamond_pieces=models.IntegerField(verbose_name="Tagged Diamond Pieces",null=True,blank=True,default=0.0)
    include_diamond_weight=models.BooleanField(verbose_name="Include Diamond Weight",default=True)

    class Meta:
        db_table = 'lot_item_diamond'
        verbose_name = 'lot_item_diamond'
        verbose_name_plural = 'lot_item_diamonds'

    def __str__(self) -> str:
        return self.diamond_name.stone_name
    
class TagEntry(models.Model):
    lot_details=models.ForeignKey(Lot,verbose_name="LOT Details",on_delete=models.PROTECT,null=True,blank=True)
    branch = models.ForeignKey(Branch,related_name="tagged_entry_branch",on_delete=models.DO_NOTHING,null=True,blank=True,default=1,db_column='branch')
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'tag_entry'
        verbose_name = 'tag_entry'
        verbose_name_plural = 'tag_entrys'

    def __str__(self) -> str:
        return self.lot_details
    
class TaggedItems(models.Model):
    tag_number=models.CharField(max_length=50,verbose_name="Tag Pieces",unique=True)
    tag_entry_details=models.ForeignKey(TagEntry,verbose_name="Tag Entry Details",on_delete=models.CASCADE)
    item_details=models.ForeignKey(LotItem,verbose_name="Item Details",on_delete=models.PROTECT)
    sub_item_details=models.ForeignKey(SubItem,verbose_name="SubItem Details",on_delete=models.PROTECT)
    size_value=models.CharField(max_length=150,verbose_name="Size",null=True,blank=True)
    tag_type=models.ForeignKey(TagTypes,verbose_name="Tag Type",on_delete=models.PROTECT)
    tag_pieces=models.IntegerField(verbose_name="Tag Pieces")
    tag_count=models.IntegerField(verbose_name="Tag Pieces")
    gross_weight=models.FloatField(max_length=50,verbose_name="Gross Weight")
    net_weight=models.FloatField(max_length=50,verbose_name="Net Weight",null=True,blank=False)
    tag_weight=models.FloatField(max_length=50,verbose_name="Tag Weight")
    cover_weight=models.FloatField(max_length=50,verbose_name="Cover Weight")
    loop_weight=models.FloatField(max_length=50,verbose_name="Loop Weight")
    other_weight=models.FloatField(max_length=50,verbose_name="Other Weight")
    stone_weight=models.FloatField(max_length=50,verbose_name="Stone Weight",null=True,blank=True)
    stone_rate=models.FloatField(max_length=50,verbose_name="Stone Weight",null=True,blank=True)
    stone_pieces=models.IntegerField(verbose_name="Stone Pieces",null=True,blank=True)
    diamond_weight=models.FloatField(max_length=50,verbose_name="Diamond Weight",null=True,blank=True)
    diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True)
    diamond_pieces=models.IntegerField(verbose_name="Diamond Pieces",null=True,blank=True)
    calculation_type=models.ForeignKey(CalculationType,verbose_name="Calculation Type",on_delete=models.PROTECT)
    min_fixed_rate=models.FloatField(max_length=50,verbose_name="Min Wastage Percent",null=True,blank=True,default=0.0)
    max_fixed_rate=models.FloatField(max_length=50,verbose_name="Min Wastage Percent",null=True,blank=True,default=0.0)
    min_wastage_percent=models.FloatField(max_length=50,verbose_name="Max Wastage Percent",null=True,blank=True,default=0.0)
    min_flat_wastage=models.FloatField(max_length=50,verbose_name="Min Flat Wastage",null=True,blank=True,default=0.0)
    max_wastage_percent=models.FloatField(max_length=50,verbose_name="Max Wastage Percent",null=True,blank=True,default=0.0)
    max_flat_wastage=models.FloatField(max_length=50,verbose_name="Max Flat Wastage",null=True,blank=True,default=0.0)
    min_making_charge_gram=models.FloatField(max_length=50,verbose_name="Min Making Charge Per Gram",null=True,blank=True,default=0.0)
    min_flat_making_charge=models.FloatField(max_length=50,verbose_name="Min Flat Making Charge",null=True,blank=True,default=0.0)
    max_making_charge_gram=models.FloatField(max_length=50,verbose_name="Max Making Charge Per Gram",null=True,blank=True,default=0.0)
    max_flat_making_charge=models.FloatField(max_length=50,verbose_name="Max Flat Making Charge",null=True,blank=True,default=0.0)
    per_gram_weight_type=models.ForeignKey(WeightType,verbose_name="Weight Type",null=True,blank=True,on_delete=models.PROTECT)
    min_pergram_rate=models.FloatField(max_length=50,verbose_name="Min Per Gram Rate",null=True,blank=True,default=0.0)
    max_pergram_rate=models.FloatField(max_length=50,verbose_name="Max Per Gram Rate",null=True,blank=True,default=0.0)
    min_per_piece_rate = models.FloatField(verbose_name="Min Per Piece Rate",default=0.0,null=True,blank=True)
    max_per_piece_rate = models.FloatField(verbose_name="Max Per Piece Rate",default=0.0,null=True,blank=True)
    per_piece_rate = models.FloatField(verbose_name="Per Piece Rate",default=0.0,null=True,blank=True)
    rough_sale_value=models.FloatField(max_length=50,verbose_name="Rough Sale Value",null=True,blank=True,default=0.0)
    halmark_huid=models.CharField(max_length=50,verbose_name="Halmark HUID")
    halmark_center=models.CharField(max_length=50,verbose_name="Halmark Center",null=True,blank=True)
    remaining_pieces=models.IntegerField(verbose_name="Remaining pieces",null=True,blank=True)
    remaining_gross_weight=models.FloatField(verbose_name="Remaining Gross Weight",null=True,blank=True)
    remaining_net_weight=models.FloatField(max_length=50,verbose_name="Remaining Net Weight",null=True,blank=True)
    remaining_tag_count=models.FloatField(max_length=50,verbose_name="Remaining Tag Count",null=True,blank=True)
    display_counter=models.ForeignKey(Counter,verbose_name="Display Counter",on_delete=models.PROTECT)
    is_billed=models.BooleanField(verbose_name="Bill Status",default=False)
    transfer=models.BooleanField(verbose_name="Transfer Status",default=0)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)
    branch = models.ForeignKey(Branch,related_name="tagged_items_branch",on_delete=models.DO_NOTHING,null=True,blank=True,default=1,db_column='branch')

    class Meta:
        db_table = 'tagged_item'
        verbose_name = 'tagged_item'
        verbose_name_plural = 'tagged_items'

    def __str__(self) -> str:
        return f"{self.tag_number}"
    
class TaggedItemStone(models.Model):
    tag_details=models.ForeignKey(TaggedItems,verbose_name="Tag Details",on_delete=models.CASCADE)
    tag_entry_details=models.ForeignKey(TagEntry,verbose_name="Tag Entry Details",on_delete=models.CASCADE)
    stone_name=models.ForeignKey(LotItemStone,verbose_name="Stone Name",on_delete=models.PROTECT)
    stone_pieces=models.IntegerField(verbose_name="Stone Pieces",null=True,blank=True)
    stone_weight=models.FloatField(max_length=50,verbose_name="Stone Weight",null=True,blank=True)
    stone_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    stone_rate=models.FloatField(max_length=50,verbose_name="Stone Rate",null=True,blank=True)
    stone_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    total_stone_value=models.FloatField(max_length=50,verbose_name="Total Stone Value",null=True,blank=True)
    include_stone_weight=models.BooleanField(verbose_name="Include Stone Weight",default=True)
    

    class Meta:
        db_table = 'tagged_item_stone'
        verbose_name = 'tagged_item_stone'
        verbose_name_plural = 'tagged_item_stones'

    def __str__(self) -> str:
        return f"{self.stone_pieces}"
    
class TaggedItemDiamond(models.Model):  
    tag_details=models.ForeignKey(TaggedItems,verbose_name="Tag Details",on_delete=models.CASCADE)
    tag_entry_details=models.ForeignKey(TagEntry,verbose_name="Tag Entry Details",on_delete=models.CASCADE)
    diamond_name=models.ForeignKey(LotItemDiamond,verbose_name="Diamond Name",on_delete=models.PROTECT)
    diamond_pieces=models.IntegerField(verbose_name="Diamond Pieces",null=True,blank=True)
    diamond_weight=models.FloatField(max_length=50,verbose_name="Diamond Weight",null=True,blank=True)
    diamond_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True)
    diamond_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    total_diamond_value=models.FloatField(max_length=50,verbose_name="Total Diamond Value",null=True,blank=True)
    include_diamond_weight=models.BooleanField(verbose_name="Include Diamond Weight",default=False)


    class Meta:
        db_table = 'tagged_item_diamond'
        verbose_name = 'tagged_item_diamond'
        verbose_name_plural = 'tagged_item_diamonds'

    def __str__(self) -> str:
        return f"{self.diamond_pieces}"
    
class TagNumber(models.Model):
    tag_number=models.CharField(max_length=50,verbose_name="Tag Number")

    class Meta:
        db_table = 'tag_number'
        verbose_name = 'tag_number'
        verbose_name_plural = 'tag_number'

    def __str__(self) -> str:
        return f"{self.tag_number}"
    
class DuplicateTag(models.Model):
    tag_details=models.ForeignKey(TaggedItems,verbose_name="Tag Details",on_delete=models.CASCADE)
    number_copies=models.IntegerField(verbose_name="Number of Copies")
    created_at=models.DateTimeField(verbose_name="Created at")
    created_by=models.ForeignKey(User,verbose_name="Created By",on_delete=models.SET_DEFAULT,default=1)

    class Meta:
        db_table = 'duplicate_tag'
        verbose_name = 'duplicate_tag'
        verbose_name_plural = 'duplicate_tags'

    def __str__(self) -> str:
        return f"{self.number_copies}"


    
