from django.db import models
from accounts.models import *
from organizations.models import Staff
from tagging.models import TaggedItems,EntryType
from settings.models import SalesEntryType, TransactionType

class CustomerGroup(models.Model):
    customer_group_name = models.CharField(max_length=100, verbose_name="Customer Group",unique=True)
    is_active = models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)

    class Meta:
        db_table = 'customer_groups'
        verbose_name = 'customer_group'
        verbose_name_plural = 'customer_groups'
 
    def __str__(self) -> str:
        return self.customer_group_name

class Customer(models.Model):

    customer_name = models.CharField(max_length=100, verbose_name="Customer Name")
    customer_group = models.ForeignKey(CustomerGroup, verbose_name='Customer Group', on_delete=models.PROTECT)
    email = models.EmailField(max_length=60,verbose_name='Email', null=True, blank=True)
    phone = models.CharField(max_length=10, verbose_name='Phone no', unique=True)
    door_no = models.CharField(max_length=10, verbose_name="Door no",null=True, blank=True)
    street_name = models.CharField(max_length=50, verbose_name="Street name",null=True, blank=True)
    area = models.CharField(max_length=100, verbose_name="Area",null=True, blank=True)
    taluk = models.CharField(max_length=100, verbose_name="Taluk",null=True, blank=True)
    postal = models.CharField(max_length=100, verbose_name="Postal code",null=True, blank=True)
    district = models.CharField(max_length=50, verbose_name="District",null=True, blank=True)
    state = models.CharField(max_length=50, verbose_name="State",null=True, blank=True)
    country = models.CharField(max_length=50, verbose_name="Country",null=True, blank=True)
    pincode = models.CharField(max_length=50, verbose_name="Pincode",null=True, blank=True)
    dob = models.DateField(verbose_name='DOB', null=True, blank=True)
    aadhar_card = models.CharField(max_length=500, verbose_name="Aadhar card", null=True, blank=True)
    pan_card = models.CharField(max_length=500, verbose_name="Pan card", null=True, blank=True)
    gst_no = models.CharField(max_length=500, verbose_name="GST No", null=True, blank=True)
    branch = models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.PROTECT)
    is_married = models.BooleanField(verbose_name="Status",default=False)
    marriage_date = models.DateField(verbose_name="Marriage Date", null=True,blank=True)
    upi_id = models.CharField(max_length=150,verbose_name="UPI ID",null=True,blank=True)
    is_active = models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)

    class Meta:
        db_table = 'customer_details'
        verbose_name = 'customer_detail'
        verbose_name_plural = 'customer_details'
 
    def __str__(self) -> str:
        return self.customer_name


class CustomerLedger(models.Model):
    
    customer_details = models.ForeignKey(Customer,verbose_name="Customer Details",on_delete=models.PROTECT)
    entry_date = models.DateTimeField(verbose_name="Entry Date")
    entry_type = models.ForeignKey(SalesEntryType,verbose_name="Entry Type",default=1,on_delete=models.PROTECT)
    transaction_type = models.ForeignKey(TransactionType,verbose_name="Transaction Type",default=1,on_delete=models.PROTECT)
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    invoice_number = models.CharField(max_length=150,verbose_name="Invoice Number",null=True,blank=True)
    reffrence_number = models.CharField(max_length=150,verbose_name="Refference Number",null=True,blank=True)
    transaction_amount = models.FloatField(verbose_name="Transaction Amount",default=0.0)
    transaction_weight = models.FloatField(verbose_name="Transaction Weight",default=0.0)
    is_cancelled = models.BooleanField(verbose_name="Cancel Status",default=False)
    
    class Meta:
        db_table = 'customer_ledger'
        verbose_name = 'customer_ledger'
        verbose_name_plural = 'customer_ledger'

    def __str__(self) -> str:
        return self.customer_details.customer_name