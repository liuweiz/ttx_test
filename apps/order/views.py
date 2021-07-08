import uuid

from alipay import AliPay
from django.http import JsonResponse, HttpResponse

from ttx import settings
from .models import OrderInfo,OrderGoods
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from apps.goods.models import Goods
from apps.user.models import Address
from django.views.decorators.http import require_POST
from apps.cart.views import Cart


@require_POST
def order_place(request):
    sku_ids=request.POST.getlist('sku_ids')
    addr=request.user.address_set.all()
    if not sku_ids:
        return redirect(reverse('cart:cart_list'))
    else:
        l=[]
        s=0
        t=0
        ids=''
        for id in sku_ids:
            if not ids:
                ids+=id
            else:
                ids+= ','+id
            goods=Goods.objects.get(pk=id)
            count=Cart(request).cart[id]
            s+=count
            goods.count=count
            cost=count*goods.price
            t+=cost
            goods.cost=cost
            l.append(goods)
        return render(request,'order_place.html',locals())


@require_POST
@transaction.atomic         #事务
def order_commit(request):
    addr_id=request.POST.get('addr_id')
    sku_ids=request.POST.get('sku_ids')
    ids=sku_ids.split(',')
    count=request.POST.get('count')
    cost=request.POST.get('cost')
    pay_method=int(request.POST.get('pay_method'))
    addr=Address.objects.get(pk=addr_id)
    order_no=str(uuid.uuid4().hex)
    save_id=transaction.savepoint()     #事务保存点
    try:
        order=OrderInfo.objects.create(user=request.user,pay_way=pay_method,count=count,total=cost,order_no=order_no)
        for id in ids:
            goods=Goods.objects.get(pk=id)
            num=Cart(request).cart[id]
            OrderGoods.objects.create(order=order,sku=goods,count=num,comment='好吃')
            Cart(request).remove(id)

    except:
        transaction.savepoint_rollback(save_id)         #回滚
        return JsonResponse({'res':3,'errmsg':'操作失败'})
    else:
        transaction.savepoint_commit(save_id)       #提交

    return JsonResponse({'res':'5'})


