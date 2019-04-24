from django.shortcuts import render
from django.views.generic import View
from django import http
from meiduo.utils.response_code import RETCODE
from meiduo.libs.yuntongxun.sms import CCP
import re,logging,random
from meiduo.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from . import constants

logger = logging.getLogger("django")

# Create your views here.

class ImageCountView(View):
    """生产图片验证码"""
    # /image_codes/" + this.uuid + "/"
    def get(self, request, uuid):
        name, text, image = captcha.generate_captcha()
        conn = get_redis_connection("verify_code")
        conn.setex("img_%s" % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        return http.HttpResponse(image, content_type="image/jpg")

class SMSCodeView(View):
    """发送短信"""
    # '/sms_codes/' + this.mobile + '/?image_code=' + this.image_code + '&uuid=' + this.uuid;
    def get(self, request, mobile):
        # 接收参数
        image_code_client = request.GET.get("image_code")
        uuid = request.GET.get("uuid")

        # 校验参数
        if not all([image_code_client, uuid]):
            return http.JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必传参数'})

        # 创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')
        # 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            # 图形验证码过期或者不存在
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码失效'})

        try:
            # 删除redis中的图片数据
            redis_conn.delete("img_%s", uuid)
        except Exception as e:
            logger.error(e)

        # 判等
        if image_code_server.decode('utf-8').lower() != image_code_client.lower():
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证码有误'})

        # 完成图片验证码校验成功，可以发送短信

        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '发送短信过于频繁'})

        # 生成短信验证码：生成6位数验证码
        sms_code = "%06d" % random.randint(0,999999)

        # 保存短信验证码
        redis_conn.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)

        # 重新写入send_flag
        redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 调用函数发送函数
        CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES], constants.SEND_SMS_TEMPLATE_ID)

        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})
