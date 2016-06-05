from django.http import Http404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, generics, status

from .models import Chat
from accounts.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):

    user = UserSerializer()

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
