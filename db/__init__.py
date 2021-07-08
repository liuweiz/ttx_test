from django.db import models


class BaseMode(models.Model):
    create=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update=models.DateTimeField(auto_now=True,verbose_name='更新时间')
    is_delete=models.BooleanField(default=False,verbose_name='是否删除')

    class Meta:
        abstract=True