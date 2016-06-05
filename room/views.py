from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, generics, status

from .models import Chat
from accounts.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Chat


class ChatAddSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Chat


class ChatListView(generics.ListAPIView):
    """
    List or Create Chats
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatSerializer


    def get_queryset(self):
        # Pagination could be added instead
        if not self.kwargs.get('room'):
            raise Http404()

        return Chat.objects.filter(
            room=self.kwargs['room']
        ).order_by('-created')[:50]



from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def chat_room(request, room):
    """
    Room view - show the room, with latest messages.
    The template for this view has the WebSocket business to send and stream
    messages, so see the template for where the magic happens.
    """
    messages = Chat.objects.filter(room=room).order_by('-created')[:50]

    return render(request, "room.html", {
        'room': room,
        'messages': messages,
    })
