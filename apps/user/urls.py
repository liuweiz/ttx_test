from django.urls import path
from . import views
app_name='user'
urlpatterns=[
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('forget_password/',views.forget,name='forget_pwd'),
    path('change_password/<uid>/',views.change_pwd,name='pwd_change'),
    path('user_center/',views.user_center,name='user_center'),
    path('address/',views.address,name='address'),
    path('order/',views.user_order,name='user_order'),
    path('add_address/',views.add_address,name='add_addr')
]