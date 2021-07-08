from django.db import models
from db import BaseMode
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser,BaseMode):

    def __str__(self):
        return self.username

    class Meta:
        db_table='df_user'
        verbose_name=verbose_name_plural='用户表'

class Address(BaseMode):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='所属用户')
    receiver=models.CharField('收件人',max_length=100)
    addr=models.CharField('地址',max_length=100)
    postcode=models.CharField('邮编',max_length=100)
    phone=models.CharField('号码',max_length=11)
    is_default=models.BooleanField(default=True,verbose_name='是否默认地址')

    def __str__(self):
        return self.receiver

    class Meta:
        db_table='df_address'
        verbose_name = verbose_name_plural ='地址表'




