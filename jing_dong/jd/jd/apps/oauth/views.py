from django.shortcuts import render, redirect
from django.conf import settings
from django.http import *
from django.db import DatabaseError
from django.views.generic import View
from jd.utils.response_code import RETCODE
from .models import OAuthQQUser
from django.contrib.auth import login
from .utils import generate_eccess_token,check_access_token
import re
from django_redis import get_redis_connection
from users.models import User

# Create your views here.

from QQLoginTool.QQtool import OAuthQQ

class QQAuthURLView(View):
    """提供QQ登录页面网址
                https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=xxx&redirect_uri=xxx&state=xxx
            """
    def get(self, request):
        # qq/authorization/?next=' + next 前端获取登录链接的请求
        next = request.GET.get("next")
        # 创建对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET, redirect_uri=settings.QQ_REDIRECT_URI, state=next)
        # 返回登录链接
        login_url = oauth.get_qq_url()
        return JsonResponse({"login_url":login_url, "code":RETCODE.OK, "errmsg":"OK"})

class QQAuthUserView(View):
    """用户扫码后回调处理
    http://www.meiduo.site:8000/oauth_callback?code=7029A89D5F0E4C76A8764FC06ED3E201&state=%2F"""
    def get(self, request):
        code = request.GET.get("code")
        next = request.GET.get("state", "/contents/")
        print(next,"111")

        # 获取openid 唯一标识qq用户
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET, redirect_uri=settings.QQ_REDIRECT_URI, state=next)
        access_token = oauth.get_access_token(code)
        openid = oauth.get_open_id(access_token)

        try:
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # QQ第一次登录未绑定美多用户
            openid = generate_eccess_token(openid)
            context = {'openid': openid}
            return render(request, 'oauth_callback.html', context)
        else:
            # qq用户绑定了美多用户
            user = oauth_user.user
            # 状态保持
            login(request, user)
            # 设置cookie
            response = redirect(next)
            response.set_cookie("username", user.username, max_age=60*60)

            return response

    def post(self, request):
        """美多商城用户绑定到openid"""
        # 接收参数
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        openid = request.POST.get("openid")
        sms_code_client = request.POST.get("sms_code")

        # 校验参数
        # 判断参数是否齐全
        if not all([mobile, password, sms_code_client]):
            return HttpResponseForbidden('缺少必传参数')

        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseForbidden('请输入正确的手机号码')

        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('请输入8-20位的密码')

        redis_conn = get_redis_connection("verify_code")
        sms_code_server = redis_conn.get("sms_%s" % mobile)

        if sms_code_server is None:
            return render(request, 'oauth_callback.html', {'sms_code_errmsg': '无效的短信验证码'})

        if sms_code_client != sms_code_server.decode():
            return render(request, 'oauth_callback.html', {'sms_code_errmsg': '输入短信验证码有误'})

        # 判断openid是否有效：错误提示放在sms_code_errmsg位置
        openid = check_access_token(openid)
        if not openid:
            return render(request, 'oauth_callback.html', {'openid_errmsg': '无效的openid'})

        # 保存注册数据
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 用户不存在,新建用户
            user = User.objects.create_user(username=mobile, password=password, mobile=mobile)
        else:
            # 如果用户存在，检查用户密码
            if not user.check_password(password):
                return render(request, 'oauth_callback.html', {'account_errmsg': '用户名或密码错误'})

        # 将用户绑定openid
        try:
            print(openid)
            OAuthQQUser.objects.create(openid=openid, user=user)
        except DatabaseError:
            return render(request, 'oauth_callback.html', {'qq_login_errmsg': 'QQ登录失败'})

        # 实现状态保持
        login(request, user)

        # 响应绑定结果
        next = request.GET.get('state', "/contents/")
        print(next, "222")
        response = redirect(next)

        # 登录时用户名写入到cookie，有效期15天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        return response

