from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from api.filters import TitleFilter
from api.pagination import ReviewsPagination
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnlyPermission
from api.serializers import (CategoriesSerializer, CommentsSerializer,
                             GenresSerializer, ReviewsSerializer,
                             TitleSerializer, TitleSerializerCreate)
from reviews.models import Categories, Genres, Review, Title


class ListCreateDestroyMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoriesViewSet(ListCreateDestroyMixin):
    """Вьюсет для обработки категорий"""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(ListCreateDestroyMixin):
    """Вьюсет для обработки жанров"""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки произведений"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter
    ordering_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializerCreate
        return TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = ReviewsPagination
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title_id=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title_id=title_id)
        serializer.save(author=self.request.user, review=review)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = ReviewsPagination
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)
