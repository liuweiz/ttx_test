from django.contrib.auth import authenticate,logout, login as login_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from apps.goods.views import client
from apps.goods.models import Goods


from .models import User
import re
# Create your views here.

"""
实现用户注册登入功能模块
"""

#用户注册视图函数
def register(request):
    if request.method=='POST':
        name=request.POST.get('user_name')
        pwd=request.POST.get('pwd')
        cpwd=request.POST.get('cpwd')
        email=request.POST.get('email')
        allow=request.POST.get('allow')     #选中为on
        if not all((name,pwd,cpwd,email,allow)):
            return render(request,'register.html',{'errmsg':'信息不完整'})
        if pwd!=cpwd:
            return render(request,'register.html',{'errmsg':'密码不正确'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request,'register.html',{'errmsg':'邮箱格式不正确'})
        if allow != 'on':
            return render(request,'register.html',{'errmsg':'请同意协议'})
        try:
            User.objects.create(username=name,password=make_password(pwd),email=email)

        except Exception:
            return render(request, 'register.html', {'errmsg': '改用户名以被注册'})
        else:
            return redirect(reverse('user:login'))

    return render(request,'register.html')

#用户登入视图函数
def login(request):
    if request.method=='POST':
        name=request.POST.get('username')
        pwd=request.POST.get('pwd')
        next=request.POST.get('next')
        choice =request.POST.get('remember')
        if all((name,pwd)):
            user=authenticate(request,username=name,password=pwd)
            if user:
                res=redirect(next)
                if choice=='on':
                    #登入页面是否记住用户，设置永久不过期
                    res.set_cookie('username',name,max_age=10)
                else:
                    res.delete_cookie('username')
                login_user(request,user)    #设置用户session信息，可用request.user调用
                return res
            else:
                return render(request, 'login.html', {'erro':'用户名和密码不正确'})
        else:
            return render(request, 'login.html', {'erro':'请输入用户名和密码'})

    else:
        next=request.GET.get('next')
        if not next:
            next=reverse('goods:index')
        username=request.COOKIES.get('username',"")
        checked=''
        if username:
            checked='checked'
        return render(request,'login.html',{'username':username,'checked':checked,'next':next})

#用户退出登入视图函数
def logout_user(request):
    logout(request)
    return redirect(reverse('goods:index'))

# 忘记密码发送邮件视图函数
def forget(request):
    if request.method=='POST':
        email=request.POST.get('email')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request,'forget_password.html',{'err':'请输入正确邮箱'})
        user=User.objects.filter(email=email).first()
        if user:
            uid=urlsafe_base64_encode(force_bytes(user.id))
            send_mail('修改密码', render_to_string('pwd_change.html',{'uid':uid}),'111@111.com',[email])
            return render(request,'forget_password.html')
        return render(request,'forget_password.html',{'err':'此邮箱未注册账号'})



    return render(request,'forget_password.html')

#点击邮件链接修改密码视图函数
def change_pwd(request,uid):
    id=int(urlsafe_base64_decode(uid).decode())
    if request.method=='POST':
        name=request.POST.get('name')
        new=request.POST.get('new')
        user = User.objects.get(id=id)
        if name==user.username:
            user.password=make_password(new)
            user.save()
            return redirect(reverse('user:login'))
        return render(request, 'change.html',{'err':'用户名错误'})
    return render(request,'change.html')


def user_center(request):
    goods=client.smembers(request.user.username)
    li=[]
    for good in list(goods):
        li.append(Goods.objects.get(pk=int(good)))
    li=li[::-1][:4]
    return render(request,'user_center.html',{'page':'user','lit':li})

def address(request):
    addr = request.user.address_set.all()
    default_addr=None
    if addr:
        default_addr=request.user.address_set.get(is_default=True)
    if request.method=='POST':
        addrs=request.POST.get('address')
        addr.update(is_default=False)
        addressed=request.user.address_set.filter(addr=addrs).first()
        addressed.is_default=True
        addressed.save()

    return render(request,'address.html',{'page':'addr','addr':addr,'default_addr':default_addr})


def add_address(request):
    if request.method=='POST':
        addrs=request.user.address_set.all()
        receiver=request.POST.get('receiver')
        address=request.POST.get('addr')
        code=request.POST.get('zip_code')
        phone=request.POST.get('phone')
        if not addrs:
            request.user.address_set.create(user=request.user,receiver=receiver,addr=address,postcode=code,phone=phone)
        else:
            request.user.address_set.create(user=request.user, receiver=receiver, addr=address, postcode=code, phone=phone,is_default=False)
    return redirect(reverse('user:address'))

def user_order(request):
    user=request.user
    orders=user.orderinfo_set.all().order_by('id')
    paginator=Paginator(orders,1)
    page=int(request.GET.get('page',1))
    if page > paginator.num_pages:
        page = paginator.num_pages
    elif page < 1:
        page = 1
    page_obj = paginator.page(page)
    return render(request,'user_order.html',{'page':'order','li':orders,'obj':page_obj,'paginator':paginator})