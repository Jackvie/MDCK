from django.conf.urls import url
from . import views

urlpatterns = [
    # qq/authorization/?next=' + next

    url(r'^qq/authorization/$', views.QQAuthURLView.as_view(), name="authorization"),
    url(r"^oauth_callback/$", views.QQAuthUserView.as_view(), name="callback"),
]