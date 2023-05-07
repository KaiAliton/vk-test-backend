from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.abstract.serializers import AbstractSerializer
from apps.user.serializers import UserSerializer
from apps.post.models import Post
from apps.user.models import User


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='public_id')

    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_liked(self, instance):
        request = self.context.get('request', None)
        if request is None or request.user.is_anonymous:
            return False

        return request.user.has_liked_post(instance)

    def get_likes_count(self, instance):
        return instance.liked_by.count()

    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep["author"])
        comments = Comment.objects.filter(post__public_id=rep['id'])
        rep["comments"] = CommentSerializer(comments, many=True).data
        rep["author"] = UserSerializer(author).data
        return rep

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't create a post for another user.")

        return value

    class Meta:
        model = Post
        fields = ['id', 'author', 'body', 'edited',
                  'created', 'updated', 'liked', 'cover', 'likes_count']
        read_only_fields = ["edited"]
