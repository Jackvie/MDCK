from django.conf.urls import url

from orders import views

urlpatterns = [
    # 结算订单
    url(r'orders/settlement/$', views.OrderSettlementView.as_view()),
]
