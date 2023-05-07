
from ..abstract.serializers import AbstractSerializer
from .models import User


class UserSerializer(AbstractSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar',
                  'is_active', 'created', 'updated']
        read_only_field = ['is_active']
