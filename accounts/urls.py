from django.conf.urls import url
from django.contrib.auth import views as auth_views
from accounts import views


urlpatterns = [
    url(r'^logout/$', auth_views.logout),
    url(r'^login/$', views.Login.as_view()),
    url(r'^register/$', views.Register.as_view()),
]
