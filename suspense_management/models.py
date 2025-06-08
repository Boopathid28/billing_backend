from django.conf import settings
from django.db import models
from customer.models import Customer
from masters.models import Metal
from organizations.models import Branch
from payment_management.models import PaymentMenthod,PaymentProviders

# Create your models here.

class SuspenseDetails(models.Model):
    
    customer_details = models.ForeignKey(Customer,verbose_name="Customer Details",on_delete=models.PROTECT)
    suspense_id = models.CharField(max_length=150,verbose_name="Suspense ID",unique=True)
    is_redeemed = models.BooleanField(verbose_name="Redeem Status",default=False)
    bill_number = models.CharField(max_length=150,verbose_name="Bill Number",null=True,blank=True)
    is_closed = models.BooleanField(verbose_name="Closed Status",default=False)
    closed_by = models.CharField(max_length=150,verbose_name="Closed By",null=True,blank=True)
    closed_date = models.DateTimeField(verbose_name="Closed Date",null=True,blank=True)
    is_cancelled = models.BooleanField(verbose_name="Cancel Status",default=False)
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name="Created at",null=True,blank=True)
    created_by = models.CharField(max_length=150,verbose_name="Created by",null=True,blank=True)
    
    class Meta:
        db_table = 'suspense_details'
        verbose_name = 'suspense_details'
        verbose_name_plural = 'suspense_details'
        
    def __str__(self) -> str:
        return self.suspense_id
        
class SuspenseItemDetails(models.Model):
    
    suspense_details = models.ForeignKey(SuspenseDetails,verbose_name="Suspense Details",on_delete=models.CASCADE)
    metal_details = models.ForeignKey(Metal,verbose_name="Metal Details",on_delete=models.PROTECT)
    metal_weight = models.FloatField(verbose_name="Metal Weight",default=0.0)
    metal_amount = models.FloatField(verbose_name="Metal Amount",default=0.0)
    total_amount = models.FloatField(verbose_name="Total Amount",default=0.0)
    
    class Meta:
        db_table = 'suspense_item_details'
        verbose_name = 'suspense_item_details'
        verbose_name_plural = 'suspense_item_details'
        
    def __str__(self) -> str:
        return self.suspense_details.suspense_id
        
class SuspensePaymentDetails(models.Model):
    
    suspense_details = models.ForeignKey(SuspenseDetails,verbose_name="Suspense Details",on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=150,verbose_name="Payment ID",unique=True)
    payment_date = models.DateTimeField(verbose_name="Payment Date")
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    created_by = models.CharField(max_length=150,verbose_name="Created by",null=True,blank=True)
        
    class Meta:
        db_table = 'suspense_payment_details'
        verbose_name = 'suspense_payment_details'
        verbose_name_plural = 'suspense_payment_details'
        
    def __str__(self) -> str:
        return self.suspense_details.suspense_id
    
class SuspensePaymentDenominations(models.Model):
    
    payment_details = models.ForeignKey(SuspensePaymentDetails,verbose_name="Suspense Payment Details",on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMenthod,verbose_name="Payment Method",default=1,on_delete=models.PROTECT)
    payment_provider = models.ForeignKey(PaymentProviders,verbose_name="Payment Provider",null=True,blank=True,on_delete=models.PROTECT)
    paid_amount = models.FloatField(verbose_name="Paid Amount",default=0.0)
    remark = models.CharField(max_length=150,verbose_name="Remark",null=True,blank=True)
    
    class Meta:
        db_table = 'suspense_payment_denominations'
        verbose_name = 'suspense_payment_denominations'
        verbose_name_plural = 'suspense_payment_denominations'
        
    def __str__(self) -> str:
        return self.payment_details.payment_id