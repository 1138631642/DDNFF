# encoding=utf-8
from django.contrib import admin
from models import *


class TypeInfoAdmin(admin.ModelAdmin):
    """注册商品类型"""
    list_display = ['id','ttitle']


class GoodsInfoAdmin(admin.ModelAdmin):
    """注册商品"""
    list_per_page = 15
    list_display = ['id','gtitle',
                    'gprice','gunite',
                    'gclick','gkucun',
                    'gtype',]


admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)
