from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination, viewsets

from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (IsAdminOrReadOnly,
                          IsAuthorOrModeratorOrAdminOrReadOnly)
from reviews.models import Category, Genre, Review, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleListSerializer, TitleSerializer)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = pagination.PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action not in ['list', 'retrieve']:
            return TitleSerializer
        return TitleListSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        if review.title.id == int(self.kwargs.get('title_id')):
            return review.comments.all()
        raise Exception('Ошибка получения комментариев')

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        if review.title.id == int(self.kwargs.get('title_id')):
            return serializer.save(author=self.request.user, review=review)
        raise Exception('Ошибка создания комментария для отзыва')
