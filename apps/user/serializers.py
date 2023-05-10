
from ..abstract.serializers import AbstractSerializer
from .models import User


class UserSerializer(AbstractSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if self.context:
            rep['isFriend'] = self.context['request'].user.friends.filter(public_id = rep['id']).exists()
        return rep

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'bio', 'city', 'birthday',
                  'is_active', 'created', 'updated']
        read_only_field = ['is_active']
