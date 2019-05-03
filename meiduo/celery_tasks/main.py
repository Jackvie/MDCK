from celery import Celery
import os


# 告诉celery去那里加载Django配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo.settings.dev")

# 创建celery实现
celery_app = Celery('meiduo')

# 加载celery配置
celery_app.config_from_object('celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])