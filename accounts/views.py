from django.contrib.auth import login as auth_login

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from .serializers import UserRegisterSerializer, UserLoginSerializer


class Register(generics.GenericAPIView):
    """
    Creates User Account

    Returns: SESSION cookie on success and 201 status; Errors and 4xx status code on failure
    """

    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def post_register(self):
        auth_login(self.request, self.user)

    def get_response(self):
        token = Token.objects.create(user=self.user)
        return Response({"key": token.key}, status=status.HTTP_201_CREATED)

    def get_error_response(self):
        return Response(self.serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.data)
        if not self.serializer.is_valid():
            return self.get_error_response()

        self.user = self.serializer.save()
        self.post_register()
        return self.get_response()


# Create a Verify Token API

class Login(generics.GenericAPIView):
    """
    Check the credentials and return the SESSION KEY set cookie header
    if the credentials are valid and authenticated.
    Calls Django Auth login method

    Accepts: username, password
    Returns: SESSION Key, 200 on success; Errors and 4xx status code on failure
    """

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def login(self):
        self.user = self.serializer.user
        auth_login(self.request, self.user)

    def get_response(self):
        token, _ = Token.objects.get_or_create(user=self.user)
        return Response({"key": token.key}, status=status.HTTP_200_OK)

    def get_error_response(self):
        return Response(self.serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.data)
        if not self.serializer.is_valid():
            return self.get_error_response()
        self.login()
        return self.get_response()
