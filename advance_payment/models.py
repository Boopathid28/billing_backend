from django.db import models
from accounts.models import *
from customer.models import Customer
from masters.models import Purity

class AdvancePurpose(models.Model):
    purpose_name = models.CharField(max_length=100, verbose_name="purpose Name")
    is_active = models.BooleanField(verbose_name="Active", default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.SET_DEFAULT, default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'advance_purpose'
        verbose_name = 'advance_purpose'
        verbose_name_plural = 'advance_purposes'

    def __str__(self) -> str:
        return self.purpose_name

class  AdvanceDetails(models.Model):
    
    advance_id = models.CharField(max_length=150,verbose_name="Advance ID",unique=True)
    customer_details = models.ForeignKey(Customer,verbose_name="Customer Details",on_delete=models.PROTECT)
    total_advance_amount = models.FloatField(verbose_name="Total Advance Amount",default=0.0)
    advance_weight_purity = models.ForeignKey(Purity,verbose_name="Advance Weight Purity",on_delete=models.PROTECT,null=True,blank=True)
    total_advance_weight = models.FloatField(verbose_name="Total Advance Weight",default=0.0)
    advance_purpose = models.ForeignKey(AdvancePurpose,verbose_name="Advance Purpose",null=True,blank=True,on_delete=models.PROTECT)
    remark = models.TextField(verbose_name="Remark",null=True,blank=True)
    is_redeemed = models.BooleanField(verbose_name="Redeem Status",default=False)
    is_cancelled = models.BooleanField(verbose_name="Cancel Status",default=False)
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name="Created at",null=True,blank=True)
    created_by = models.ForeignKey(User,verbose_name="Created by",on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'advance_details'
        verbose_name = 'advance_details'
        verbose_name_plural = 'advance_details'
        
    def __str__(self) -> str:
        return self.advance_id
    
class AdvanceLogs(models.Model):
    
    advance_details = models.ForeignKey(AdvanceDetails,verbose_name="Advance Details",on_delete=models.CASCADE)
    redeem_amount = models.FloatField(verbose_name="Redeem Amount",default=0.0)
    redeem_weight = models.FloatField(verbose_name="Redeem Weight",default=0.0)
    is_cancelled = models.BooleanField(verbose_name="Cancel Status",default=False)
    
    class Meta:
        db_table = 'advance_log_details'
        verbose_name = 'advance_log_details'
        verbose_name_plural = 'advance_log_details'
        
    def __str__(self) -> str:
        return self.advance_details.advance_id