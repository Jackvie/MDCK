from django.contrib.auth.backends import ModelBackend
import re
from users.models import User
from django.db import models

def get_user_by_count(account):
    """手机号或用户名返回user对象"""
    try:
        if re.match(r"^1[3-9]\d{9}$", account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """自定义认证类"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_count(username)
        if user and user.check_password(password):
            return user
