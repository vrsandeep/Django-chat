from django.conf import settings
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<room>[a-zA-Z0-9]+)/$', views.ChatListView.as_view()),
    url(r'^render/(?P<room>[\w-]{,50})/$', views.chat_room, name='chat_room')
]
