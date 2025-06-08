from django.db import models
from customer.models import Customer
from accounts.models import User
from masters.models import VoucherType,CardType, GSTType
from books.models import AccountHeadBankDetails,AccountHeadDetails

# Create your models here.

class PaymentMenthod(models.Model):
    payment_method_name = models.CharField(max_length=50,verbose_name="Payment Method Name",unique=True)
    color = models.CharField(max_length=50,verbose_name="Color",default=1)
    bg_color = models.CharField(max_length=50,verbose_name="BG Color",default=1)
    
    class Meta:
        db_table = 'payment_method'
        verbose_name = 'payment_method'
        verbose_name_plural = 'payment_methods'
 
    def __str__(self) -> str:
        return self.payment_method_name
    
class PaymentProviders(models.Model):
    payment_method = models.ForeignKey(PaymentMenthod,verbose_name="Payment Method",on_delete=models.PROTECT)
    payment_provider_name = models.CharField(max_length=50,verbose_name="Payment Provider Name")
    
    class Meta:
        db_table = 'payment_provider'
        verbose_name = 'payment_provider'
        verbose_name_plural = 'payment_providers'
 
    def __str__(self) -> str:
        return self.payment_provider_name
    
class PaymentModule(models.Model):
    module_name = models.CharField(max_length=50,verbose_name="Module Name",unique=True)
    
    class Meta:
        db_table = 'payment_module'
        verbose_name = 'payment_module'
        verbose_name_plural = 'payment_module'
 
    def __str__(self) -> str:
        return self.module_name

class CustomerPaymentTabel(models.Model):
    payment_method = models.ForeignKey(PaymentMenthod,verbose_name="Payment_method",on_delete=models.PROTECT)
    payment_provider = models.ForeignKey(PaymentProviders,verbose_name="Payment_provider",on_delete=models.PROTECT,null=True,blank=True)
    payment_module = models.ForeignKey(PaymentModule,verbose_name="Payment_module",on_delete=models.PROTECT)
    refference_number = models.CharField(max_length=100,verbose_name="Refference Number")
    paid_amount = models.FloatField(verbose_name="Paid Amount",default=0.0)
    payment_refference_number = models.CharField(max_length=100,verbose_name="Payment Refference Number",null= True,blank=True)
    customer_details = models.ForeignKey(Customer,verbose_name="Cutomer Details",on_delete=models.PROTECT)
    payment_date = models.DateTimeField(verbose_name="Payment Date",null=True,blank=True)
    
    class Meta:
        db_table = 'payment_table'
        verbose_name = 'payment_table'
        verbose_name_plural = 'payment_tables'
 
    def __str__(self) -> str:
        return f"{self.refference_number}"

class CommonPaymentDetails(models.Model):

    refference_number = models.CharField(max_length=100, verbose_name='Order Id',unique=True)
    total_amount=models.FloatField(verbose_name="Total Amount",null=True,blank=True,default=0.0)
    discount_percentage=models.FloatField(verbose_name="Discount Percentage",null=True,blank=True,default=0.0)
    discount_amount=models.FloatField(verbose_name="Discount Amount",null=True,blank=True,default=0.0)
    gst_type=models.ForeignKey(GSTType,verbose_name="GST Type", on_delete=models.PROTECT,default=1)
    igst_percentage=models.FloatField(verbose_name="IGST Percentage",null=True,blank=True,default=0.0)
    igst_amount=models.FloatField(verbose_name="IGST Amount",null=True,blank=True,default=0.0)
    sgst_percentage=models.FloatField(verbose_name="SGST Percentage",null=True,blank=True,default=0.0)
    sgst_amount=models.FloatField(verbose_name="SGST Amount",null=True,blank=True,default=0.0)
    cgst_percentage=models.FloatField(verbose_name="CGST",null=True,blank=True,default=0.0)
    cgst_amount=models.FloatField(verbose_name="CGST",null=True,blank=True,default=0.0)
    others=models.FloatField(verbose_name="Others",null=True,blank=True,default=0.0)
    round_off_total=models.FloatField(verbose_name="Round Off",null=True,blank=True,default=0.0)
    hall_mark_charges=models.FloatField(verbose_name="Hall Mark Charges",null=True,blank=True,default=0.0)
    making_charge_per_gram=models.FloatField(verbose_name="Making Charge Per Gram",default=0.0,null=True,blank=True)
    flat_making_charge=models.FloatField(verbose_name="Flat Making Charge",default=0.0,null=True,blank=True)
    stone_amount=models.FloatField(verbose_name="Stone Amount",default=0.0,null=True,blank=True)
    diamond_amount=models.FloatField(verbose_name="Diamond Amount",default=0.0,null=True,blank=True)
    payable_amount=models.FloatField(verbose_name="Payable Amount",null=True,blank=True,default=0.0)
    salereturn_amount=models.FloatField(max_length=50,verbose_name="Salereturn Amount",null=True, blank=True,default=0.0)
    exchange_amount=models.FloatField(max_length=50,verbose_name="Exchange Amount",null=True, blank=True,default=0.0)
    advance_amount=models.FloatField(verbose_name="Advance Amount",null=True,blank=True,default=0.0)
    balance_amount=models.FloatField(verbose_name="Balance Amount",null=True,blank=True,default=0.0)
    amount_received=models.FloatField(verbose_name="Amount Received",null=True,blank=True,default=0.0)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', related_name='order_payment_created_by', on_delete=models.DO_NOTHING)
    modified_by = models.ForeignKey(User, verbose_name='Modified by', related_name='order_payment_modified_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'common_payment'
        verbose_name = 'common_payment'
        verbose_name_plural = 'common_payments'

    def __str__(self) -> str:
        return self.refference_number