from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserAccount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=20,blank=True,null=True)
    address = models.CharField(max_length=255,blank=True,null=True)


    def __str__(self):
        return f'{self.user}'
