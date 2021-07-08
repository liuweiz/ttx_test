from django.db import models
from db import BaseMode
from apps.user.models import User
from apps.goods.models import Goods
# Create your models here.

class OrderInfo(BaseMode):
    pay_ways=(
        (1,'货到付款'),
        (2,'支付宝'),
        (3,'微信付款'),
        (4,'银联付款')
    )
    pay_status=(
        (1,'待支付'),
        (2,'待评价'),
        (3,'待发货'),
        (4,'待收货'),
        (5,'已完成'),
    )
    id=models.AutoField('订单id',primary_key=True)
    user=models.ForeignKey(User,verbose_name='用户',on_delete=models.CASCADE)
    pay_way=models.SmallIntegerField('支付方式',default=2,choices=pay_ways)
    count=models.IntegerField('商品总数')
    total=models.DecimalField('总价',decimal_places=2,max_digits=10)
    status=models.SmallIntegerField('状态',default=1,choices=pay_status)
    order_no=models.CharField('支付编号',max_length=100)

    class Meta:
        db_table='df_order_info'
        verbose_name = verbose_name_plural ='订单表'


class OrderGoods(BaseMode):
    order=models.ForeignKey(OrderInfo,on_delete=models.CASCADE,verbose_name='订单')
    sku=models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name='商品')
    count=models.IntegerField('商品数目')
    comment=models.TextField('评论')
    @property
    def price(self):
        return self.sku.price * self.count

    class Meta:
        db_table='df_order_goods'
        verbose_name = verbose_name_plural ='订单商品表'