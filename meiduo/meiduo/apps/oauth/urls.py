from django.conf.urls import url

from oauth import views

urlpatterns = [
    # 获取QQ登录链接
    url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
    # QQ扫码登录后的回调
    url(r'^oauth_callback$', views.QQAuthUserView.as_view()),
]