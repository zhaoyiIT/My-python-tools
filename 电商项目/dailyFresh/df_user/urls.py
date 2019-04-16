from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^register/$',views.register),  # 跳转到注册页面
    url(r'^register_handle/$',views.register_handle),  # 注册方法
    url(r'^register_exist/$',views.register_exist),  # 验证用户名是否存在
    url(r'^login/$',views.login),    #跳转到用户登录页面
    url(r'^login_handle/$',views.login_handle),  # 用户登录方法
    url(r'^info/$',views.toUserInfo),  # 跳转到用户中心界面
    url(r'^order/$',views.turnToOrder),  # 跳转到 用户中心->全部订单页面
    url(r'^site/$',views.turnToSite)  # 跳转到 用户中心->收货地址页面
]