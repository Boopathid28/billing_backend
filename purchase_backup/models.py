from django.db import models

# Create your models here.
from django.db import models
from accounts.models import *
from billing.admin import EstimateDetailsAdmin
from billing.models import EstimateDetails
from books.models import AccountHeadDetails
from customer.models import Customer
from masters.models import Metal, Purity, StoneDetails
from product.models import Item, SubItem
from settings.models import PaymentMode
from tagging.models import RateType, StoneWeightType

class Purchasepersontype(models.Model):
    purchase_person_name=models.CharField(max_length=55,verbose_name="Purchase person type",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'purchase_person_types'
        verbose_name = 'purchase_person_type'
        verbose_name_plural = 'purchase_person_types'

    def __str__(self) -> str:
        return self.purchase_person_name

# Create your models here.
class PurchaseType(models.Model):
    purchase_type_name=models.CharField(max_length=55,verbose_name="Purchase type",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'purchase_types'
        verbose_name = 'purchase_type'
        verbose_name_plural = 'purchase_types'

    def __str__(self) -> str:
        return self.purchase_type_name
    

class PurchaseEntry(models.Model):
    bill_no = models.CharField(max_length=100,verbose_name="purchase bill number",null=True,blank=True)
    po_id = models.CharField(max_length=100,verbose_name="purchase  number",null=True,blank=True)
    purchase_person_type =models.ForeignKey(Purchasepersontype,related_name="purchase_person",on_delete=models.PROTECT,null=True,blank=True)
    person_id=models.IntegerField(verbose_name="Persong Details")
    branch = models.ForeignKey(Branch,related_name="branch",on_delete=models.PROTECT,null=True,blank=True)
    sgst=models.FloatField(max_length=100,verbose_name="purchase sgst",null=True,blank=True,default=0.0)
    igst=models.FloatField(max_length=100,verbose_name="purchase sgst",null=True,blank=True,default=0.0)
    gst=models.FloatField(max_length=100,verbose_name="purchase gst",null=True,blank=True,default=0.0)
    total_pieces=models.FloatField(max_length=100,verbose_name="total_pieces",null=True,blank=True,default=1)
    total_netweight=models.FloatField(max_length=100,verbose_name="total_weight",null=True,blank=True,default=0.0)
    total_grossweight=models.FloatField(max_length=100,verbose_name="total_grossweight",null=True,blank=True,default=0.0)
    sub_total=models.FloatField(max_length=100,verbose_name="purchase subtotal",null=True,blank=True,default=0.0)
    total_amount=models.FloatField(max_length=100,verbose_name="purchase total amount",null=True,blank=True,default=0.0)
    total_stone_amount=models.FloatField(max_length=100,verbose_name="purchase total stone amount",null=True,blank=True,default=0.0)
    hallmark_amount=models.FloatField(max_length=100,verbose_name="purchase total hallmark amount",null=True,blank=True,default=0.0)
    mc_amount=models.FloatField(max_length=100,verbose_name="purchase total mc amount",null=True,blank=True,default=0.0)
    purchase_date = models.DateField(verbose_name="purchase date",null=True,blank=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'purchase_entry'
        verbose_name = 'purchase_entry'
        verbose_name_plural = 'purchase_entry'

    def __str__(self) -> str:
        return self.estimation_no

class Purchasepayment(models.Model):
    purchaseentry = models.ForeignKey(PurchaseEntry,related_name="purchase_payment_entry",on_delete=models.PROTECT,null=True,blank=True)
    purchase_paymode=models.ForeignKey(PaymentMode,related_name="purchase_payment_mode",on_delete=models.PROTECT,null=True,blank=True)
    paid_amount=models.FloatField(max_length=100,verbose_name="purchase paid amount",null=True,blank=True,default=0.0)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)
    class Meta:
        db_table = 'purchase_payment'
        verbose_name = 'purchase_payment'
        verbose_name_plural = 'purchase_payment'

    def __str__(self) -> str:
        return self.purchase_metal
    
class PurchaseItemDetail(models.Model):
    purchaseentry = models.ForeignKey(PurchaseEntry,related_name="purchase_entry",on_delete=models.PROTECT,null=True,blank=True)
    purchase_metal=models.ForeignKey(Metal,related_name="purchase_metal",on_delete=models.PROTECT,null=True,blank=True)
    purchase_purity = models.ForeignKey(Purity,related_name ="purchase_purity",on_delete = models.PROTECT,null=True,blank=True)
    purchase_item= models.IntegerField(verbose_name ="purchase_item_deatils",null=True,blank=True,default=0)
    purchase_subitem= models.IntegerField(verbose_name ="purchase_sub_tem",null=True,blank=True,default=0)
    pieces=models.CharField(max_length=100,verbose_name="total_pieces",null=True,blank=True)
    stone_pieces=models.CharField(max_length=100,verbose_name="stone_pieces",null=True,blank=True)
    stone_weight=models.FloatField(max_length=100,verbose_name="stone_weight",null=True,blank=True,default=0.0)
    diamond_pieces=models.CharField(max_length=100,verbose_name="diamond_pieces",null=True,blank=True)
    diamond_weight=models.FloatField(max_length=100,verbose_name="diamond_weight",null=True,blank=True,default=0.0)
    gross_weight=models.FloatField(max_length=100,verbose_name="gross_weight",null=True,blank=True,default=0.0)
    less_weight=models.FloatField(max_length=100,verbose_name="less_weight",null=True,blank=True,default=0.0)
    net_weight=models.FloatField(max_length=100,verbose_name="net_weight",null=True,blank=True,default=0.0)
    total_amount=models.FloatField(max_length=100,verbose_name="purchase Item Deatils total amount",null=True,blank=True,default=0.0)
    class Meta:
        db_table = 'purchase_item_detail'
        verbose_name = 'purchase_item_detail'
        verbose_name_plural = 'purchase_item_detail'

    def __str__(self) -> str:
        return self.pieces
    

class PurchaseStoneDetails(models.Model):
    purchaseentry = models.ForeignKey(PurchaseEntry,related_name="purchase_stone_entry",on_delete=models.PROTECT,null=True,blank=True)
    purchase_item=models.ForeignKey(PurchaseItemDetail,related_name="stone_purchase_item",on_delete=models.PROTECT,null=True,blank=True)
    stone_name=models.ForeignKey(StoneDetails,verbose_name="Stone Name",on_delete=models.PROTECT)
    stone_pieces=models.IntegerField(verbose_name="Stone Pieces",null=True,blank=True)
    stone_weight=models.FloatField(max_length=50,verbose_name="Stone Weight",null=True,blank=True)
    stone_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    stone_rate=models.FloatField(max_length=50,verbose_name="Stone Rate",null=True,blank=True)
    stone_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    include_stone_weight=models.BooleanField(verbose_name="Include Stone Weight",default=True)
    total_stone_value=models.FloatField(max_length=50,verbose_name="Total Stone Value",null=True,blank=True)

    class Meta:
        db_table = 'purchase_item_stone'
        verbose_name = 'purchase_item_stone'
        verbose_name_plural = 'purchase_item_stones'

    def __str__(self) -> str:
        return self.stone_pieces
        
class PurchaseDiamondDetails(models.Model):
    purchaseentry = models.ForeignKey(PurchaseEntry,related_name="purchase_diamond_entry",on_delete=models.PROTECT,null=True,blank=True)
    purchase_item=models.ForeignKey(PurchaseItemDetail,related_name="diamond_purchase_item",on_delete=models.PROTECT,null=True,blank=True)
    diamond_name=models.ForeignKey(StoneDetails,verbose_name="Diamond Name",on_delete=models.PROTECT)
    diamond_pieces=models.IntegerField(verbose_name="Diamond Pieces",null=True,blank=True)
    diamond_weight=models.FloatField(max_length=50,verbose_name="Diamond Weight",null=True,blank=True)
    diamond_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Weight Type",on_delete=models.PROTECT)
    diamond_rate=models.FloatField(max_length=50,verbose_name="Diamond Rate",null=True,blank=True)
    diamond_rate_type=models.ForeignKey(RateType,verbose_name="Rate Type",on_delete=models.PROTECT)
    include_diamond_weight=models.BooleanField(verbose_name="Include Diamond Weight",default=True)
    total_diamond_value=models.FloatField(max_length=50,verbose_name="Total Diamond Value",null=True,blank=True)

    class Meta:
        db_table = 'purchase_item_diamond'
        verbose_name = 'purchase_item_diamond'
        verbose_name_plural = 'purchase_item_diamonds'

    def __str__(self) -> str:
        return self.diamond_pieces
    
    
class NewPurchase(models.Model):
    total_pieces = models.IntegerField(verbose_name="pieces",null=True,blank=True,default=0)
    due_date = models.DateField(verbose_name="due_date",null=True,blank=True)
    order_date = models.DateField(verbose_name="order_date",null=True,blank=True)
    total_item = models.IntegerField(verbose_name="pieces",null=True,blank=True,default=0)
    total_net_weight =models.FloatField(max_length=100,verbose_name="net weight",null=True,blank=True,default=0.0)
    total_gross_weight =models.FloatField(max_length=100,verbose_name="gross weight",null=True,blank=True,default=0.0)
    others = models.IntegerField(verbose_name="others",null=True,blank=True,default=0)
    hallmark = models.IntegerField(verbose_name="hallmark",null=True,blank=True,default=0)
    total_amount =models.FloatField(max_length=100,verbose_name="total amount",null=True,blank=True,default=0.0)
    is_billed = models.BooleanField(verbose_name="billed or not", null=True,blank=True,default=False)
    designer_name = models.ForeignKey(AccountHeadDetails,related_name="designer_name",on_delete=models.CASCADE,null=True,blank=True)
    purchase_order_id = models.CharField(max_length=100,verbose_name="purchase order id",null=True,blank=True)
    total_pure_weight = models.FloatField(max_length=100,verbose_name="total pure weight",null=True,blank=True,default=0.0)
    paid_weight =models.FloatField(max_length=100,verbose_name="paid gross weight",null=True,blank=True,default=0.0)
    paid_amount =models.FloatField(max_length=100,verbose_name="paid total amount",null=True,blank=True,default=0.0)
    branch = models.ForeignKey(Branch, related_name="purchase_order_branch", on_delete=models.DO_NOTHING,null=True,blank=True)
    no_of_days = models.IntegerField(verbose_name="no_of_days",null=True,blank=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, related_name="purchase_order_created_by", on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.ForeignKey(User, related_name="purchase_order_modified_by", on_delete=models.DO_NOTHING,null=True,blank=True)


    class Meta:
        db_table = 'newpurchase'
        verbose_name = 'newpurchase'
        verbose_name_plural = 'newpurchase'

    def __str__(self) -> str:
        return self.designer_name.account_head_name
    
class NewPurchaseItemdetail(models.Model):
    purchase_order = models.ForeignKey(NewPurchase,related_name="purchase_order",on_delete=models.CASCADE,null=True,blank=True)
    metal = models.ForeignKey(Metal,related_name="prchaseorder_item_metal_name",on_delete=models.CASCADE,null=True,blank=True)
    item_code  = models.CharField(max_length=100,verbose_name="item_code",null=True,blank=True)
    item = models.ForeignKey(Item,related_name="item",on_delete=models.CASCADE,null=True,blank=True)
    sub_item = models.ForeignKey(SubItem,related_name="sub_item",on_delete=models.CASCADE,null=True,blank=True)
    flat_wastage = models.FloatField(max_length=100,verbose_name="flat wastage",null=True,blank=True,default=0.0)
    wastage = models.FloatField(max_length=100,verbose_name="wastage",null=True,blank=True,default=0.0)
    making_charge_pergram = models.FloatField(max_length=100,verbose_name="making charge",null=True,blank=True,default=0.0)
    flat_makingcharge =models.FloatField(max_length=100,verbose_name="flat making charge",null=True,blank=True,default=0.0)
    pieces = models.IntegerField(verbose_name="pieces",null=True,blank=True,default=0)
    gross_weight =models.FloatField(max_length=100,verbose_name="gross weight",null=True,blank=True,default=0.0)
    less_weight =models.FloatField(max_length=100,verbose_name="less weight",null=True,blank=True,default=0.0)
    net_weight =models.FloatField(max_length=100,verbose_name="net weight",null=True,blank=True,default=0.0)
    touch =models.FloatField(max_length=100,verbose_name="touch",null=True,blank=True,default=0.0)
    pure_weight = models.FloatField(max_length=100,verbose_name="pure weight",null=True,blank=True,default=0.0)
    no_stone_pieces = models.IntegerField(verbose_name="stone  pieces",null=True,blank=True,default=0)
    stone_weight =models.FloatField(max_length=100,verbose_name="stone weight",null=True,blank=True,default=0.0)
    no_diamond_pieces = models.IntegerField(verbose_name=" diamond pieces",null=True,blank=True,default=0)
    diamond_weight =models.FloatField(max_length=100,verbose_name="diamond weight",null=True,blank=True,default=0.0)
    stone_amount =models.FloatField(max_length=100,verbose_name="stone amount",null=True,blank=True,default=0.0)
    total_amount =models.FloatField(max_length=100,verbose_name="total amount",null=True,blank=True,default=0.0)
    diamond_amount=models.FloatField(max_length=100,verbose_name="stone amount",null=True,blank=True,default=0.0)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, related_name="purchase_orderitem_created_by", on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.ForeignKey(User, related_name="purchase_orderitem_modified_by", on_delete=models.DO_NOTHING,null=True,blank=True)

    class Meta:
        db_table = 'newpurchase_item_detail'
        verbose_name = 'newpurchase_item_detail'
        verbose_name_plural = 'newpurchase_item_detail'

    def __str__(self) -> str:
        return self.item_code

class NewPurchaseStoneDetails(models.Model):
    purchase_order = models.ForeignKey(NewPurchase,related_name="new_purchase_order",on_delete=models.CASCADE,null=True,blank=True)
    purchase_item=models.ForeignKey(NewPurchaseItemdetail,related_name="item_purchase_order",on_delete=models.PROTECT,null=True,blank=True)
    stone_name=models.ForeignKey(StoneDetails,verbose_name="Purchase order Stone Name",on_delete=models.PROTECT)
    stone_pieces=models.IntegerField(verbose_name="Purchase order Stone Pieces",null=True,blank=True)
    stone_weight=models.FloatField(max_length=50,verbose_name="Purchase orderStone Weight",null=True,blank=True)
    stone_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Purchase order Weight Type",on_delete=models.PROTECT)
    stone_rate=models.FloatField(max_length=50,verbose_name="Purchase orderStone Rate",null=True,blank=True)
    stone_rate_type=models.ForeignKey(RateType,verbose_name="Purchase orderRate Type",on_delete=models.PROTECT)
    include_stone_weight=models.BooleanField(verbose_name="Purchase order Include Stone Weight",default=True)
    total_stone_value=models.FloatField(max_length=50,verbose_name="Purchase order Total Stone Value",null=True,blank=True)

    class Meta:
        db_table = 'newpurchase_item_stone'
        verbose_name = 'newpurchase_item_stone'
        verbose_name_plural = 'newpurchase_item_stones'

    def __str__(self) -> str:
        return self.stone_pieces
        
class NewPurchaseDiamondDetails(models.Model):
    purchase_order = models.ForeignKey(NewPurchase,related_name="purchase_order_new",on_delete=models.CASCADE,null=True,blank=True)
    purchase_item=models.ForeignKey(NewPurchaseItemdetail,related_name="purchase_order_item",on_delete=models.PROTECT,null=True,blank=True)
    diamond_name=models.ForeignKey(StoneDetails,verbose_name="Purchase order Diamond Name",on_delete=models.PROTECT)
    diamond_pieces=models.IntegerField(verbose_name="Purchase order Diamond Pieces",null=True,blank=True)
    diamond_weight=models.FloatField(max_length=50,verbose_name="Purchase order Diamond Weight",null=True,blank=True)
    diamond_weight_type=models.ForeignKey(StoneWeightType,verbose_name="Purchase order Weight Type",on_delete=models.PROTECT)
    diamond_rate=models.FloatField(max_length=50,verbose_name="Purchase order Diamond Rate",null=True,blank=True)
    diamond_rate_type=models.ForeignKey(RateType,verbose_name="Purchase order Rate Type",on_delete=models.PROTECT)
    include_diamond_weight=models.BooleanField(verbose_name="Purchase order Include Diamond Weight",default=True)
    total_diamond_value=models.FloatField(max_length=50,verbose_name="Purchase order total Diamond Value",null=True,blank=True)

    class Meta:
        db_table = 'newpurchase_item_diamond'
        verbose_name = 'newpurchase_item_diamond'
        verbose_name_plural = 'newpurchase_item_diamonds'

    def __str__(self) -> str:
        return self.diamond_pieces
 
  
class MetalRateCut(models.Model):
    payment_bill_no = models.CharField(max_length=20,verbose_name="payment by metalbill no",null=True,blank=True)
    designer_name = models.ForeignKey(AccountHeadDetails,related_name="purchase_bymetal_designer",on_delete=models.CASCADE,null=True,blank=True)  
    date=models.DateField(verbose_name="paymentbymetaldate",null=True,blank=True)  
    purchase_order = models.CharField(max_length = 20,verbose_name="purchase_payment_metal_cut",null=True,blank=True)
    metal=models.ForeignKey(Metal,related_name="purchase_rate_cut_metal",on_delete=models.PROTECT,null=True,blank=True)
    metal_weight=models.FloatField(max_length=100,verbose_name=" metal_weight",null=True,blank=True,default=0.0)
    pure_calculation=models.FloatField(verbose_name="pure_calculation",null=True,blank=True,default=0)
    pure_weight=models.FloatField(max_length=100,verbose_name="metalrate cut pure weight",null=True,blank=True,default=0.0)
    discount = models.FloatField(max_length = 100,verbose_name ="metal_rate cut discount",null=True,blank=True,default=0.0)
    branch = models.ForeignKey(Branch, related_name="metalrate_cut_branch", on_delete=models.DO_NOTHING,null=True,blank=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.ForeignKey(User, related_name="metalratecut_modified_by", on_delete=models.DO_NOTHING,null=True,blank=True)
    class Meta:
        db_table = 'vendormetal_rate_cut'
        verbose_name = 'vendormetal_rate_cut'
        verbose_name_plural = 'vendormetal_rate_cut'

    def __str__(self) -> str:
        return self.pure_weight
    
class CashRateCut(models.Model):
    payment_bill_no = models.CharField(max_length=20,verbose_name="payment by cash bill no",null=True,blank=True)
    designer_name = models.ForeignKey(AccountHeadDetails,related_name="purchase_cash_designer",on_delete=models.CASCADE,null=True,blank=True)  
    date=models.DateField(verbose_name="paymentbycashdate",null=True,blank=True)  
    purchase_order = models.CharField(max_length=50,verbose_name="purchase_payment_metal_rate",null=True,blank=True)
    pure_weight=models.FloatField(max_length=100,verbose_name="pure_weight",null=True,blank=True,default=0.0)
    rate=models.FloatField(max_length=100,verbose_name=" metal_weight",null=True,blank=True,default=0.0)
    rate_cut=models.FloatField(max_length=100,verbose_name="pure_weight",null=True,blank=True,default=0.0)
    discount = models.FloatField(max_length = 100,verbose_name ="rate cut discount",null=True,blank=True,default=0.0)
    branch = models.ForeignKey(Branch, related_name="cash_ratecut_branch", on_delete=models.DO_NOTHING,null=True,blank=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by =models.ForeignKey(User, related_name="cashratecut_modified_by", on_delete=models.DO_NOTHING,null=True,blank=True)
    class Meta:
        db_table = 'vendorcash_rate_cut'
        verbose_name = 'vendorcash_rate_cut'
        verbose_name_plural = 'vendorcash_rate_cut'

    def __str__(self) -> str:
        return self.rate_cut
    
class AmountSettle(models.Model):
    payment_bill_no = models.CharField(max_length=20,verbose_name="payment bymaount bill no",null=True,blank=True)
    designer_name = models.ForeignKey(AccountHeadDetails,related_name="purchase_amount_designer",on_delete=models.CASCADE,null=True,blank=True)  
    date=models.DateField(verbose_name="paymentamountdate",null=True,blank=True)  
    purchase_order = models.CharField(max_length=50,verbose_name="purchaseorder",null=True,blank=True)
    amount = models.FloatField(max_length = 100,verbose_name ="amount",null=True,blank=True,default=0.0)
    discount = models.FloatField(max_length = 100,verbose_name ="discount",null=True,blank=True,default=0.0)
    cash_receivable = models.BooleanField(verbose_name='reduce cash',default=False,null=True,blank=True)
    metal_receivable=models.BooleanField(verbose_name='reduce cash',default=False,null=True,blank=True)
    branch = models.ForeignKey(Branch, related_name="payment_settle_branch", on_delete=models.DO_NOTHING,null=True,blank=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.ForeignKey(User, related_name="vendor_amount_modified_by", on_delete=models.DO_NOTHING,null=True,blank=True)
    class Meta:
        db_table = 'vendor_amountsettle'
        verbose_name = 'vendor_amountsettle'
        verbose_name_plural = 'vendor_amountsettle'

    def __str__(self) -> str:
        return self.amount