# encoding:utf-8
from django.conf.urls import url
import views
urlpatterns = [

    # 注册
    url(r'^register$', views.register),
    url(r'^register_hander$',views.register_hander),

    # 测试
    # url(r'^getdate$', views.getdate),

    # 登入
    url(r'^login$', views.login),
    url(r'^login_hander$',views.login_hander),

    # 用户信息
    url(r'^info$', views.info),
    url(r'^order_(\d+)$',views.order),
    url(r'^site$',views.site),
    url(r'^site_hander/(\d+)$',views.site_hander)

]