from celery import Celery

import os


# 告诉celery去那里加载Django配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jd.settings.dev")

app = Celery("kkk")

app.config_from_object("celery_tasks.conf")

app.autodiscover_tasks(["celery_tasks.sms"])
