# coding:utf8
from django.db import models

# 用户表
class UserInfo(models.Model):

    # 用户名
    uname = models.CharField(max_length=20)
    # 密码
    upwd = models.CharField(max_length=40)
    # email
    uemail = models.CharField(max_length=30)
    # 收件人
    ushou = models.CharField(max_length=20, default='')
    # 地址
    uaddress = models.CharField(max_length=100,default='')
    # 邮编
    uyoubina = models.CharField(max_length=6, default='')
    # 电话
    uphone = models.CharField(max_length=11, default='')
    # 软删除
    isDelete = models.BooleanField(default=False)


