from django.db import models
from accounts.models import *
 
class CompanyDetails(models.Model):
 
    company_name = models.CharField(max_length=100, verbose_name="Company name")
    mobile_no = models.CharField(max_length=10, verbose_name="Mobile no")
    email_id = models.CharField(max_length=100, verbose_name="Email id")
    website = models.CharField(max_length=100, verbose_name="Website", null=True, blank=True)
    std_code = models.CharField(max_length=10, verbose_name="STD code", null=True, blank=True)
    landline_no = models.CharField(max_length=100, verbose_name="Landline no", null=True, blank=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)
 
    class Meta:
        db_table = 'company_details'
        verbose_name = 'company_detail'
        verbose_name_plural = 'company_details'
 
    def __str__(self) -> str:
        return self.company_name
   
class CompanyAddressDetails(models.Model):
 
    company_details = models.ForeignKey(CompanyDetails, verbose_name='Company', on_delete=models.CASCADE)
    door_no = models.CharField(max_length=10, verbose_name="Door no",null=True,blank=True)
    street_name = models.CharField(max_length=50, verbose_name="Street name",null=True,blank=True)
    area = models.CharField(max_length=100, verbose_name="Area",null=True,blank=True)
    taluk = models.CharField(max_length=100, verbose_name="Taluk",null=True,blank=True)
    postal = models.CharField(max_length=100, verbose_name="Postal code",null=True,blank=True)
    district = models.CharField(max_length=50, verbose_name="District",null=True,blank=True)
    state = models.CharField(max_length=50, verbose_name="State",null=True,blank=True)
    country = models.CharField(max_length=50, verbose_name="Country",null=True,blank=True)
    pincode = models.CharField(max_length=50, verbose_name="Pincode")
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)
 
    class Meta:
        db_table = 'company_address_details'
        verbose_name = 'company_address_detail'
        verbose_name_plural = 'company_address_details'
 
    def __str__(self) -> str:
        return self.company_details.company_name
   
class CompanyBankDetails(models.Model):
 
    company_details = models.ForeignKey(CompanyDetails, verbose_name='Company', on_delete=models.CASCADE)
    acc_holder_name = models.CharField(max_length=100, verbose_name="Acc holder name", null=True, blank=True)
    account_no = models.CharField(max_length=100, verbose_name="Account no", null=True, blank=True)
    ifsc_code = models.CharField(max_length=100, verbose_name="IFSC code", null=True, blank=True)
    bank_name = models.CharField(max_length=100, verbose_name="Bank name", null=True, blank=True)
    branch_name = models.CharField(max_length=100, verbose_name="Branch name", null=True, blank=True)
    micr_code = models.CharField(max_length=100, verbose_name="MICR code", null=True, blank=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)
 
    class Meta:
        db_table = 'company_bank_details'
        verbose_name = 'company_bank_detail'
        verbose_name_plural = 'company_bank_details'
 
    def __str__(self) -> str:
        return self.company_details.company_name
   
class CompanyGstDetails(models.Model):
 
    company_details = models.ForeignKey(CompanyDetails, verbose_name='Company', on_delete=models.CASCADE)
    pan_no = models.CharField(max_length=50, verbose_name="Pan no", null=True, blank=True)
    gst_no = models.CharField(max_length=100, verbose_name="GST no", null=True, blank=True)
    registered_name = models.CharField(max_length=100, verbose_name="Registered name", null=True, blank=True)
    gst_status = models.CharField(max_length=100, verbose_name="GST status", null=True, blank=True)
    tax_payer_type = models.CharField(max_length=100, verbose_name="Tax payer type", null=True, blank=True)
    bussiness_type = models.CharField(max_length=100, verbose_name="Bussiness type", null=True, blank=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)
 
    class Meta:
        db_table = 'company_gst_details'
        verbose_name = 'company_gst_detail'
        verbose_name_plural = 'company_gst_details'
 
    def __str__(self) -> str:
        return self.company_details.company_name
   
