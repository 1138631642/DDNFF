# encoding=utf-8
from django.conf.urls import url
import views

urlpatterns = [


    # 商品列表页
    url(r'^list_(\d+)_(\d+)_(\d+)$',views.list),

    # 首页
    url(r'^$', views.index),
    url(r'^index$',views.index),
    # 商品详情页
    url(r'^detail_(\d+)$', views.detail),

    # 测试
    url(r'^getdate$',views.getdate),

    # 退出
    url(r'^layout$',views.layout)

]