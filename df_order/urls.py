# encoding=utf-8
from django.conf.urls import url
import views

urlpatterns = [

    # 购物车
    url(r'^cart_order$',views.cart_order),
    url(r'^cart_order2$',views.cart_order2),

    # 提交订单
    url(r'^order_hander/(\d+)/(\w+)$',views.order_hander),

    # 付款
    url(r'^pay_(\d+)$',views.pay)
]