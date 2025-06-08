from django.db import models
from books.models import AccountHeadDetails
from django.conf import settings
from accounts.models import User
from payment_management.models import *
from organizations.models import *

# Create your models here.

class VendorLedgerType(models.Model):
    
    vendor_ledger_type = models.CharField(max_length=100,verbose_name="Vendor Ledger Type",unique=True)
    created_at = models.DateTimeField(verbose_name="Create Date")
    created_by = models.ForeignKey(User,verbose_name="Created by",null=True,blank=True,on_delete=models.PROTECT)

    class Meta:
        db_table = 'vendor_ledger_type'
        verbose_name = 'vendor_ledger_type'
        verbose_name_plural = 'vendor_ledger_types'

    def __str__(self) -> str:
        return self.vendor_ledger_type


class VendorLedger(models.Model):
    
    vendor_details = models.ForeignKey(AccountHeadDetails,verbose_name="Vendor Details",on_delete=models.PROTECT)
    transaction_date = models.DateTimeField(verbose_name="Transaction Date")
    refference_number = models.CharField(max_length=150,verbose_name="Refference Number",null=True,blank=True)
    transaction_type = models.ForeignKey(VendorLedgerType,verbose_name="Transaction Type",default=1,on_delete=models.PROTECT)
    transaction_weight = models.FloatField(verbose_name="Transaction Weight",default=0.0)
    transaction_amount = models.FloatField(verbose_name="Transaction Amount",default=0.0)
    is_canceled = models.BooleanField(verbose_name="Cancel Status",default=False)
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'vendor_ledger'
        verbose_name = 'vendor_ledger'
        verbose_name_plural = 'vendor_ledger'

    def __str__(self) -> str:
        return self.vendor_details.account_head_name
    
class VendorDiscount(models.Model):
    vendor_details = models.ForeignKey(AccountHeadDetails,verbose_name="Vendor Details",on_delete=models.PROTECT)
    discount_id = models.CharField(max_length=150,verbose_name="Discount ID",unique=True)
    discount_date = models.DateTimeField(verbose_name="Discount Date")
    discount_weight = models.FloatField(verbose_name="Discount Weight",default=0.0)
    discount_amount = models.FloatField(verbose_name="Discount Amount",default=0.0)
    remark = models.TextField(verbose_name="Remark",null=True,blank=True)
    created_by = models.ForeignKey(User,verbose_name="Created by",null=True,blank=True,on_delete=models.PROTECT)
    is_canceled = models.BooleanField(verbose_name="Cancel Status",default=False)
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'vendor_discount'
        verbose_name = 'vendor_discount'
        verbose_name_plural = 'vendor_discount'

    def __str__(self) -> str:
        return self.vendor_details.account_head_name
    
    
class VendorPayment(models.Model):
    
    vendor_details = models.ForeignKey(AccountHeadDetails,verbose_name="Vendor Details",on_delete=models.PROTECT)
    payment_id = models.CharField(max_length=150,verbose_name="Payment ID",unique=True)
    payment_date = models.DateTimeField(verbose_name="Payment Date")
    payment_weight = models.FloatField(verbose_name="Payment Weight",default=0.0)
    payment_amount = models.FloatField(verbose_name="Payment Amount",default=0.0)
    remark = models.TextField(verbose_name="Remark",null=True,blank=True)
    created_by = models.ForeignKey(User,verbose_name="Created by",null=True,blank=True,on_delete=models.PROTECT)
    is_canceled = models.BooleanField(verbose_name="Cancel Status",default=False)
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    
    class Meta:
        db_table = 'vendor_payment'
        verbose_name = 'vendor_payment'
        verbose_name_plural = 'vendor_payment'

    def __str__(self) -> str:
        return self.vendor_details.account_head_name
    
class VendorAmountPaymentDenominations(models.Model):
    
    payment_details = models.ForeignKey(VendorPayment,verbose_name="Payment Details",on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMenthod,verbose_name="Payment Methods",default=1,on_delete=models.PROTECT)
    payment_providers = models.ForeignKey(PaymentProviders,verbose_name="Payment Providers",null=True,blank=True,on_delete=models.PROTECT)
    amount = models.FloatField(verbose_name="Amount",default=0.0)
    
    class Meta:
        db_table = 'vendor_payment_amount_denominations'
        verbose_name = 'vendor_payment_amount_denominations'
        verbose_name_plural = 'vendor_payment_amount_denominations'

    def __str__(self) -> str:
        return self.payment_details.vendor_details.account_head_name
    
class VendorWeightPaymentDenominations(models.Model):
    payment_details = models.ForeignKey(VendorPayment,verbose_name="Payment Details",on_delete=models.CASCADE)
    metal_weight = models.FloatField(verbose_name="Metal Weight",default=0.0)
    touch = models.FloatField(verbose_name="Touch",default=0.0)
    pure_weight = models.FloatField(verbose_name="Pure Weight",default=0.0)
    
    class Meta:
        db_table = 'vendor_payment_weight_denominations'
        verbose_name = 'vendor_payment_weight_denominations'
        verbose_name_plural = 'vendor_payment_weight_denominations'

    def __str__(self) -> str:
        return self.payment_details.vendor_details.account_head_name