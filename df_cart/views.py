# encoding=utf-8
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from df_user import user_decorator
from models import *


@user_decorator.login
def cart(request):
    """购物车"""

    # 从session中获取用户的id
    uid = request.session['uid']
    # 获取该用户购物车信息
    carts = CartInfo.objects.filter(user_id=int(uid))
    context = {'carts':carts,'carts_len':carts.count()}
    return render(request,'df_cart/cart.html',context)


@user_decorator.login
def add(request,gid,count):
    """加入购物车"""

    # 获取用户id，商品id，购买该商品的数量
    uid = request.session['uid']
    gid = int(gid)
    count = int(count)

    carts = CartInfo.objects.filter(user_id=int(uid),goods_id=gid)
    # 判断该用户是否已经再购物车中添加此商品
    if len(carts)>=1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.count = count
        cart.goods_id = gid
        cart.user_id = uid

    cart.save()

    # 查询该用户现在再购物车中一共添加了多少商品
    count = CartInfo.objects.filter(user_id=uid).count()

    return JsonResponse({'result':'添加成功','count':count})
    # context = {'result':'ok'}
    # return render(request,'getdate.html',context)


@user_decorator.login
def delete(request,cid):
    """删除购物车中的商品"""

    cid = int(cid)
    CartInfo.objects.get(pk=cid).delete()

    return JsonResponse({'result':'删除成功'})


@user_decorator.login
def edit(request,cid,count):
    """修改购物车中的商品信息"""

    cid = int(cid)
    count = int(count)

    cart = CartInfo.objects.get(pk=cid)
    cart.count = count
    cart.save()

    return JsonResponse({'result':'修改成功'})


@user_decorator.login
def cart_count(request):
    """获取该用户购物车中的商品数量"""

    uid = request.session['uid']
    uid = int(uid)
    count = CartInfo.objects.filter(user_id=uid).count()
    return JsonResponse({'count':count})


def getajax(request,gid,count):

    # return HttpResponse(gid+"|"+count)
    return JsonResponse({'result':gid+"|"+count})
def getajax2(request):

    # return HttpResponse('ajax')
    return JsonResponse({'result':'tianjiachengggong'})