class GroupLedger(models.Model):
 
    group_ledger_name = models.CharField(max_length=50, verbose_name="Group ledger name")
 
    class Meta:
        db_table = 'group_ledgers'
        verbose_name = 'group_ledger'
        verbose_name_plural = 'group_ledgers'
 
    def __str__(self) -> str:
        return self.group_ledger_name
   
class GroupType(models.Model):
 
    group_type_name = models.CharField(max_length=50, verbose_name="Group type name")
 
    class Meta:
        db_table = 'group_types'
        verbose_name = 'group_type'
        verbose_name_plural = 'group_types'
 
    def __str__(self) -> str:
        return self.group_type_name
   
class AccountGroup(models.Model):
 
    account_group_name = models.CharField(max_length=50, verbose_name="Group type name")
    account_under = models.CharField(max_length=50, verbose_name="Group under",null=True, blank=True)
    group_ledger=models.ForeignKey(GroupLedger,verbose_name="Group Ledger",default=1,on_delete=models.DO_NOTHING)
    group_type=models.ForeignKey(GroupType,verbose_name="Group Type",default=1,on_delete=models.DO_NOTHING)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)
 
    class Meta:
        db_table = 'account_groups'
        verbose_name = 'account_group'
        verbose_name_plural = 'account_groups'
 
    def __str__(self) -> str:
        return self.account_group_name
   
class CustomerType(models.Model):
 
    customer_type_name = models.CharField(max_length=50, verbose_name="Customer type name")
 
    class Meta:
        db_table = 'customer_types'
        verbose_name = 'customer_type'
        verbose_name_plural = 'customer_types'
 
    def __str__(self) -> str:
        return self.customer_type_name
   
class AccountType(models.Model):
 
    account_type_name = models.CharField(max_length=50, verbose_name="Account type name")
 
    class Meta:
        db_table = 'account_types'
        verbose_name = 'account_type'
        verbose_name_plural = 'account_types'
 
    def __str__(self) -> str:
        return self.account_type_name
 
class AccountHeadDetails(models.Model):
 
    account_head_name = models.CharField(max_length=50, verbose_name="Account Head Name")
    account_head_code= models.CharField(max_length=20, verbose_name="Account Head Code")
    customer_type=models.ForeignKey(CustomerType,verbose_name="Customer Type",default=1,on_delete=models.DO_NOTHING)
    is_buyer=models.BooleanField(verbose_name="Buyer",default=True)
    account_type=models.ForeignKey(AccountType,verbose_name="Account Type",default=1,on_delete=models.DO_NOTHING)
    group_name=models.ForeignKey(AccountGroup,verbose_name="Group Name",default=1,on_delete=models.DO_NOTHING)
    is_diamond_dealer=models.BooleanField(verbose_name="Diamond Dealer",default=True)
    credit_balance_rupee=models.CharField(max_length=10,verbose_name="Credit Balance(₹)")
    credit_balance_gm=models.CharField(max_length=10,verbose_name="Credit Balance(gm)")
    debit_balance_rupee=models.CharField(max_length=10,verbose_name="Debit Balance(₹)")
    debit_balance_gm=models.CharField(max_length=10,verbose_name="Debit Balance(gm)")
    upi_id = models.CharField(max_length=150,verbose_name="UPI ID",null=True,blank=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)
 
    class Meta:
        db_table = 'account_head'
        verbose_name = 'account_head'
        verbose_name_plural = 'account_heads'
 
    def __str__(self) -> str:
        return self.account_head_name
