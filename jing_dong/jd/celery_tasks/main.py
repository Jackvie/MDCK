from celery import Celery

import os


# 为celery使用django配置文件进行设置
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'jd.settings.dev'

app = Celery("JD")

app.config_from_object("celery_tasks.conf")

app.autodiscover_tasks(["celery_tasks.sms", "celery_tasks.email"])
