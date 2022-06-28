from django.urls import path, include
from rest_framework import routers
from api.views import PostViewSet

router = routers.SimpleRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
