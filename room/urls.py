from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<room>[a-zA-Z]+)/$', views.ChatListView.as_view()),
]