class AccountHeadAddress(models.Model):
    account_head=models.ForeignKey(AccountHeadDetails,verbose_name="Account Head",on_delete=models.CASCADE)
    door_no=models.CharField(max_length=10,verbose_name="Door Number")
    street_name=models.CharField(max_length=100,verbose_name="Street Name")
    area=models.CharField(max_length=50,verbose_name="Area")
    taluk=models.CharField(max_length=50,verbose_name="Taluk")
    postal=models.CharField(max_length=50,verbose_name="Postal")
    district=models.CharField(max_length=50,verbose_name="District")
    state=models.CharField(max_length=50,verbose_name="State")
    country=models.CharField(max_length=50,verbose_name="Country")
    pin_code=models.CharField(max_length=10,verbose_name="PinCode")
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)
 
    class Meta:
        db_table = 'account_head_address'
        verbose_name = 'account_head_address'
        verbose_name_plural = 'account_head_addresss'
 
    def __str__(self) -> str:
        return self.account_head.account_head_name
   
class AccountHeadContact(models.Model):
    account_head=models.ForeignKey(AccountHeadDetails,verbose_name="Account Head",on_delete=models.CASCADE)
    mobile_number=models.CharField(max_length=10,verbose_name="Mobile Number")
    email_id=models.CharField(max_length=100,verbose_name="Email ID",null=True, blank=True)
    website=models.CharField(max_length=100,verbose_name="Website",null=True, blank=True)
    std_code=models.CharField(max_length=10,verbose_name="STD Code",null=True, blank=True)
    landline_number=models.CharField(max_length=50,verbose_name="Landline Number",null=True, blank=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)
 
    class Meta:
        db_table = 'account_head_contact'
        verbose_name = 'account_head_contact'
        verbose_name_plural = 'account_head_contacts'
 
    def __str__(self) -> str:
        return self.account_head.account_head_name
   
class AccountHeadBankDetails(models.Model):
 
    account_head=models.ForeignKey(AccountHeadDetails,verbose_name="Account Head",on_delete=models.CASCADE)
    acc_holder_name = models.CharField(max_length=100, verbose_name="Acc holder name", null=True, blank=True)
    account_no = models.CharField(max_length=100, verbose_name="Account no", null=True, blank=True)
    ifsc_code = models.CharField(max_length=100, verbose_name="IFSC code", null=True, blank=True)
    bank_name = models.CharField(max_length=100, verbose_name="Bank name", null=True, blank=True)
    branch_name = models.CharField(max_length=100, verbose_name="Branch name", null=True, blank=True)
    micr_code = models.CharField(max_length=100, verbose_name="MICR code", null=True, blank=True)
    is_active=models.BooleanField(verbose_name="Status",default=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)
 
    class Meta:
        db_table = 'account_head_bank'
        verbose_name = 'account_head_bank'
        verbose_name_plural = 'account_head_banks'
 
    def __str__(self) -> str:
        return self.account_head.account_head_name
 
class AccountHeadGstDetails(models.Model):
 
    account_head=models.ForeignKey(AccountHeadDetails,verbose_name="Account Head",on_delete=models.CASCADE)
    pan_no = models.CharField(max_length=50, verbose_name="Pan no", null=True, blank=True)
    tin_no=models.CharField(max_length=50, verbose_name="TIN no", null=True, blank=True)
    gst_no = models.CharField(max_length=100, verbose_name="GST no", null=True, blank=True)
    registered_name = models.CharField(max_length=100, verbose_name="Registered name", null=True, blank=True)
    gst_status = models.CharField(max_length=50, verbose_name="GST status", null=True, blank=True)
    tax_payer_type = models.CharField(max_length=50, verbose_name="Tax payer type", null=True, blank=True)
    bussiness_type = models.CharField(max_length=50, verbose_name="Bussiness type", null=True, blank=True)
    is_active=models.BooleanField(verbose_name="Status",default=True, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name='Created by', on_delete=models.DO_NOTHING)
    modified_by = models.IntegerField(verbose_name='Modified by', null=True, blank=True)
 
    class Meta:
        db_table = 'account_head_gst'
        verbose_name = 'account_head_gst'
        verbose_name_plural = 'account_head_gst'
 
    def __str__(self) -> str:
        return self.account_head.account_head_name