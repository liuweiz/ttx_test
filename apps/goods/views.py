from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Banner,Index_activity,GoodsType,Goods
# Create your views here.
from apps.cart.views import Cart
from django_redis import get_redis_connection


client=get_redis_connection('default')
def index(request):
    banner=Banner.objects.order_by('index')
    active=Index_activity.objects.order_by('index')
    Type=GoodsType.objects.all()
    count=len(Cart(request).cart)
    return render(request,'index.html',locals())

def goods_list(request,pk):
    Type=GoodsType.objects.all()
    kinds=GoodsType.objects.get(pk=pk)
    goods_list=kinds.goods_set.all()
    qs=request.GET.get('order_by','id')
    goods=kinds.goods_set.all().order_by(qs)
    paginator=Paginator(goods,4)
    page=int(request.GET.get('page','1'))
    if page>paginator.num_pages:
        page=paginator.num_pages
    elif page<1:
        page=1
    page_obj=paginator.page(page)
    count = len(Cart(request).cart)
    return render(request,'type_list.html',locals())

def goods(request,pk):
    good=Goods.objects.get(pk=pk)
    Type = GoodsType.objects.all()
    goods=Goods.objects.filter(type=good.type).all()[:2]
    count = len(Cart(request).cart)
    if request.user.is_authenticated:
        #添加用户浏览记录
        client.sadd(request.user.username,good.id)
    return render(request,'good.html',locals())

def search(request):
    Type = GoodsType.objects.all()
    fruit=request.GET.get('fruit')
    goods=Goods.objects.filter(name__contains=fruit).all()
    paginator = Paginator(goods, 6)
    page = int(request.GET.get('page', '1'))
    if page > paginator.num_pages:
        page = paginator.num_pages
    elif page < 1:
        page = 1
    page_obj = paginator.page(page)
    return render(request,'search.html',locals())

