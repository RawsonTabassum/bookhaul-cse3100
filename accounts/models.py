from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class my_account_manager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_no, password=None):
        if not email:
            raise ValueError('Email address is missing!')

        if not username:
            raise ValueError('Username is missing!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
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

        user.save(using=self.db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_no = models.CharField(max_length=11, unique=True)

    # required fields
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    objects = my_account_manager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    # address= models.CharField(blank=True, max_length=100)
    # profile_picture = models.ImageField(
    #     blank=True, upload_to='userprofile', null=True)
    city = models.CharField(blank=True, max_length=20)
    postcode = models.CharField(blank=True, max_length=20)
    upazilla = models.CharField(blank=True, max_length=20)
    zilla = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.city}, {self.upazilla}-{self.postcode}, {self.zilla}'
