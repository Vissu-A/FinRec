'''
This is userapi models module.
'''

import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from storages.backends.s3boto3 import S3Boto3Storage

# Create your models here.

class FinRecUserManager(BaseUserManager):
    '''
    This is the manager class for MyUser model.
    '''
    def create_user(self, email, password, username, **extra_fields):
        """
        Create and save a User with the given email, fullname, and password.
        """
        if not email:
            raise ValueError('The user must have an email')

        if not password:
            raise ValueError('The user must have a password')

        if not username:
            raise ValueError('The user must have a user name')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username, **extra_fields):
        """
        Create and save a SuperUser with the given email, fullname, and password.
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, username, **extra_fields)

class FinRecUser(AbstractBaseUser, PermissionsMixin):
    '''
    Class for custom user model.
    password field supplied by AbstractBaseUser
    last_login field supplied by AbstractBaseUser
    is_superuser field provided by PermissionsMixin if we use PermissionsMixin
    groups field provided by PermissionsMixin if we use PermissionsMixin
    user_permissions field provided by PermissionsMixin if we use PermissionsMixin
    '''
    USERNAME_FIELD = 'email'

    # while creating superuser from command it will ask these fields to enter value.
    REQUIRED_FIELDS = ['username']

    # this is returned when we call get_email_field_name() method.
    EMAIL_FIELD = 'email'

    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    email_verified = models.BooleanField(verbose_name='Email Verified', default=False)

    img = models.ImageField(
        blank=True,
        null=True,
        storage=S3Boto3Storage(
            bucket_name='finrec',
            region_name='us-east-2'
        ),
        upload_to='user/profile'
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active.\
            Unselect this instead of deleting accounts.',
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )
    date_joined = models.DateTimeField(help_text='date joined', default=timezone.now)

    objects = FinRecUserManager()

    def __str__(self):
        email = f'{self.email}'
        return email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm_list, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        '''
        This is the meta class for MyUser Model.
        '''
        ordering = ['-email',]
    