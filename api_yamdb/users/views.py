from api.permissions import IsAdmin
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import (GetTokenSerializer, MeUserSerializer,
                          SignupSerializer, UserSerializer)
from .utils import (create_confirmation_code, create_jwt_token,
                    send_confirmation_code)


class APISignup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user, _ = User.objects.get_or_create(
                username=username,
                email=email
            )
        except Exception as error:
            raise ValidationError(
                (f'Ошибка создания нового пользователя {error}. '
                 'Данный username или email уже существует')
            )
        user.confirmation_code = create_confirmation_code(user)
        user.save()
        send_confirmation_code(user)
        return Response(serializer.validated_data, status=HTTP_200_OK)


class APIGetToken(APIView):
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if confirmation_code != user.confirmation_code:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response({'token': create_jwt_token(user)})


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    def perform_create(self, serializer):
        if 'role' not in self.request.data:
            serializer.save(role='user')
        serializer.save()

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
    )
    def get_or_update_yourself(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserSerializer(user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    user,
                    data=request.data,
                    partial=True
                )
            else:
                serializer = MeUserSerializer(
                    user,
                    data=request.data,
                    partial=True
                )
            if not serializer.is_valid():
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.data)
