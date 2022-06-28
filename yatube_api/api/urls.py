from django.urls import path, include
from rest_framework import routers
from api.views import PostViewSet, CommentViewSet

router = routers.SimpleRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet,
                basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
