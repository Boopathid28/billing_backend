from django.db import models
from accounts.models import *

    
class Department(models.Model):
    department_name = models.CharField(max_length=100, verbose_name="Department name", unique=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.SET_DEFAULT, default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'departments'
        verbose_name = 'department'
        verbose_name_plural = 'departments'

    def __str__(self) -> str:
        return self.department_name
    
class Designation(models.Model):
    designation_name = models.CharField(max_length=100, verbose_name="Designation name", unique=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.SET_DEFAULT, default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'designations'
        verbose_name = 'designation'
        verbose_name_plural = 'designations'

    def __str__(self) -> str:
        return self.designation_name
    

class Staff(models.Model):
 
    staff_id = models.CharField(max_length=100, verbose_name="Staff id,", unique=True)
    first_name = models.CharField(max_length=100, verbose_name="First Name", null=True, blank=True)
    last_name = models.CharField(max_length=100, verbose_name="Last Name", null=True, blank=True)
    email = models.EmailField(max_length=60,verbose_name='Email', null=True, blank=True, unique=True)
    phone = models.CharField(max_length=10, verbose_name='Phone no', null=True, blank=True, unique=True)
    city = models.CharField(max_length=100, verbose_name="City", null=True, blank=True)
    state = models.CharField(max_length=100, verbose_name="State", null=True, blank=True)
    country = models.CharField(max_length=100, verbose_name="Country", null=True, blank=True)
    address = models.CharField(max_length=500, verbose_name="Address", null=True, blank=True)
    pincode = models.CharField(max_length=10, verbose_name="Pincode", null=True, blank=True)
    aadhar_card = models.CharField(max_length=500, verbose_name="Aadhar card", null=True, blank=True)
    pan_card = models.CharField(max_length=500, verbose_name="Pan card", null=True, blank=True)
    user = models.CharField(max_length=50, verbose_name="User", null=True, blank=True)
    location= models.ForeignKey(Location, verbose_name="Location", on_delete=models.PROTECT)
    branch= models.ForeignKey(Branch, verbose_name="Branch", on_delete=models.PROTECT)
    department= models.ForeignKey(Department, verbose_name="Department", on_delete=models.PROTECT)
    designation= models.ForeignKey(Designation, verbose_name="Designation", on_delete=models.PROTECT)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name="Created By", on_delete=models.SET_DEFAULT, default=1)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True, blank=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True, blank=True)
 
    class Meta:
        db_table = 'staffs'
        verbose_name = 'staff'
        verbose_name_plural = 'staffs'
 
    def __str__(self) -> str:
        return self.staff_name