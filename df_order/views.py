# encoding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from df_user import user_decorator
from df_cart.models import *
from df_user.models import *
from django.db import transaction
from models import *
from datetime import datetime
from decimal import Decimal
from django.core.paginator import Paginator

@user_decorator.login
def cart_order(request):
    """订单信息"""

    # 获取用户选择购买商品的id
    data = request.GET
    cids = data.getlist('cids')

    # 将商品的id存储到session中
    request.session['cid']=cids
    cids2 = request.session['cid']

    return JsonResponse({'result':cids2})
    # return redirect('/index')


@user_decorator.login
def cart_order2(request):

    # 判断session中是否存储用户要打算购买商品的id
    if request.session.has_key('cid'):
        cids = request.session['cid']
        # 定义一个列表用来存储该商品对象
        carts = []
        for cartid in cids:
            cart = CartInfo.objects.filter(pk=int(cartid))
            carts.append(cart[0])
        # 获取一个用户，并将里面的地址取出来
        cart1 = CartInfo.objects.get(pk=int(cids[0]))
        user = UserInfo.objects.get(pk=cart1.user_id)
        address = user.uaddress
        context = {'carts':carts,'address':address}
    else:
        context = {'carts': '', 'address': ''}

    return render(request, 'df_order/place_order.html',context)


@transaction.atomic()
@user_decorator.login
def order_hander(request,total,address):
    """付账"""

    # 定义一个点，方便回滚找点
    tran_id = transaction.savepoint()

    # 从session中获取购物车中的所有商品的id
    cids = request.session['cid']

    # context = {'address':address}
    # return render(request,'getdate.html',context)

    try:
        # 创建订单对象
        order = OrderInfo()
        # 获取当前系统的时间
        now = datetime.now()
        # 获取用户的id
        uid = request.session['uid']
        # 编辑订单编号  20180116..-uid
        order.oid = '%s/%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(int(total))
        order.oaddress = address
        order.save()

        # 创建详单对象
        for id in cids:

            detail = OrderDetailInfo()
            detail.order = order
            # 根据购物车id获取购物车对象
            cart = CartInfo.objects.get(pk=int(id))
            good = cart.goods
            detail.count = cart.count
            detail.goods_id = cart.goods_id
            detail.price = good.gprice
            detail.save()

        transaction.savepoint_commit(tran_id)

    except Exception as result:

        # print('order fail：%s'% result.message)
        # 回滚到刚刚定义的点处
        transaction.savepoint_rollback(tran_id)

    return redirect('/order_1')


@user_decorator.login
def pay(request,oid):
    """付款"""

    oid = int(oid)
    detail = OrderDetailInfo.objects.get(pk=oid)

    order = OrderInfo.objects.get(pk=detail.order_id)
    order.oIsPay=1
    order.save()
    return redirect('/order_1')

    # context = {'oid':oid,'detail':detail}
    # return render(request,'getdate.html',context)
