from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from .sierializers import ArticleSerializer, ArticleDetailSerializer, ArticleListSerializer, \
    CommentCreateSerializer, ArticleUpdateSerializer
from .permission import IsOwnerOfComment, IsOwnerOfArticle
from .models import Article, Comment


class ArticleCreateAPIView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)


class ArticleListAPIView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticated,)


class CommentAddView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_article(self):
        return get_object_or_404(Article, slug=self.kwargs.get('article_slug'))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)
        return Response({'comment': serializer.data, 'status': HTTP_201_CREATED})

    def perform_create(self, serializer):
        return serializer.save(article=self.get_article())


class ArticleDestroyAPIView(generics.DestroyAPIView):
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOfArticle)
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={
            'msg': f'Your article "{instance.title}" was delete successful.'
        }, status=status.HTTP_204_NO_CONTENT)


class ArticleUpdateAPIView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOfArticle)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    serializer_class = ArticleUpdateSerializer


class CommentDestroyAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOfComment)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={
            'comment': instance.comment,
            'msg': 'Your comment was delete successful.'
        }, status=status.HTTP_204_NO_CONTENT)
