from celery import Celery

app = Celery(__name__)

app.config_from_object("celery_tasks.conf")

app.autodiscover_tasks(["celery_tasks.sms"])
