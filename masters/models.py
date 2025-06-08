from django.db import models
from accounts.models import *
from books.models import AccountHeadDetails


class Metal(models.Model):
    metal_name = models.CharField(max_length=100, verbose_name="Metal name", unique=True)
    metal_code = models.CharField(max_length=10, verbose_name="Metal code", unique=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.SET_DEFAULT, default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'metals'
        verbose_name = 'metal'
        verbose_name_plural = 'metals'

    def __str__(self) -> str:
        return self.metal_name
    
class Purity(models.Model):
    purity_name = models.CharField(max_length=100, verbose_name="Purity name", unique=False)
    purity_code = models.CharField(max_length=10, verbose_name="Purity code", unique=True)
    purrity_percent = models.FloatField(verbose_name='Purity percent')
    metal = models.ForeignKey(Metal, verbose_name="Metal", on_delete=models.PROTECT)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    is_visible = models.BooleanField(verbose_name="Visible", default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.SET_DEFAULT, default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'purities'
        verbose_name = 'purity'
        verbose_name_plural = 'purities'

    def __str__(self) -> str:
        return self.purity_name
    
# class MetalRate(models.Model):

#     association_rate = models.JSONField(verbose_name="Association rate")
#     rate = models.JSONField(verbose_name="Rate")    
#     created_at = models.DateTimeField(verbose_name="Created at", null=True)
#     created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.SET_DEFAULT, default=1)
#     modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
#     modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

#     class Meta:
#         db_table = 'metal_rates'
#         verbose_name = 'metal_rate'
#         verbose_name_plural = 'metal_rates'

#     def __str__(self) -> str:
#         return str(self.created_at)


class MetalRate(models.Model):
    
    rate = models.FloatField(verbose_name="Rate")
    purity = models.ForeignKey(Purity,verbose_name="Purity",on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="Created at",null=True,blank=True)
    created_by = models.CharField(max_length=150,verbose_name="Created by",null=True,blank=True)
    
    class Meta:
        db_table = 'metal_rate'
        verbose_name = 'metal_rate'
        verbose_name_plural = 'metal_rates'

    def __str__(self) -> str:
        return self.purity.purity_name
 
class TaxDetails(models.Model):
    metal=models.ForeignKey(Metal,verbose_name="Metal Details",on_delete=models.CASCADE)
    tax_code=models.CharField(max_length=50,verbose_name="Tax Code",unique=True)
    tax_name=models.CharField(max_length=50,verbose_name="Tax Name")
    tax_description=models.CharField(max_length=50,verbose_name="Tax Description")
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.SET_DEFAULT, default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'tax_detail'
        verbose_name = 'tax_detail'
        verbose_name_plural = 'tax_details'

    def __str__(self) -> str:
        return self.tax_name

class PurchaseTaxDetails(models.Model):
    tax_details=models.ForeignKey(TaxDetails,verbose_name="Tax Details",on_delete=models.CASCADE)
    purchase_tax_igst=models.FloatField(max_length=10,verbose_name="IGST Purchase Tax",default=0.0)
    purchase_tax_cgst=models.FloatField(max_length=10,verbose_name="CGST Purchase Tax",default=0.0)
    purchase_tax_sgst=models.FloatField(max_length=10,verbose_name="SGST Purchase Tax",default=0.0)
    purchase_surcharge_percent=models.FloatField(max_length=10,verbose_name="Surcharge Percentage")
    purchase_additional_charges=models.FloatField(max_length=10,verbose_name="Additional Charges")
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.SET_DEFAULT, default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)


    class Meta:
        db_table = 'purchase_tax_detail'
        verbose_name = 'purchase_tax_detail'
        verbose_name_plural = 'purchase_tax_details'

    def __str__(self) -> str:
        return self.tax_details.tax_name
    
class SalesTaxDetails(models.Model):
    tax_details=models.ForeignKey(TaxDetails,verbose_name="Tax Details",on_delete=models.CASCADE)
    sales_tax_igst=models.FloatField(max_length=10,verbose_name="IGST Sales Tax",default=0.0)
    sales_tax_cgst=models.FloatField(max_length=10,verbose_name="CGST Sales Tax",default=0.0)
    sales_tax_sgst=models.FloatField(max_length=10,verbose_name="SGST Sales Tax",default=0.0)
    sales_surcharge_percent=models.FloatField(max_length=10,verbose_name="Surcharge Percentage")
    sales_additional_charges=models.FloatField(max_length=10,verbose_name="Additional Charges")
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.SET_DEFAULT, default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)


    class Meta:
        db_table = 'sales_tax_detail'
        verbose_name = 'sales_tax_detail'
        verbose_name_plural = 'sales_tax_details'

    def __str__(self) -> str:
        return self.tax_details.tax_name
    
