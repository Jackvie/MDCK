from celery_tasks.sms.yuntongxun.sms import CCP
from celery_tasks.sms import constants
from celery_tasks.main import app
import logging,time

logger = logging.getLogger('django')


@app.task(bind=True, name="sccp_send_sms_code", retry_backoff=3)
def ccp_send_sms_code(self, mobile, sms_code):

    try:
        result = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES], constants.SEND_SMS_TEMPLATE_ID)
    except Exception as e:
        logger.error(e)
        raise self.retry(exc=e, max_retries=3)

    if result != 0:
        # 有异常自动重试三次
        raise self.retry(exc=Exception('发送短信失败'), max_retries=3)

    return result