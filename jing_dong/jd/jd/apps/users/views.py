from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import *
import re
from .models import User
from django.db import DatabaseError
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from jd.utils.response_code import RETCODE
from django_redis import get_redis_connection
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins
# Create your views here.

class RegisterView(View):
    """注册"""
    def get(self, request):
        """返回注册页面"""
        return render(request, "register.html")

    def post(self, request):
        """注册结果处理"""
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get('password2')
        mobile = request.POST.get("mobile")
        sms_code_cli = request.POST.get("sms_code")
        allow = request.POST.get("allow")

        # 判断参数是否齐全
        if not all([username, password, password2, mobile, allow, sms_code_cli]):
            return HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseForbidden('请输入正确的手机号码')

        # 判等短信验证码
        redis_conn = get_redis_connection("verify_code")
        sms_code_ser = redis_conn.get("sms_%s" % mobile).decode()
        if sms_code_ser is None:
            return render(request, 'register.html', {'sms_code_errmsg':'无效的短信验证码'})
        if sms_code_ser != sms_code_cli:
            return render(request, 'register.html', {'sms_code_errmsg': '输入短信验证码有误'})

        # 判断是否勾选用户协议
        if allow != 'on':
            return HttpResponseForbidden('请勾选用户协议')

        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            print("-----")
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        login(request,user)

        response = redirect(reverse("contents:index"))
        response.set_cookie("username", user.username, max_age=24 * 3600)
        return response


class UsernameCountView(View):
    """username重复校验"""
    def get(self, request, username):
        count = User.objects.filter(username__exact=username).count()
        return JsonResponse({"count":count, 'code': RETCODE.OK, 'errmsg': 'OK'})


class MobileCountView(View):
    """mobile重复校验"""
    def get(self, request, mobile):
        count = User.objects.filter(mobile__exact=mobile).count()
        return JsonResponse({"count":count, 'code': RETCODE.OK, 'errmsg': 'OK'})


class LoginView(View):
    """登录"""
    def get(self, request):
        """返回登录页面"""
        return  render(request, "login.html")

    def post(self, request):
        """登录结果处理"""
        username = request.POST.get("username")
        password = request.POST.get("password")
        remembered = request.POST.get("remembered")
        next = request.GET.get("next")

        if not all([username, password]):
            return render(request, "login.html", {"account_errmsg": "缺少必传参数"})

        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseForbidden('请输入正确的用户名或手机号')

        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('密码最少8位，最长20位')

        # if re.match(r"^1[3-9]\d{9}$", username):
        #     # 如果是手机格式，将属性username换位mobile
        #     User.USERNAME_FIELD = "mobile"

        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, "login.html", {"account_errmsg": "用户名或密码错误"})

        login(request, user)
        if remembered != "on":
            request.session.set_expiry(0)
        if next is None:
            response = redirect(reverse("contents:index"))
        else:
            response = redirect(next)

        response.set_cookie("username", user.username, max_age=24*3600)
        return response



class LogoutView(View):
    """退出登录"""
    def get(self, request):
        logout(request)
        response = redirect(reverse("users:login"))
        response.delete_cookie("username")
        return response


# class LoginRequiredMixin(object):
#     """验证登录扩展类"""
#     @classmethod
#     def as_view(cls, **initkwargs):
#         # 自定义的as_view()方法中，调用父类的as_view()方法
#         view = super().as_view(**initkwargs)
#         return login_required(view)


class UserInfoView(mixins.LoginRequiredMixin, View):
    """用户中心"""

    def get(self, request):
        """提供个人信息界面"""
        return render(request, 'user_center_info.html')




