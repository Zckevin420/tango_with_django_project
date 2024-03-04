from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

# Create your models here.
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        #extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
class Users(AbstractBaseUser):
    userid = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    # password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    usertype = models.IntegerField(default=1, null=False)
    is_superuser = models.BooleanField(default=False)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    #last_login = models.DateTimeField('last login', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'

class Items(models.Model):
    itemid = models.BigAutoField(primary_key=True)
    itemname = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'items'




