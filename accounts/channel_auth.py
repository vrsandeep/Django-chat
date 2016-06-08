import json
import functools

from rest_framework.authtoken.models import Token

from channels.handler import AsgiRequest


def fetch_user_from_token(key):
    try:
        user = Token.objects.get(key=key)
    except Token.DoesNotExist:
        raise ValueError("Invalid Token!")


def channel_session_user_from_token(func):
    """
    Decorator that automatically transfers the user from token to
    channel-based sessions, and returns the user as message.user as well.
    Useful for things that consume e.g. websocket.connect
    """
    @functools.wraps(func)
    def inner(message, *args, **kwargs):
        # Taken from channels.session.http_session
        # Make sure there's NOT a token_session already
        if hasattr(message, "token_session"):
            return func(message, *args, **kwargs)
        try:
            if "method" not in message.content:
                message.content['method'] = "FAKE"
            request = AsgiRequest(message)
        except Exception as e:
            raise ValueError("Cannot parse HTTP message - are you sure this is a HTTP consumer? %s" % e)

        token = request.GET.get("token", None)
        if token is None:
            # _close_reply_channel(message)
            raise ValueError("Missing token request parameter. Closing channel.")

        message.user = fetch_user_from_token(token)
        message.token = token

        return func(message, *args, **kwargs)
    return inner


def token_session_user(func):
    """
    Checks the presence of a "token" field on the message's text field and
    tries to authenticate the user based on its content.
    """

    @functools.wraps(func)
    def inner(message, *args, **kwargs):
        # Make sure there's a reply_channel
        if not message.reply_channel:
            raise ValueError(
                "No reply_channel sent to consumer; @token_session " +
                "can only be used on messages containing it."
            )
        message_text = message.get('text', None)
        if message_text is None:
            raise ValueError("Missing text field. Closing channel.")

        try:
            message_text_json = json.loads(message_text)
        except ValueError:
            # raise Exception("Missing key from payload")
            pass
        token = message_text_json.pop('token', None)
        if token is None:
            raise ValueError("Missing token field. Closing channel.")

        message.token = token
        message.user = fetch_user_from_token(token)
        message.text = json.dumps(message_text_json)

        return func(message, *args, **kwargs)
    return inner
