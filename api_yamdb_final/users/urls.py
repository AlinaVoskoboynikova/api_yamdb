from django.urls import include, path
from rest_framework import routers
from users.views import (APIAuthSignup, APIAuthToken, APIUserDetail, APIUserMe,
                         UserViewSet)

app_name = 'users'

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('users/me/', APIUserMe.as_view()),
    path('users/<str:username>/', APIUserDetail.as_view()),
    path('', include(router.urls)),
    path('auth/signup/', APIAuthSignup.as_view()),
    path('auth/token/', APIAuthToken.as_view()),
]
