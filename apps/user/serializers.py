
from ..abstract.serializers import AbstractSerializer
from .models import User


class UserSerializer(AbstractSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'bio', 'city', 'birthday',
                  'is_active', 'created', 'updated']
        read_only_field = ['is_active']
