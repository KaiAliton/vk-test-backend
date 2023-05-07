from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from apps.post.serializers import PostSerializer
from ..abstract.views import AbstractViewSet
from apps.user.serializers import UserSerializer
from apps.user.models import User
from rest_framework.response import Response


class UserViewSet(AbstractViewSet):
    http_method_names = ('patch', 'get', 'post')
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_queryset(self):
        if not self.request.user.is_anonymous and self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


    @action(methods=['get'], detail=True)
    def friends(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        friends = user.friends.all()
        friends_serializer = UserSerializer(friends, many=True)
        output = {
            "user": serializer.data,
            "friends": friends_serializer.data,
        }
        return Response(output)


    @action(methods=['post'], detail=True)
    def add_friend(self, request, *args, **kwargs):
        friend = self.get_object()
        user = self.request.user

        user.add_friend(friend)
        serializer = self.serializer_class(friend)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def delete_friend(self, request, *args, **kwargs):
        friend = self.get_object()
        user = self.request.user

        user.delete_friend(friend)
        serializer = self.serializer_class(friend)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def posts(self, request, *args, **kwargs):
        user = self.get_object()
        posts = user.posts.all()
        post_serializer = PostSerializer(posts, many=True)
        return Response(post_serializer.data)
