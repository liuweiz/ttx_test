from django.urls import path
from .views import order_place,order_commit,pay,check

app_name='order'
urlpatterns=[
        path('place',order_place,name='order_place'),
        path('commit',order_commit,name='order_commit'),
        path('pay',pay,name='order_pay'),
        # path('check',check,name='order_check'),
        # path('res',pay,name='order_pay'),
]