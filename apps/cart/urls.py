from django.urls import path
from . import views

app_name='cart'
urlpatterns=[
        path('add',views.add_cart,name='add_cart'),
        path('',views.owner_cart,name='cart_list'),
        path('update',views.update_cart,name='cart_del'),
        path('delete',views.remove_cart,name='cart_update'),
]