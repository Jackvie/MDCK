from django.shortcuts import render
from django.views.generic import View
from jd.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from . import constants
from django.http import HttpResponse,JsonResponse
from jd.utils.response_code import RETCODE
import re,logging,random
from jd.libs.yuntongxun.sms import CCP

logger = logging.getLogger("django")

# Create your views here.

class ImageCodeView(View):
    """生产图片验证码"""
    def get(self, request, uuid):
        # "image_codes/" + this.uuid + "/"
        name, text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection("verify_code")
        p = redis_conn.pipeline()
        p.setex("img_%s" % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        p.execute()
        return HttpResponse(image, content_type="image/jpg")

class SMSCodeView(View):
    """短信验证码"""
    def get(self, request, mobile):
        """校验图片验证码,发送短信"""
        # 接受参数
        image_code_cli = request.GET.get("image_code")
        uuid = request.GET.get("uuid")

        if not all([image_code_cli, uuid]):
            return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必传参数'})

        # 链接redis２号库
        redis_conn = get_redis_connection("verify_code")
        image_code_ser = redis_conn.get("img_%s" % uuid).decode()
        if image_code_ser is None:
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码失效'})
        # 图片验证码存在，删除图片数据
        try:
            redis_conn.delete("img_%s" % uuid)
        except Exception as e:
            logger.error(e)

        # 判等
        if image_code_cli.lower() != image_code_ser.lower():
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证码有误'})

        # 图片验证码校验成功可以发送短信

        # 校验是否已经发送多短信
        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:
            return JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '发送短信过于频繁'})

        # 短信验证码存于２号库
        sms_code = random.randint(0, 999999)
        p = redis_conn.pipeline()
        p.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        p.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        p.execute()
        # 发送
        CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES], constants.SEND_SMS_TEMPLATE_ID)

        return JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})

