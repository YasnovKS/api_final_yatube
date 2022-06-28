from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from posts.models import Post
from .serializers import PostSerializer, CommentSerializer
from rest_framework.pagination import LimitOffsetPagination
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)


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


class CommentViewSet(viewsets.ModelViewSet):
    '''Класс представления для объектов модели Comment.
    Реализует возможность получения, добавления, редактирования
    и удаления комментариев к постам пользователей.'''
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user,
                        post=post)
