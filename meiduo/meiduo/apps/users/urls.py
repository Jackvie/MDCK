from django.conf.urls import url
from . import views

urlpatterns = [
        # 注册页面
        url(r"^register/$", views.RegisterView.as_view(), name="register"),
        # 用户名查重
        url(r"^usernames/(?P<username>[a-zA-Z0-9-_]{5,20})/count/$", views.UsernameCountView.as_view()),
        # 手机号查重
        url(r"^mobiles/(?P<mobile>1[345789]\d{9})/count/$", views.MobileCountView.as_view()),
    ]
