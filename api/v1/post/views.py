from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from api.v1.abstract.views import AbstractViewSet
from api.v1.mixin.views import PaginatedResponseMixin
from apps.post.models import Post
from apps.post.serializers import PostSerializer
from apps.auth.permissions import UserPermission
from rest_framework.response import Response


class PostViewSet(PaginatedResponseMixin, AbstractViewSet):
    http_method_names = ('post', 'get', 'patch', 'delete')
    permission_classes = (UserPermission,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user

        user.like_post(post)

        serializer = self.serializer_class(post)

        return Response(serializer.data)


    @action(methods=['post'], detail=True)
    def remove_like(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user

        user.remove_like_post(post)

        serializer = self.serializer_class(post)

        return Response(serializer.data)
