from django.db import models

# Create your models here.
class Area(models.Model):
    """省市区模型类"""
    name = models.CharField(max_length=20, verbose_name="名称")
    # 父级查询子级数据 默认Area模型类对象.area_set
    # related_name = 'subs'
    # 现在Area模型类对象.subs语法
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subs", verbose_name='上级行政区划')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


