from django.db import models
from jd.utils.models import BaseModel
# Create your models here.


class OAuthQQUser(BaseModel):
    """QQ用户模型类"""
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)
    # 应用名.模型类
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name
