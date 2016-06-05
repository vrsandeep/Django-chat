from django.conf import settings
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<room>[a-zA-Z]+)/$', views.ChatListView.as_view()),
]
if settings.DEBUG:
    urlpatterns.append( url(r'^render/(?P<room>[\w-]{,50})/$', views.chat_room, name='chat_room'))
