from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class UserAccount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    balance = models.FloatField(default=0)
    last_balance_added = models.DateTimeField(blank=True,null=True)


    def __str__(self):
        return f'{self.user}'
