from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name,username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    
    # Fields
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=180, unique=True)
    phone_number = models.CharField(max_length=10)
    
    Doctor = 1
    Customer = 2
    ROLE_CHOICE = (
        (Doctor, 'Doctor'),
        (Customer, 'Customer'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, default=Customer)  # Thiết lập giá trị mặc định
    
    
    
    # Required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)  # Updated when the user logs in
    create_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Đặt mặc định thành True
    is_superadmin = models.BooleanField(default=False)

    # Django settings
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name']

    
    objects = UserManager()

    def full_name(self):
        return f'{self.first_name}{self.last_name}'
    def __str__(self):
        return self.email
    
    # Permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True

class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)    
    address = models.CharField(blank=True, max_length=50)
    photo = models.ImageField(blank=True, upload_to='uploads/photos/')
    country = models.CharField(null=True, blank=True, max_length=20)
    city = models.CharField(null=True, blank=True, max_length=20)


    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return self.address 