# encoding:utf-8
from django.db import models


class OrderInfo(models.Model):
    """订单信息"""

    # 订单编号
    oid = models.CharField(max_length=20,primary_key=True)
    # 用户
    user = models.ForeignKey('df_user.UserInfo')
    # 商品订单时间，auto_now:表示一添加就是当前系统时间
    odate = models.DateTimeField(auto_now=True)
    # 是否支付
    oIsPay = models.BooleanField(default=False)
    # 总价钱
    ototal = models.DecimalField(max_digits=6,decimal_places=2)
    # 收货地址
    oaddress = models.CharField(max_length=100,default='')


class OrderDetailInfo(models.Model):

    """订单中单个商品的详情"""

    # 商品
    goods = models.ForeignKey('df_goods.GoodsInfo')
    # 那个订单
    order = models.ForeignKey(OrderInfo)
    # 价钱
    price = models.DecimalField(max_digits=6,decimal_places=2)
    # 数量
    count = models.IntegerField()

