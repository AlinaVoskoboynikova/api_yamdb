from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                       ReviewsViewSet, TitleViewSet)

router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router.urls)),
]
