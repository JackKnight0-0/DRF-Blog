from rest_framework import serializers

from .models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Article
        fields = (
            'title',
            'content',
            'author'
        )


class ArticleListSerializer(serializers.ModelSerializer):
    my_absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Article
        fields = (
            'author',
            'my_absolute_url',
            'title',
            'content',
            'author'
        )


class ArticleDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Article
        fields = (
            'author',
            'author_username',
            'title',
            'content',
            'comments',
            'create_data',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        comments = Comment.objects.filter(id__in=data.get('comments'))
        comments_data = {}
        for comment in comments:
            user = comment.user
            comments_data[comment.id] = {
                'user_id': user.id,
                'username': user.username,
                'comment': comment.comment
            }
        data['comments'] = comments_data
        return data


class ArticleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'title',
            'content'
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    article = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'user',
            'article',
            'comment'
        )
