from celery_tasks.main import celery_app
from django.conf import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo.settings.dev")
import django
django.setup()
from scripts.regenerate_detail_html import generate_static_sku_detail_html
from goods.models import SKU

# 异步生成详情静态页面
@celery_app.task(bind=True,name="generate_static_sku_detail_html")
def generate_detail_html(self):
    skus = SKU.objects.all()
    for sku in skus:
        generate_static_sku_detail_html(sku.id)
