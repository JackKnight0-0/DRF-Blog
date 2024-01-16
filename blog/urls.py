from django.urls import path

from .views import ArticleCreateAPIView, ArticleListAPIView, ArticleDetailView, CommentAddView, CommentDestroyAPIView, \
    ArticleDestroyAPIView, ArticleUpdateAPIView

urlpatterns = [
    path('', ArticleListAPIView.as_view()),
    path('new/', ArticleCreateAPIView.as_view()),
    path('comment/<int:pk>/', CommentDestroyAPIView.as_view()),
    path('comment/new/<slug:article_slug>/', CommentAddView.as_view()),
    path('delete/<slug:slug>/', ArticleDestroyAPIView.as_view()),
    path('edit/<slug:slug>/', ArticleUpdateAPIView.as_view()),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='detail_article'),
]
