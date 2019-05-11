from django.shortcuts import render
from django.views.generic import View
from django_redis import get_redis_connection
from decimal import Decimal

from meiduo.utils.view import LoginRequiredMixin
from goods.models import SKU
from users.models import Address

# Create your views here.

class OrderSettlementView(LoginRequiredMixin, View):
    """结算订单"""
    def get(self, request):
        """提供订单结算页面"""

        # 获取登录用户
        user = request.user
        # 获取用户地址
        try:
            addresses = Address.objects.filter(user=user, is_deleted=False)
        except Address.DoesNotExist:
            # 如果地址为空，渲染模板时会判断，并跳转到地址编辑页面
            addresses = None
        # 从Redis购物车中查询出被勾选的商品信息
        # redis_conn = get_redis_connection('carts')
        # redis_cart = redis_conn.hgetall("carts_%s" % user.id)
        # cart_selected = redis_conn.smembers("selected_%s" % user.id)
        pl = get_redis_connection('carts').pipeline()
        pl.hgetall("carts_%s" % user.id)
        pl.smembers("selected_%s" % user.id)
        ret_list = pl.execute()
        redis_cart = ret_list[0]
        cart_selected = ret_list[1]

        cart_dict = dict()
        for sku_id in cart_selected:
            cart_dict[int(sku_id)] = int(redis_cart[sku_id])

        total_count = 0
        total_amount = Decimal("8.00")
        
        # 查询商品信息
        skus = SKU.objects.filter(id__in=cart_dict.keys())
        for sku in skus:
            sku.count = cart_dict[sku.id]
            sku.amount = sku.price * sku.count
            total_count += sku.count
            total_amount += sku.amount

        # 补充运费
        freight = Decimal('10.00')


        # 渲染界面
        context = {
            'addresses': addresses,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'freight': freight,
            'payment_amount':total_amount + freight
        }
        return render(request, "place_order.html", context)