class ShapeDetails(models.Model):
    shape_name=models.CharField(max_length=30,verbose_name="Shape",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'shape_detail'
        verbose_name = 'shape_detail'
        verbose_name_plural = 'shape_details'

    def __str__(self) -> str:
        return self.shape_name
    
class CutDetails(models.Model):
    cut_name=models.CharField(max_length=30,verbose_name="Cut",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'cut_detail'
        verbose_name = 'cut_detail'
        verbose_name_plural = 'cut_details'

    def __str__(self) -> str:
        return self.cut_name
    
class ColorDetails(models.Model):
    color_name=models.CharField(max_length=30,verbose_name="Color",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'color_detail'
        verbose_name = 'color_detail'
        verbose_name_plural = 'color_details'

    def __str__(self) -> str:
        return self.color_name
    
class ClarityDetails(models.Model):
    clarity_name=models.CharField(max_length=30,verbose_name="Clarity",unique=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'clarity_detail'
        verbose_name = 'clarity_detail'
        verbose_name_plural = 'clarity_details'

    def __str__(self) -> str:
        return self.clarity_name
    

class CentGroup(models.Model):
    centgroup_name=models.CharField(max_length=30,verbose_name="Cent Group",unique=True)
    from_weight=models.FloatField(max_length=10,verbose_name="From Weight")
    to_weight=models.FloatField(max_length=10,verbose_name="To Weight")
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'centgroup_detail'
        verbose_name = 'centgroup_detail'
        verbose_name_plural = 'centgroup_details'

    def __str__(self) -> str:
        return self.centgroup_name
    

class TagTypes(models.Model):
    tag_name=models.CharField(max_length=25,verbose_name="Tag Type Name",unique=True)
    tag_code=models.CharField(max_length=10,verbose_name="Tag Type Name",unique=True)
    metal=models.ForeignKey(Metal,on_delete=models.DO_NOTHING)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'tag_type'
        verbose_name = 'tag_type'
        verbose_name_plural = 'tag_types'

    def __str__(self) -> str:
        return self.tag_name
    

class StoneDetails(models.Model):
    stone_name=models.CharField(max_length=50,verbose_name="Stone Name")
    stone_code=models.CharField(max_length=10,verbose_name="Stone Code")
    reduce_weight=models.BooleanField(verbose_name="Reduce Weight",default=False)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'stone_detail'
        verbose_name = 'stone_detail'
        verbose_name_plural = 'stone_details'

    def __str__(self) -> str:
        return self.stone_name
    
class CaratRate(models.Model):
    designer=models.ForeignKey(AccountHeadDetails,verbose_name="Designer",on_delete=models.DO_NOTHING)
    stone=models.ForeignKey(StoneDetails,verbose_name="Stone",on_delete=models.PROTECT)
    shape=models.ForeignKey(ShapeDetails,verbose_name="Shape",on_delete=models.PROTECT)
    cut=models.ForeignKey(CutDetails,verbose_name="Cut",on_delete=models.PROTECT)
    color=models.ForeignKey(ColorDetails,verbose_name="Color",on_delete=models.PROTECT)
    clarity=models.ForeignKey(ClarityDetails,verbose_name="Clarity",on_delete=models.PROTECT)
    cent_group=models.ForeignKey(CentGroup,verbose_name="Cent Group",on_delete=models.PROTECT)
    purchase_rate=models.FloatField(max_length=100,verbose_name="Purchase Rate")
    selling_rate=models.FloatField(max_length=100,verbose_name="Selling Rate")
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'carat_rate_detail'
        verbose_name = 'carat_rate_detail'
        verbose_name_plural = 'carat_rate_details'

    def __str__(self) -> str:
        return self.designer.account_head_name
    

    
class TaxDetailsAudit(models.Model):
    tax_details=models.OneToOneField(TaxDetails,verbose_name="Tax Details",on_delete=models.PROTECT)
    metal=models.OneToOneField(Metal,verbose_name="Metal",on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'tax_details_audit'
        verbose_name = 'tax_details_audit'
        verbose_name_plural = 'tax_details_audit'

    def __str__(self) -> str:
        return self.tax_details.tax_name

class MetalOldRate(models.Model):
    metal=models.ForeignKey(Metal,verbose_name="Metal",on_delete=models.PROTECT)
    old_metal_rate=models.FloatField(max_length=50,verbose_name="old Metal Rate", null=True,blank=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'metal_old_rate'
        verbose_name = 'metal_old_rate'
        verbose_name_plural = 'metal_old_rates'

    def __str__(self) -> str:
        return self.metal.metal_name
    
class RepairType(models.Model):
    repair_type_name = models.CharField(max_length=30,verbose_name="Repair Type")
    min_vendor_charges=models.FloatField(verbose_name="Min Vendor Charges",default=0.0)
    max_vendor_charges=models.FloatField(verbose_name="Max Vendor Charges",default=0.0)
    min_customer_charges=models.FloatField(verbose_name="Min Customer Charges",default=0.0)
    max_customer_charges=models.FloatField(verbose_name="Max Customer Charges",default=0.0)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By",related_name="repair_type_created_by",on_delete=models.DO_NOTHING)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.ForeignKey(User, verbose_name="Created By",related_name="repair_type_modified_by",on_delete=models.DO_NOTHING,null=True,blank=True)

    class Meta:
        db_table = 'repair_type'
        verbose_name = 'repair_type'
        verbose_name_plural = 'repair_types'

    def __str__(self) -> str:
        return self.repair_type_name

class CardType(models.Model):
    card_name=models.CharField(max_length=100,verbose_name="Card Name",unique=True)
    is_active=models.BooleanField(verbose_name="Active",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'card_type'
        verbose_name = 'card_type'
        verbose_name_plural = 'card_types'

    def __str__(self) -> str:
        return self.card_name
    

class VoucherType(models.Model):
    voucher_name=models.CharField(max_length=100,verbose_name="Voucher Name",unique=True)
    is_active=models.BooleanField(verbose_name="Active",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'voucher_type'
        verbose_name = 'voucher_type'
        verbose_name_plural = 'voucher_types'

    def __str__(self) -> str:
        return self.voucher_name


class GiftVoucher(models.Model):
    voucher_type=models.ForeignKey(VoucherType,verbose_name="Voucher Type",on_delete=models.PROTECT)
    voucher_no=models.CharField(max_length=100,verbose_name="Voucher Number")
    cash=models.FloatField(max_length=50,verbose_name="Cash")
    from_date=models.DateField(verbose_name="From date")
    to_date=models.DateField(verbose_name="To date")
    is_active=models.BooleanField(verbose_name="Active",default=True)
    is_redeemed=models.BooleanField(verbose_name="Active",default=False)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'gift_voucher'
        verbose_name = 'gift_voucher'
        verbose_name_plural = 'gift_voucheres'

    def __str__(self) -> str:
        return self.voucher_type.voucher_name
    
class GSTType(models.Model):
    gst_type_name=models.CharField(max_length=100,verbose_name="GST Type Name",unique=True)
    is_active=models.BooleanField(verbose_name="Active",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'gst_type'
        verbose_name = 'gst_type'
        verbose_name_plural = 'gst_types'

    def __str__(self) -> str:
        return self.gst_type_name
    

class CashCounter(models.Model):
    counter_name=models.CharField(max_length=100,verbose_name="Counter Name",unique=True)
    password=models.CharField(max_length=120,verbose_name="Password")
    is_active=models.BooleanField(verbose_name="Active",default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'cash_counter'
        verbose_name = 'cash_counter'
        verbose_name_plural = 'cash_counter'

    def __str__(self) -> str:
        return self.counter_name
    
