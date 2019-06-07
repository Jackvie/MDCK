from django.shortcuts import render
from django.views import View
from datetime import time
from django.conf import settings

from contents.utils import get_categories, spike_expire_time
from contents.models import ContentCategory
from goods.models import SKU
# Create your views here.

class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        categories = get_categories()

        contents = {}  # 广告信息
        # 查询所有的广告的类别
        content_categories = ContentCategory.objects.all()

        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 渲染模板的上下文
        context = {
            'categories': categories,
            'contents': contents,
        }
        return render(request, 'index.html', context)


class SpikeView(View):
    """秒杀"""
    def get(self,request):
        skus = SKU.objects.filter(id__lte=8)
        spike_end = spike_expire_time(*settings.SPIKE_LIST)
        # spike_end = spike_expire_time(2019,6,8,0,0,0)

        # 已售=销量/(销量+库存) sku.saled_rate
        for sku in skus:
            saled_rate = int((sku.sales/(sku.stock+sku.sales))*100)
            if saled_rate == 100:
                sku.saled_rate = "已售完"
            else:
                sku.saled_rate = "已售出:{}%".format(saled_rate)

        context = {"skus": skus, "spike_end":int(spike_end)}
        return render(request, "spike.html", context)
