# encoding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from models import *


def index(request):
    """首页"""

    # 从数据库中获取数据
    typelist = TypeInfo.objects.all()

    # 测试是否能从数据库中获取数据
    # context = {'list': typelist[0].goodsinfo_set.all()}
    # return render(request,'getdate.html',context)

    # 获取水果类型下的所有水果,先倒序排序，找出最近添加的前4条数据
    # 获取所有：typelist[0].goodsinfo_set.all()

    # 水果类
    type1 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    # 海鲜类
    type2 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    # 猪肉类
    type3 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    # 鸡蛋类
    type4 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    # 蔬菜类
    type5 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    # 速冻类
    type6 = typelist[5].goodsinfo_set.order_by('-id')[0:4]

    # 将数据传入到index页面
    context = {'type1':type1,'type2':type2,
               'type3':type3,'type4':type4,
               'type5':type5,'type6':type6}

    return render(request,'df_goods/index.html',context)


def list(request,tid,sort,pindex):
    """商品列表"""

    typeid = int(tid)
    # 根据typeid获取该商品类型对象
    typeinfo = TypeInfo.objects.get(pk=typeid)
    # 获取该商品类型下面最新添加的两条数据
    newTwos = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    # 根据用户选择排序的类型，获取该商品下所有的商品
    if sort == '1':
        goods = GoodsInfo.objects.filter(gtype_id=typeid).order_by('-id')
    elif sort == '2':
        goods = GoodsInfo.objects.filter(gtype_id=typeid).order_by('-gprice')
    else:
        goods = GoodsInfo.objects.filter(gtype_id=typeid).order_by('-gclick')
    # 获取指定页数的数据
    index = int(pindex)
    # 分页 每页两条数据
    paginator = Paginator(goods,2)
    # 获取指定页数下的数据
    page = paginator.page(index)

    context = {'newTwos':newTwos,'goods':goods,
               'sort':sort,'typeinfo':typeinfo,
               'page':page,'paginator':paginator,
               'pindex':index}
    return render(request,'df_goods/list.html',context)

    # 测试
    # page =paginator.page(1).object_list
    # index = paginator.page(1).number
    # context = {'newTwos':newTwos,'goods':goods}
    # return render(request,'getdate.html',context)


def detail(request,gid):
    """商品详情页"""

    # 获取商品id
    goodid = int(gid)
    # 获取指定商品
    good = GoodsInfo.objects.get(pk=goodid)
    # 用户每次请求看一次该商品，就让该商品的点击量加1
    good.gclick = good.gclick+1
    good.save()

    # 当用户点击详情的时候，将最近浏览的5个商品记录下来

    # 先从cookie中获取记录浏览的商品id，如果不存在就给''
    # goods_ids = request.COOKIES.get('goods_ids', '')
    goods_ids = request.session.get('goods_ids','')
    # goodid = '%d'%good.id
    goodid = str(gid)
    # 判断是否有记录，如果有就继续判断
    if goods_ids != '':
        # 拆分列表
        goods_ids1 = goods_ids.split(',')
        # 在判断，用户当前浏览的商品，这个列表中是否已经存在，
        # 如果存在就删除，重新添加到列表最前端
        if goods_ids1.count(goodid) >= 1:
            goods_ids1.remove(goodid)
        # 再将该商品添加到第一位
        goods_ids1.insert(0, goodid)
        # 判断列表中记录的商品数量是否超过了6条，如果超过了6条
        # 就删除最后一条
        if len(goods_ids1) >= 6:
            del goods_ids1[5]
        # 再使用','将列表重新拼接成字符串
        goods_ids = ','.join(goods_ids1)
    else:
        # 如果cookie中没有记录，则直接往里面添加就行
        goods_ids = goodid
    # 将浏览商品记录写入cookie
    request.session['goods_ids'] = goods_ids

    # 获取于该商品同类型的商品点击量最高的前2条数据
    newTwos = good.gtype.goodsinfo_set.order_by('-gclick')[0:2]

    context = {'good':good,'newTwos':newTwos}
    return render(request,'df_goods/detail.html',context)


def layout(request):
    """退出登入"""

    # 当用户点击退出的时候，将session中用户名和id清空就行
    request.session.flush()
    return redirect('/')


def getdate(request):
    """测试"""
    return render(request,'getdate.html')