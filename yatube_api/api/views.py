from rest_framework import viewsets
from posts.models import Post
from .serializers import PostSerializer
from rest_framework.pagination import LimitOffsetPagination
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    '''Класс представления для объектов модели Post.
    Реализует возможность получения, добавления, редактирования
    и удаления постов пользователей.'''

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
