from django.conf.urls import url
from . import views

urlpatterns = [
        # 生成图片验证码
        url(r"^image_codes/(?P<uuid>[\w-]+)/$", views.ImageCodeView.as_view(), name="image_codes"),
        # 校验图片验证码并发送短信
        url(r"^sms_codes/(?P<mobile>1[345789]\d{9})/$", views.SMSCodeView.as_view(), name="sms_codes"),
]