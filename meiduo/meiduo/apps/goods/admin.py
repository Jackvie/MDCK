from django.contrib import admin

from goods.models import SKU,SPU

# Register your models here.
class SKUAdmin(admin.ModelAdmin):
    """SKU更新或保存时"""
    def save_model(self, request, obj, form, change):
        super().save_model(request,obj,form,change)
        from celery_tasks.detail.tasks import generate_detail_html
        generate_detail_html.delay()  # 异步生成详情静态文件

    def delete_model(self, request, obj):
        super().delete_model(request,obj)
        from celery_tasks.detail.tasks import generate_detail_html
        generate_detail_html.delay()

admin.site.register(SKU, SKUAdmin)
admin.site.register(SPU)
