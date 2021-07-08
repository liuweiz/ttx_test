from django.urls import path
from . import views


app_name='goods'
urlpatterns=[
    path('',views.index,name='index'),
    path('type/<int:pk>/',views.goods_list,name='type_list'),
    path('goods/<int:pk>/',views.goods,name='goods'),
    path('search',views.search,name='search')
]