from django.conf.urls import url
from users import views

urlpatterns = [
            url('^register/$', views.RegisterView.as_view(), name="register"),
            url(r"^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$", views.UsernameCountView.as_view()),
        ]