alipay = AliPay(
        appid='2021000116664162',
        app_notify_url=None,
        alipay_public_key_string = """-----BEGIN RSA PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs8E9YuWulkkzXMVtM98Uv6yIklqeA95QN8sQ/c5uDDQsSSZufXX/tFX3fGwEjbpKHe2+FT7upphJeDfiqFqTTD2ppl3hKoC9uHvWfLlUgEogKj5qIgIOJ02to99xKYQre6YpuYIMisI4NMCIGiCyjLLvk0Rbc74+1hyJWHq33NPFzTmtd6zVrOySpAKku8CkzsMtZq6766oro11x0gUiv8GPHh6JxBd8XEwCQ1Q/Vtn3fwmyD+Ec2lkwjLV9hvoxeZA+LVMTheTu0+bBTSgQ60A+vR9m4A3CL/uGziYef0wxJg73I8320c0bmd6eo0xy4OyTbmcv2NFqJOLUyN4EYwIDAQAB                                                                                                                
-----END RSA PUBLIC KEY-----""", # 支付宝公钥
        app_private_key_string ="""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAmogdR4awG13mhTngodsUAtNKWVUg/ySjJnv+c26L21ANJi2i8D29qt89aLqJCZeA4EDZn1B6p6gqJDnaiFDpizKJJjsFi+JwUCFCaylK4I7OPqNks/cd1whplEibACh5rLPL5/V5LbFLdRmKXSw5V5VNwkhsVZPBId/K/xuXBaL1fBqV0GDZWXeYZkkwr3siuCPk2gUoWO5qlwss6km5w8r3fZiOOylshs6+3RdFEbjQ6DXXgAVM9uq7AOZrJgqRZrmCKWCDI4tb3Ou9zFmXPdP+WUYgXQZ/9DmQjVpjGZcNAFdAkz7rTVTin6kOoKdyt78/Bq4cZxA35FXAJrxCoQIDAQABAoIBAFBhwSk1jGGP5JskUg6fULdvhNsXBwTw39Ti5qbQt/sqlsxnLLxewUwit2TEswfEQQtlcE4IpOSU+ubBGUWTIQiBDwpN5UKwVM+5nTz0y7gnUG0QvQ9H2cPC4nh5k/bvFuuY0tYjwBbehGuzD2AL4wAF797BoWiaZPnj2Un95f7Nxy0gBmfX84+fdiiccmfOP/w+tQTmjeLWPE3c6VplbQpWz6S64wGF5zeKyilN/HHA7cCg2AJc81oL+RJT60trgnFOKkLFcojX/mT0RcsmWTLhlfaz4mm/obIbJOiq7ct+U1MJQJKKhPE03n5axC6aRcwNNTkDxCRBo/NtlIrhaakCgYEA3yWVtl7UwY0JRNmkIaECDJCe1gHqOw9YGRzEkmALywUF3UDg6Q7lWmnm5Ibu5B9I24Onip13yUnle7xpkckotRh7+lYmhg1pT63R1za8/8Yp1HbhnR6lIITIxLr8F7S16EXfgzwDmPyV7bm5kk4G6YEVa4239+il6nyMcqgd6kcCgYEAsUhsEJoYlfZAWsm83xVv2fRI1kkJaKTEW7CbC/gdlfRIsx6lLHoDRd9uvcjbc/K2XyU3SkM5K18L7Bb1HA1s5KKVNxNYWO0Fl5lPnkl2xWLykG6v1wXVTyQ/tMyG8pkhQPQ6C1JAkSwZzyk90jEGqaMjeI93t+fheiOiIhne99cCgYEA3VlZ/dJptyjgxeQiNJ2S+8XFWUIDB9y7pgVsVEpjyFpOK+A8edKl3Z7pQ0050R3bVqxs2EpFVW0w7yHBkrR45dLIwFUO17CcA0bHvXT1273FJpVaTVHluLEeuk9E23sNar9M7M/uPaZoTq0JkEBICP5bshmdIJQtaMFtTBrJuecCgYA36UxTrBXG7eP7/hX4EW22QonaMyypeRWIiVlM3BKQoXtwKmETduOjXMUzS66SkeCcf0NBw5O7Lv22lsL09vL55KDEvvAlE5Oo7SwkEq1HsV4o2Q/R88ADdr40yjBhQJQxRRUtTuKYJl15bVtW+ClOxOnB8xVhxdrhx20x7hDY/wKBgQDAAOXOLDfRyTYdzj5xwOWqxoS3Wbv41+s4/BC6RkF470lH2zVgDpZoW5soc7TumxtkqSrRxBmUDOwIg0YncBAL96wPJypAldGNFN6SKhJekurfU1sv+fOJQO9VNRGDjPJ31D3sje1WEM+8MOaiUS+zHO/ywfBsi6goP4bXweUjhQ==
-----END RSA PRIVATE KEY-----""" ,  # 应用私钥
        sign_type='RSA2',
        debug = True # 默认是True代表测试环境，False代表正式环境

    )
def pay(request):
    if request.method=='POST':
        id=request.POST.get('order_id')
        order_number = OrderInfo.objects.get(id=id)
        order_number.status=3
        order_number.save()
        query_params = alipay.api_alipay_trade_page_pay(
            subject='商品购买',  # 商品的简单描述
            out_trade_no=order_number.order_no,  # 商品订单号
            total_amount=str(order_number.total),  # 交易金额(单位是元，保留两位小数)
            return_url='http://127.0.0.1:8000/',  # 支付成功之后跳转到的网页地址",
            notify_url='http://127.0.0.1:8000/order/check'  # 支付成功后，通知我们的地址，通知方式为post，
        )
        print(query_params)
        pay_url = 'https://openapi.alipaydev.com/gateway.do?{}'.format(query_params)

        # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
        # 支付默认网关 https://openapi.alipaydev.com/gateway.do

        return JsonResponse({'pay_url':pay_url,'res':3})  # 跳转到支付页面


def check(request):

    if request.method=='POST':
        body = request.body.decode()
        d = {x.split('=')[0]: x.split('=')[1] for x in body.split('&')}
        no=d.pop('out_trade_no')
        print(no)
        sign = d.pop('sign', None)  # 取出签名
        status = alipay.verify(d, sign)  # 验证签名并获取结果
        if status:
            order=OrderInfo.objects.filter(order_no=no).first()
            print(order)
            order.status=3
            order.save()
            return HttpResponse('success')  # 返回成功信息到支付宝服务器

def res(requeest):
    pass

