# coding:utf8
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from hashlib import sha1
from models import *
from . import user_decorator
from df_goods.models import *
from df_order.models import *
from django.core.paginator import Paginator

def register(request):
    # 注册显示
    context = {'title':'注册'}
    return render(request,'df_user/register.html',context)


def register_hander(request):
    # 注册验证

    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    # 判断该用户是否已近注册过
    user = UserInfo.objects.filter(uname=uname)
    if user.count() > 0:
        return HttpResponse('<script>alert("该用户已经注册过了！");window.location="/register"</script>')
    # 判断用户两次输如的密码是否一致
    if upwd != upwd2:
        return HttpResponse('<script>alert("两次输入的密码不一致！");window.location="/register"</script>')

    # 对用户进行加密
    s = sha1()
    s.update(upwd)
    pwd3 = s.hexdigest()

    # 将该用户保存到数据库
    user = UserInfo()
    user.uname = uname
    user.upwd = pwd3
    user.uemail = uemail
    user.save()

    return render(request,'df_user/login.html')


def login(request):
    # 显示用户登入界面

    context = {'title':'登入'}
    return render(request,'df_user/login.html',context)


def login_hander(request):
    # 验证用户登入

    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    ujizhu = post.get('jizhu',0)

    # 从数据库查找该用户，看该用户是否存在
    user = UserInfo.objects.filter(uname=uname)
    if user.count() <= 0:
        return HttpResponse('<script>alert("该用户不存在！");window.location="/login"</script>')

    # 对用户填入的密码进行加密，判断该用户输入的密码是否正确
    s = sha1()
    s.update(upwd)
    upwd2 = s.hexdigest()

    if upwd2 != user[0].upwd:
        return HttpResponse('<script>alert("密码不正确！！");window.location="/login"</script>')

    # 从cookie中获取url值，如果 有则返回cookie中的值，
    # 没有则反会当前路径,方便用户登入成功后跳回原来页面
    url = request.COOKIES.get('url','/')
    red = HttpResponseRedirect(url)
    # 判断该用户是否勾选记住密码
    if ujizhu == '1':
        # 将该用户的信息存储到cookie中

        red.set_cookie('uname',uname)
    else:
        # 不记录该用户的信息，如果记录了就要删除
        red.set_cookie('uname','',max_age=-1)

    # 将登入成功的用户id记录到session中
    request.session['uid'] = user[0].id
    request.session['user_name'] = uname
    context = {'title':'用户中心'}
    # return HttpResponse(request.session['uid'])
    return redirect('/info',context)


@user_decorator.login
def info(request):
    # 用户信息

    # 判断该id是否存在
    if request.session.has_key('uid'):
        # 从session中获取登入进来的用户id
        uid = request.session['uid']
        # 用数据库中获取该用户的信息
        user = UserInfo.objects.get(pk=uid)
        uname = user.uname
        uphone = user.uphone
        uaddress = user.uaddress

        # 从cookie中读取该用户的浏览记录
        if request.session.has_key('goods_ids'):
            goods_ids = request.session.get('goods_ids','')
            goods_ids1 = goods_ids.split(',')
            # 创建一个列表，用来添加用户浏览的商品
            good_list = []
            for goods_id in goods_ids1:
                # good_list.append(GoodsInfo.objects.filter(id=int(goods_id))[0])
                good_list.append(GoodsInfo.objects.get(id=int(goods_id)))
        else:
            good_list=''

        context = {'title':'个人中心',
                   'uname':uname,
                   'uphone':uphone,
                   'uaddress':uaddress,
                   'good_list':good_list}
    else:
        context = {'title': '个人中心',
                   'uname': '',
                   'uphone': '',
                   'uaddress': '',
                   'good_list':''
                   }
    return render(request,'df_user/user_center_info.html',context)


@user_decorator.login
def order(request,index):
    # 用户订单

    uid = request.session['uid']
    orders = OrderInfo.objects.filter(user_id=int(uid))
    details = []
    for order in orders:
        detail = OrderDetailInfo.objects.filter(order_id=order.oid)
        details.append(detail)

    index = int(index)
    # 分页 每页两条数据
    paginator = Paginator(orders, 2)
    # 获取指定页数下的数据
    page = paginator.page(index)

    context = {'details':details,'orders':orders,
               'page':page,'paginator':paginator,
               'index':index}
    # return render(request,'getdate.html',context)
    return render(request,'df_user/user_center_order.html',context)


@user_decorator.login
def site(request):
    # 地址

    # 判断session中是否有用户id
    if request.session.has_key('uid'):
        # 获取该用户的id
        uid = request.session['uid']
        user = UserInfo.objects.get(pk=uid)

    context = {'title':'用户中心','user':user}
    # return render(request,'getdate.html',context)
    return render(request,'df_user/user_center_site.html',context)


def site_hander(request,uid):
    # 修改用户收货信息

    user = UserInfo.objects.get(pk=uid)
    post = request.POST
    user.ushou = post.get('ushou')
    user.uaddress = post.get('uaddress')
    user.uyoubina = post.get('uyoubina')
    user.uphone = post.get('uphone')
    user.save()

    context = {'title':'个人中心'}
    # return redirect('/site',context)
    return redirect('/cart_order2',context)

def getdate(request):

    # 从cookie中读取该用户的浏览记录
    goods_ids = request.COOKIES.get('goods_ids', '23131')
    #goods_ids1 = goods_ids.split(',')
    # 创建一个列表，用来添加用户浏览的商品
    # good_list = []
    # print(goods_ids)
    # for goods_id in goods_ids:
    #     good_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context = {'list':goods_ids}
    return render(request,'base_head.html',context)
