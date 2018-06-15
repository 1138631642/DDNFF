# encoding=utf-8

from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# 检测用户是否登入，没有登入就跳转到登入页面，如果登入了就返回
# 跳转到原路径上


def login(func):
    def login_func(request,*args,**kwargs):
        # 从session中获取用户id值，看用户是否登入，登入了直接
        # 让用户继续执行，没有登入则让该用户跳到登入页面
        if request.session.has_key('uid'):
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/login')
            # 将用户请求的地址保存到cookie中，作为url的值
            red.set_cookie('url',request.get_full_path())
            return red
    return login_func