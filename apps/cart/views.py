from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views.decorators.http import require_POST

from apps.goods.models import Goods


class Cart(object):
    def __init__(self,request):
        self.request=request
        self.session=self.request.session
        cart=self.session.get(self.request.user.id)
        if not cart:
            cart=self.session[self.request.user.id]={}
        self.cart=cart

    def add(self,k,c):
        if k not in self.cart:
            self.cart[k]=c
        else:
            self.cart[k]+=c
        self.save()

    def update(self,k,c):
        self.cart[k] = c
        self.save()

    def remove(self,k):
        if k in self.cart:
            del self.cart[k]
            self.save()

    def save(self):
        self.session.modified=True








def add_cart(request):
    if request.method=='POST':
        response = JsonResponse({'res': 4})
        if request.user.is_authenticated:
            sku_id = request.POST.get('sku_id')
            count_good = int(request.POST.get('count'))
            cart = Cart(request)
            cart.add(sku_id,count_good)
            total_count=len(cart.cart)
            response=JsonResponse({'res':5,'total_count':total_count})
        return response

@require_POST
def remove_cart(request):
    id=request.POST.get('sku_id')
    Cart(request).remove(id)
    return JsonResponse({'res':3,'total_count':len(Cart(request).cart)})

@require_POST
def update_cart(request):
    id = request.POST.get('sku_id')
    c=request.POST.get('count')
    Cart(request).update(id,int(c))
    return JsonResponse({'res':5,'total_count': len(Cart(request).cart)})


@login_required
def owner_cart(request):
    cart_list=Cart(request).cart
    count=len(cart_list)
    item={}
    items={}
    cost=0
    for x in cart_list:
        good=Goods.objects.get(id=int(x))
        item[good]=cart_list[x]
        items[good]=float('{:.2f}'.format(cart_list[x]*good.price))
        cost+=cart_list[x]*good.price
    return render(request,'owner_cart.html',locals())

