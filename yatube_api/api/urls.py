from django.urls import path, include
from rest_framework import routers
from api.views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

router = routers.SimpleRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet,
                basename='comments')
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls.jwt')),
]
