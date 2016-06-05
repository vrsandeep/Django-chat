from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers


def format_name(name):
    if name:
        return name.title()
    return name

def get_username_field():
    username_field = User._meta.get_field(User.USERNAME_FIELD)
    if hasattr(serializers.ModelSerializer, 'serializer_field_mapping'):  # DRF 3.1
        mapping_dict = serializers.ModelSerializer.serializer_field_mapping
    else:
        raise AttributeError(
            'serializers.ModelSerializer doesn\'t have any of these attributes: '
            'field_mapping, _field_mapping, serializer_field_mapping '
        )
    field_class = mapping_dict[username_field.__class__]
    return field_class()


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'password',
        )
        read_only_fields = (
            'is_admin', 'is_staff',
        )

    def __init__(self, *args, **kwargs):
        super(UserRegisterSerializer, self).__init__(*args, **kwargs)
        self.fields[User.USERNAME_FIELD] = get_username_field()

    def validate_username(self, data):
        """  Ensure the email id was not registered previously """

        if not User.objects.filter(username=data).exists():
            return data
        raise serializers.ValidationError('This username is already registered!')

    def validate_password(self, password):
        if len(password) == 0:
            raise serializers.ValidationError('EMPTY PASSWORD')
        return password

    def save(self, *args, **kwargs):
        self.user = super(UserRegisterSerializer, self).save()
        self.user.set_password(self.validated_data.get('password'))
        self.user.save()
        self.user = authenticate(username=self.user.username, password=self.validated_data['password'])
        self.user.save()
        return self.user


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('password',)
        read_only_fields = ('is_admin', 'is_staff')

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.fields[User.USERNAME_FIELD] = get_username_field()

    def validate(self, attrs):
        self.user = authenticate(username=attrs[User.USERNAME_FIELD], password=attrs['password'])
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError('Account is disabled')
            return attrs
        else:
            raise serializers.ValidationError('Invalid username or password')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'id',)
