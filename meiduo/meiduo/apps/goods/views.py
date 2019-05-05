from django.shortcuts import render
from django.views import View
from django import http
from django.core.paginator import Paginator

from contents.utils import get_categories
from goods.models import GoodsCategory, SKU
from goods.utils import get_breadcrumb
from meiduo.utils.response_code import RETCODE
# Create your views here.

class ListView(View):
    """商品列表页"""

    def get(self, request, category_id, page_num):
        """提供商品列表页"""
        sort = request.GET.get("sort", "default")  # 获取排序参数
        categories = get_categories()  # 获取商品类别分类

        try:
            category = GoodsCategory.objects.get(id=category_id)  # 获取点击的3级数据对象
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseNotFound('GoodsCategory does not exist')

        breadcrumb = get_breadcrumb(category)  # 查询面包屑导航

        # 按照排序规则查询该分类商品SKU信息
        if sort == 'price':
            # 按照价格由低到高
            sort_field = 'price'
        elif sort == 'hot':
            # 按照销量由高到低
            sort_field = '-sales'
        else:
            sort_field = "-create_time"

        # 查询3级对象下的所有sku商品
        sku_qs = category.sku_set.filter(is_launched=True).order_by(sort_field)

        # 创建分页对象
        paginator = Paginator(sku_qs, 5)  # 分5页
        page_skus = paginator.page(page_num)  # 第几页对象
        total_page = paginator.num_pages  # 总页数


        # 拼接响应数据
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'category': category,
            'sort': sort,
            'total_page': total_page,
            'page_skus': page_skus,
            'page_num': page_num
        }
        return render(request, 'list.html', context)


class HotGoodsView(View):
    """商品热销排行"""

    def get(self, request, category_id):
        """提供商品热销排行JSON数据"""
        # 根据销量倒序
        skus = SKU.objects.filter(category_id=category_id).order_by("-sales")[:2]

        # 序列化
        hot_skus = []

        for sku in skus:
            hot_skus.append(
                {
                    'id': sku.id,
                    'default_image_url': sku.default_image.url,
                    'name': sku.name,
                    'price': sku.price
                }
            )

        return http.JsonResponse({'code':RETCODE.OK, 'errmsg':'OK', 'hot_skus':hot_skus})