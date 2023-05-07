from django.db import models
from ..abstract.models import AbstractModel, AbstractManager


class PostManager(AbstractManager):
    pass

class Post(AbstractModel):
    author = models.ForeignKey(to='user.User', on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    cover = models.ImageField(upload_to='covers')
    edited = models.BooleanField(default=False)
    objects = PostManager()

    def __str__(self):
        return f'{self.body}'
