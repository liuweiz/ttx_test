from django.db import models
from db import BaseMode

# Create your models here.
class GoodsType(BaseMode):
    type=models.CharField('类别',max_length=100)
    image=models.ImageField('商品类别图片',upload_to='type')
    logo=models.CharField(max_length=10)

    def __str__(self):
        return self.type

    class Meta:
        db_table='df_goods_type'
        verbose_name = verbose_name_plural ='商品类别表'


class Goods(BaseMode):
    name=models.CharField(max_length=100)
    type=models.ForeignKey(GoodsType,on_delete=models.CASCADE)
    img=models.ImageField(upload_to='fruit')
    desc=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        db_table='df_goods'
        verbose_name = verbose_name_plural ='商品表'


class Banner(BaseMode):
    img=models.ImageField(upload_to='banner')
    index=models.PositiveIntegerField()

    class Meta:
        db_table='df_index_goodsbanner'
        verbose_name = verbose_name_plural ='轮播图'


class Index_activity(BaseMode):
    name=models.CharField('活动名称',max_length=100)
    url=models.URLField('活动链接')
    images=models.ImageField('活动图片',upload_to='banner')
    index=models.SmallIntegerField(default=0,verbose_name='展示顺序')

    class Meta:
        db_table='df_index_activity'
        verbose_name = verbose_name_plural ='活动表'












