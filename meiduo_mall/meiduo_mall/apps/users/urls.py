from django.conf.urls import url
from users import views

urlpatterns = [
            url('^register/$', views.RegisterView.as_view(), name="register"),
        ]
