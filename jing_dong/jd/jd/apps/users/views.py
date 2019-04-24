from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import *
import re
from .models import User
from django.db import DatabaseError
from django.contrib.auth import login
from django.urls import reverse
from jd.utils.response_code import *
from django_redis import get_redis_connection
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

        return redirect(reverse("contents:index"))

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

