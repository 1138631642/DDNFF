# encoding:utf8
from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
    """商品分类模型"""

    # 商品类名
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle.encode('utf8')


class GoodsInfo(models.Model):
    """商品模型"""

    # 商品名称
    gtitle = models.CharField(max_length=20)
    # 匹配图片 update_to:图片存储地址
    gpic = models.ImageField(upload_to='df_goods')
    # 商品价格 max_digits:总位数，decimal_places：保留几位
    gprice = models.DecimalField(max_digits=5,decimal_places=2)
    # 单位
    gunite = models.CharField(max_length=20)
    # 点击量(将来根据点击量，来判断该商品的人气)
    gclick = models.IntegerField()
    # 商品简介
    gjianjie = models.CharField(max_length=200)
    # 商品库存
    gkucun = models.IntegerField()
    # 详情介绍(使用富文本编辑器)
    gcontent = HTMLField()
    # 给这个商品创建一个外键，来指向商品类型
    gtype = models.ForeignKey(TypeInfo)
    # 推荐商品
    # gadv = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)