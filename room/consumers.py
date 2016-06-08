"""
    All WebSocket connections require authenticated user
"""
import logging

from channels import Group

from .models import ROOMS, Chat
from .views import ChatAddSerializer
from accounts.channel_auth import channel_session_user_from_token, token_session_user


log = logging.getLogger(__name__)


def find_room(request_path):
    """
    Looks up the room from the request path and returns it
    """
    path = request_path.decode('ascii').strip('/').split('/')
    try:
        if path[0] != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            raise ValueError("Invalid ws path")

        room = path[-1]
        if room not in [i[0] for i in ROOMS]:
            log.info('ws room %s does not exist', room)
            raise ValueError("%s room does not exist" , room)
    except ValueError,e:
        return None
    return room


@channel_session_user_from_token
def ws_connect(message):
    """
    Websocket onconnect channel
    """
    room = find_room(message['path'])
    if not room:
        return
    log.debug('chat connect room=%s client=%s:%s',
        room, message['client'][0], message['client'][1])
    Group('chat-' + room, channel_layer=message.channel_layer).add(message.reply_channel)


@token_session_user
def ws_receive(message):
    """
    Websocket Receive channel
    """
    room = find_room(message['path'])
    if not room:
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    import json
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return

    if not data:
        return

    # Save Chat to db, ideally perform this in another channel
    data['room'] = room
    log.debug('chat message room=%s username=%s message=%s',
        room, data['user'], data['content'])
    serializer = ChatAddSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        log.debug('Saved!')
    else:
        log.debug("ws message unexpected format data=%s", serializer.errors)
        return

    # Relay chat message to users in this room
    Group('chat-'+room, channel_layer=message.channel_layer).send(
        {"text": json.dumps(serializer.data)}
    )


def ws_disconnect(message):
    """
    Websocket onclose channel
    """
    room = find_room(message['path'])
    if not room:
        return

    Group('chat-' + room, channel_layer=message.channel_layer).discard(message.reply_channel)
