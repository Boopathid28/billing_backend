from django.db import models
from accounts.models import User,Branch
from customer.models import Customer
from tagging.models import Item
from masters.models import Metal,RepairType, Purity
from books.models import AccountHeadDetails
from settings.models import PaymentStatus,StatusTable
from organizations.models import Staff
from advance_payment.models import AdvanceDetails
from payment_management.models import PaymentMenthod,PaymentProviders

# Create your models here.

class RepairOrderNumber(models.Model):
    repair_number=models.CharField(max_length=20,verbose_name="Repair Number",unique=True)
    created_at=models.DateTimeField(verbose_name="Created_at",null=True,blank=True)
    created_by=models.ForeignKey(User,verbose_name="Created By",on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at=models.DateTimeField(verbose_name="Modified at",null=True,blank=True)
    modified_by=models.CharField(max_length=20,verbose_name="Modified by",null=True,blank=True)

    class Meta:
        db_table = 'repair_number'
        verbose_name = 'repair_number'
        verbose_name_plural = 'repair_numbers'

    def __str__(self) -> str:
        return self.repair_number
    
class RepairFor(models.Model):
    repair_for=models.CharField(max_length=20,verbose_name="Repair For",unique=True)
    created_at=models.DateTimeField(verbose_name="Created_at",null=True,blank=True)
    created_by=models.ForeignKey(User,verbose_name="Created By",on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at=models.DateTimeField(verbose_name="Modified at",null=True,blank=True)
    modified_by=models.CharField(max_length=20,verbose_name="Modified by",null=True,blank=True)

    class Meta:
        db_table = 'repair_for'
        verbose_name = 'repair_for'
        verbose_name_plural = 'repair_for'

    def __str__(self) -> str:
        return self.repair_for
    
class RepairDetails(models.Model):
    repair_number=models.CharField(max_length=20,verbose_name="Repair Number",unique=True)
    repair_for = models.ForeignKey(RepairFor,verbose_name="Repair For",on_delete=models.PROTECT)
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT,null=True,blank=True)
    customer_details=models.ForeignKey(Customer,verbose_name="Customer Details",on_delete=models.PROTECT,null=True,blank=True)
    repair_recived_date=models.DateField(verbose_name="Repair Recieved Date", null=False,blank=False)
    est_repair_delivery_days=models.IntegerField(verbose_name="Repair Delivery Days", null=True,blank=True, default=0)
    est_repair_delivery_date=models.DateField(verbose_name="Repair Delivery Date", null=False,blank=False)
    status = models.ForeignKey(StatusTable,verbose_name="Status",on_delete=models.PROTECT,null=True,blank=True)
    payment_status = models.ForeignKey(PaymentStatus,verbose_name="payment status",related_name="repair_payment_status",on_delete=models.PROTECT,null=True,blank=True)
    total_issued_weight=models.IntegerField(verbose_name="Total Issued Weight",null=True,blank=True,default=0)
    total_customer_charges=models.IntegerField(verbose_name="Total Customer Charges",null=True,blank=True,default=0)
    total_vendor_charges=models.IntegerField(verbose_name="Total Vendor Charges",null=True,blank=True,default=0)
    description=models.CharField(max_length=500,verbose_name="Description",null=True,blank=True)
    is_issued=models.BooleanField(verbose_name="Is issued",default=False)
    created_at=models.DateTimeField(verbose_name="Created_at",null=True,blank=True)
    created_by=models.ForeignKey(User,verbose_name="Created By",on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at=models.DateTimeField(verbose_name="Modified at",null=True,blank=True)
    modified_by=models.CharField(max_length=20,verbose_name="Modified by",null=True,blank=True)

    class Meta:
        db_table = 'repair_detail'
        verbose_name = 'repair_detail'
        verbose_name_plural = 'repair_details'

    def __str__(self) -> str:
        return F"{self.repair_number}"
    
class RepairItemDetails(models.Model):
    repair_order_details=models.ForeignKey(RepairDetails,verbose_name="Repair Order details",on_delete=models.CASCADE,default=1)
    repair_type=models.ForeignKey(RepairType,verbose_name="Repair Type",on_delete=models.PROTECT)
    item_details=models.ForeignKey(Item,verbose_name="Item details",on_delete=models.PROTECT)
    metal_details=models.ForeignKey(Metal,verbose_name="Metal details",on_delete=models.PROTECT)
    issued_gross_weight=models.FloatField(max_length=50,verbose_name="Issued Gross weight",null=True,blank=True,default=0.0)
    issued_net_weight=models.FloatField(max_length=50,verbose_name="Issued Net weight",null=True,blank=True,default=0.0)
    added_net_weight=models.FloatField(max_length=50,verbose_name="Added Net weight",null=True,blank=True,default=0.0)
    less_weight=models.FloatField(max_length=50,verbose_name="Less weight",null=True,blank=True,default=0.0)
    old_stone=models.IntegerField(verbose_name="Old Stone",null=True,blank=True,default=0)
    old_diamond=models.IntegerField(verbose_name="Old Diamond",null=True,blank=True,default=0)  
    total_pieces=models.IntegerField(verbose_name="Total pieces",null=True,blank=True,default=0)
    image=models.FileField(verbose_name="image",null=True,blank=True)
    customer_charges=models.IntegerField(verbose_name="Customer Charges",null=True,blank=True,default=0)
    vendor_charges=models.IntegerField(verbose_name="Vendor Charges",null=True,blank=True,default=0)
    is_assigned = models.BooleanField(verbose_name="Assigned", default=False)
    assigned_by = models.ForeignKey(User, verbose_name='Assigned by', related_name='repair_order_item_assigned_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    order_status = models.ForeignKey(StatusTable,verbose_name="Order Status",on_delete=models.PROTECT,null=True)
    is_recieved = models.BooleanField(verbose_name="Recieved", default=False)
    is_delivered = models.BooleanField(verbose_name="Recieved", default=False)
    delivered_at = models.DateTimeField(verbose_name='Delivered at', null=True, blank=True)
    created_at=models.DateTimeField(verbose_name="Created_at",null=True,blank=True)
    created_by=models.ForeignKey(User,verbose_name="Created By",on_delete=models.DO_NOTHING,null=True,blank=True)
    modified_at=models.DateTimeField(verbose_name="Modified at",null=True,blank=True)
    modified_by=models.CharField(max_length=20,verbose_name="Modified by",null=True,blank=True)

    class Meta:
        db_table = 'repair_item_detail'
        verbose_name = 'repair_item_detail'
        verbose_name_plural = 'repair_item_details'

    def __str__(self) -> str:
        return f"{self.repair_order_details.repair_number}"

    
class RepairOrderIssued(models.Model):
    repair_details=models.ForeignKey(RepairDetails,verbose_name="Repair Details",on_delete=models.CASCADE)
    repair_item_details=models.ForeignKey(RepairItemDetails,verbose_name="Repair Item Details",on_delete=models.CASCADE,null=True)
    vendor_name=models.ForeignKey(AccountHeadDetails,verbose_name="Designer Name",null=True,blank=True,on_delete=models.PROTECT)
    issue_date=models.DateField(verbose_name="Issue Date",null=True,blank=True)
    estimate_due_date=models.DateField(verbose_name="Estimate due Date",null=True,blank=True)
    estimate_due_days = models.IntegerField(verbose_name="Estimate Due Days",null=True,blank=True)
    remainder_days=models.IntegerField(verbose_name="Remainder Days",null=True,blank=True)
    remainder_date=models.DateField(verbose_name="Remainder Date",null=True,blank=True)
    paid_amount=models.FloatField(verbose_name="Paid Amount",null=True,blank=True,default=0)
    paid_weight=models.FloatField(verbose_name="Paid Weight",null=True,blank=True,default=0)
    payment_status=models.ForeignKey(PaymentStatus,verbose_name="Payment status",on_delete=models.PROTECT,null=True,blank=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'repair_order_issued'
        verbose_name = 'repair_order_issued'
        verbose_name_plural = 'repair_order_issued'

    def __str__(self) -> str:
        return self.repair_details.repair_number

class DeliveryBill(models.Model):
    delivery_note_id=models.CharField(max_length=50,verbose_name="Delivery Note ID",unique=True)
    repair_details_id=models.ForeignKey(RepairDetails,verbose_name="Repair Receipt ID",on_delete=models.CASCADE,default=1)
    customer_mobile=models.CharField(max_length=10,verbose_name="Customer Mobile",null=True,blank=True)
    customer_details=models.ForeignKey(Customer,verbose_name="Customer Details",on_delete=models.PROTECT)
    delivery_date=models.DateField(verbose_name="Delivery Date",null=True,blank=True)
    status=models.ForeignKey(StatusTable,verbose_name="Status",null=True,blank=True,on_delete=models.PROTECT)
    total_stone_rate=models.FloatField(verbose_name="Total Stone Rate", null=True,blank=True, default=0.0)
    total_diamond_rate=models.FloatField(verbose_name="Total Diamond Rate", null=True,blank=True, default=0.0)
    estimate_repair_charge=models.FloatField(verbose_name="Estimate Repair Charge", null=True,blank=True, default=0.0)
    working_charge=models.FloatField(verbose_name="Working Charge", null=True,blank=True, default=0.0)
    added_weight_amount=models.FloatField(verbose_name="Added Weight Amount", null=True,blank=True, default=0.0)
    less_weight_amount=models.FloatField(verbose_name="Less Weight Amount", null=True,blank=True, default=0.0)
    advance_amount=models.FloatField(verbose_name="Advance Amount", null=True,blank=True, default=0.0)
    grand_total=models.FloatField(verbose_name="Grand Total", null=True,blank=True, default=0.0)
    balance_amount=models.FloatField(verbose_name="Balance Amount", null=True,blank=True, default=0.0)
    cash=models.FloatField(verbose_name="Cash Amount", null=True,blank=True, default=0.0)
    upi=models.FloatField(verbose_name="UPI Amount", null=True,blank=True, default=0.0)
    debit_card_amount=models.FloatField(verbose_name="Debit Card Amount", null=True,blank=True, default=0.0)
    credit_card_amount=models.FloatField(verbose_name="Credit Card Amount", null=True,blank=True, default=0.0)
    account_transfer=models.FloatField(verbose_name="Account Transfer", null=True,blank=True, default=0.0)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'delivery_bill'
        verbose_name = 'delivery_bill'
        verbose_name_plural = 'delivery_bills'

    def __str__(self) -> str:
        return f"{self.delivery_note_id}"

class RepairOrderOldGold(models.Model):
    refference_number=models.CharField(max_length=50,verbose_name="Refference Number",default=1)
    old_gold_no=models.CharField(max_length=100,verbose_name="Oldgold Number",null=True,blank=True)
    metal=models.ForeignKey(Metal,verbose_name="Metal Name",null=True,blank=True,on_delete=models.PROTECT,default=1)
    gross_weight=models.FloatField(verbose_name="Gross Weight",null=True,blank=True,default=0.0)
    net_weight=models.FloatField(verbose_name="Gross Weight",null=True,blank=True,default=0.0)
    dust_weight = models.FloatField(max_length=50,verbose_name="Dust Weight",null=True,blank=True,default=0.0)
    metal_rate=models.FloatField(verbose_name="Metal Rate",null=True,blank=True,default=0)
    today_metal_rate=models.FloatField(max_length=50,verbose_name="Today Metal Rate",null=True,blank=True,default=0.0)
    old_rate=models.FloatField(verbose_name="Old Rate",null=True,blank=True,default=0)
    total_amount=models.FloatField(verbose_name="Total Amount",null=True,blank=True,default=0)
    purity = models.ForeignKey(Purity,verbose_name="oldgold_purity",null=True,blank=True,on_delete = models.PROTECT,default=1)
    employee_id = models.ForeignKey(Staff,verbose_name="Employee Id",null=True,blank=True,on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.DO_NOTHING,default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'repair_order_oldgold'
        verbose_name = 'repair_order_oldgold'
        verbose_name_plural = 'repair_order_oldgold'

    def __str__(self) -> str:
        return self.refference_number
    


class RepairPayment(models.Model):    

    repair_payment_id = models.CharField(max_length=150,verbose_name="Repair Payment ID",unique=True)
    repair_details = models.ForeignKey(RepairDetails,verbose_name="Repair Details",on_delete=models.CASCADE)
    payment_date = models.DateTimeField(verbose_name="Payment Date")            
    branch=models.ForeignKey(Branch,verbose_name="Branch",on_delete=models.PROTECT)
    created_by = models.CharField(max_length=150,verbose_name="Created by",null=True,blank=True)
    
    class Meta:
        db_table = 'repair_payment'
        verbose_name = 'repair_payment'
        verbose_name_plural = 'repair_payment'

    def __str__(self) -> str:
        return self.repair_payment_id
    
class RepairPaymentDenominations(models.Model):
    
    repair_payment_details = models.ForeignKey(RepairPayment,verbose_name="Payment Details",on_delete=models.CASCADE)  
    payment_method = models.ForeignKey(PaymentMenthod,verbose_name="Payment Methods",default=1,on_delete=models.PROTECT)
    payment_providers = models.ForeignKey(PaymentProviders,verbose_name="Payment Providers",null=True,blank=True,on_delete=models.PROTECT)
    total_amount = models.FloatField(verbose_name="Total Amount",default=0.0)
    
    class Meta:
        db_table = 'repair_payment_denominations'
        verbose_name = 'repair_payment_denominations'
        verbose_name_plural = 'repair_payment_denominations'

    def __str__(self) -> str:
        return self.repair_payment_details.repair_payment_id
    
class RepairAdvanceDetails(models.Model):
    
    repair_payment_details = models.ForeignKey(RepairPayment,verbose_name="Payment Details",on_delete=models.CASCADE)
    advance_details = models.ForeignKey(AdvanceDetails,verbose_name="Advance Details",on_delete=models.PROTECT)
    redeem_weight = models.FloatField(verbose_name="Redeem Weight",default=0.0)
    redeem_metal_rate = models.FloatField(verbose_name="Redeem Metal Rate",default=0.0)
    redeem_metal_value = models.FloatField(verbose_name="Redeem Metal Value",default=0.0)
    redeem_amount = models.FloatField(verbose_name="Redeem Amount",default=0.0)
    total_amount = models.FloatField(verbose_name="Total Amount",default=0.0)
    
    class Meta:
        db_table = 'repair_advance_details'
        verbose_name = 'repair_advance_details'
        verbose_name_plural = 'repair_advance_details'
        
    def __str__(self) -> str:
        return self.repair_payment_details.repair_payment_id


