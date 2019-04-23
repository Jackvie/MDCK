from django.conf.urls import url
from . import views

urlpatterns = [
    # 生产图片验证码
    url(r"^image_codes/(?P<uuid>[\w-]+)/$", views.ImageCountView.as_view()),
    # 发送短信 '/sms_codes/' + this.mobile + '/?image_code=' + this.image_code + '&uuid=' + this.uuid;
    url(r"^sms_codes/(?P<mobile>1[3-9]\d{9})/$", views.SMSCodeView.as_view()),
]