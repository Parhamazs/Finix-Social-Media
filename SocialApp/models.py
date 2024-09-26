from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(null=True,blank=True, verbose_name='بایو کاربر')
    photo = models.ImageField(blank=False,null=False, upload_to="account_images/",verbose_name='تصویر کاربری')
    phone = models.CharField(max_length=12)
    birthday = models.DateField(null=True,blank=True,verbose_name='تاریخ تولد')
