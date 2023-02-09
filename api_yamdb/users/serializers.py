from rest_framework import serializers

from .models import User


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                f'username {value} уже используется'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                f'email {value} уже используется'
            )
        return value


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role'
                  )


class MeUserSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)
