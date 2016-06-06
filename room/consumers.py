"""
    All WebSocket connections require authenticated user
"""
import logging

from channels import Group
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

from .models import ROOMS, Chat
from .views import ChatSerializer, ChatAddSerializer


log = logging.getLogger(__name__)


@channel_session_user_from_http
def ws_connect(message):

    try:
        path = message['path'].decode('ascii').strip('/').split('/')
        if path[0] != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return
        room = path[-1]
        if room not in [i[0] for i in ROOMS]:
            log.debug('ws room %s does not exist', room)
            return
    except ValueError, e:
        log.debug('invalid ws path=%s', message['path'])
        return

    log.debug('chat connect room=%s client=%s:%s',
        room, message['client'][0], message['client'][1])

    Group('chat-' + room, channel_layer=message.channel_layer).add(message.reply_channel)
    message.channel_session['room'] = room


@channel_session_user
def ws_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        room = message.channel_session['room']
        if room not in [i[0] for i in ROOMS]:
            log.debug('received message, ws room %s does not exist', room)
            return
    except KeyError, e:
        log.debug('no room in channel_session')
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    import json
    try:
        data = json.loads(message['text'])
        log.debug(data)
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return

    if data:
        data['room'] = room
        data['user'] = message.user.username
        log.debug('chat message room=%s username=%s message=%s',
            room, data['user'], data['content'])
        serializer = ChatAddSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            log.debug('Saved!')
        else:
            log.debug("ws message unexpected format data=%s", serializer.errors)
            return

        Group('chat-'+room, channel_layer=message.channel_layer).send(
            {"text": json.dumps(serializer.data)}
        )


@channel_session_user
def ws_disconnect(message):
    try:
        room = message.channel_session['room']
        if room not in [i[0] for i in ROOMS]:
            log.debug('disconnect, ws room %s does not exist', room)
            return
        Group('chat-' + room, channel_layer=message.channel_layer).discard(message.reply_channel)
    except KeyError:
        return
