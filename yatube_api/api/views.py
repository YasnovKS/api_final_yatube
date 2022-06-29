from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from posts.models import Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


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
    pagination_class = None

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user,
                        post=post)


class GroupViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    '''Класс представления для объектов модели Group.
    Реализует возможность получения данных о сообществах.'''

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


class FollowViewSet(viewsets.ModelViewSet):
    '''Класс представления для объектов модели Follow.
    Реализует возможность получения данных о подписках,
    а также возможность подписываться на пользователей и
    отписываться от них.'''
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter)
    filterset_fields = ('following',)
    search_fields = ('following__username',)
    pagination_class = None

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
