from django.conf.urls import url

from carts import views

urlpatterns = [
    url(r'carts/$', views.CartsView.as_view()),        
]