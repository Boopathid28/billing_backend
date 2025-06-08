from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

    
class Location(models.Model):
    location_name = models.CharField(max_length=100, verbose_name="Location name", unique=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'locations'
        verbose_name = 'location'
        verbose_name_plural = 'locations'

    def __str__(self) -> str:
        return self.location_name    

class Branch(models.Model):
    branch_name = models.CharField(max_length=100, verbose_name="Branch name", unique=True)
    location = models.ForeignKey(Location, verbose_name="Location", on_delete=models.PROTECT)
    branch_shortcode = models.CharField(max_length=50,verbose_name="branch short code",null=True,blank=True)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    created_at = models.DateTimeField(verbose_name="Created at", null=True)
    created_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True)

    class Meta:
        db_table = 'branches'
        verbose_name = 'branch'
        verbose_name_plural = 'branches'

    def __str__(self) -> str:
        return self.branch_name
class UserRole(models.Model):

    role_name = models.CharField(max_length=50, verbose_name='Role name', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Status')
    is_admin = models.BooleanField( verbose_name='Admin Status',default=False)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name='Modified at', null=True, blank=True)

    class Meta:
        db_table = 'user_roles'
        verbose_name = 'user_role'
        verbose_name_plural = 'user_roles'

    def __str__(self) -> str:
        return self.role_name
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, phone):
        if not email:
            raise ValueError('Email is required!')
        if not password:
            raise ValueError('Password is required')
        
        user = self.model(
            email = self.normalize_email(email)
        )
        user.is_staff = True
        user.phone = phone
        user.set_password(password)
        user.save(self._db)
        return user
    
    def create_superuser(self, email, password, phone):
        if not email:
            raise ValueError('Email is required!')
        if not password:
            raise ValueError('Password is required')
        
        user = self.model(
            email = self.normalize_email(email)
        )
        user.is_staff = True
        user.is_superuser = True
        user.phone = phone
        user.set_password(password)
        user.save(self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(max_length=60,verbose_name='Email', unique=True)
    phone = models.CharField(max_length=10, verbose_name='Phone no', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_loggedin = models.BooleanField(default=False, verbose_name='Logged in')
    last_login = models.DateTimeField(verbose_name='Last Login', null=True, blank=True)
    is_superuser = models.BooleanField(verbose_name='Django user', default=False)
    is_staff = models.BooleanField(verbose_name='Employee', default=True)
    is_deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=True)
    created_by = models.CharField(max_length=50, verbose_name='Created By', null=True, blank=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", null=True, blank=True)
    modified_by = models.CharField(max_length=50, verbose_name="Modified By", null=True, blank=True)
    deleted_at = models.DateTimeField(verbose_name="Deleted at", null=True, blank=True)
    deleted_by = models.CharField(max_length=50, verbose_name="Deleted By", null=True, blank=True)
    role = models.ForeignKey(UserRole, verbose_name='User Role', on_delete=models.PROTECT, null=True, blank=True)
    branch = models.ForeignKey(Branch, verbose_name='User Branch', on_delete=models.PROTECT, null=True, blank=True)

 
    USERNAME_FIELD = 'email'
 
    REQUIRED_FIELDS = ['phone',]
 
    object = CustomUserManager()
 
    class Meta:
        db_table="users"
        verbose_name = 'user'
        verbose_name_plural = 'users'
 
    def __str__(self) -> str:
        return self.email
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True