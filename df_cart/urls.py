# encoding=utf-8

from django.conf.urls import url
import views

urlpatterns = [

    # 购物车
    url(r'^cart$',views.cart),

    # 添加商品
    url(r'^add_(\d+)_(\d+)$',views.add),

    # 删除购物车中的商品
    url(r'^delete_(\d+)$',views.delete),

    # 修改购物车中的信息
    url(r'^edit_(\d+)_(\d+)$',views.edit),

    # 请求购物车中商品的数量
    url(r'^cart_count$',views.cart_count)

    # url(r'^getdata$',views.ge)
]