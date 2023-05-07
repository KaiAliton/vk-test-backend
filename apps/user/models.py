import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from ..abstract.models import AbstractModel, AbstractManager


class UserManager(BaseUserManager, AbstractManager):

    def create_user(self, username, email, password=None,
                    **kwargs):
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')
        if password is None:
            raise TypeError('User must have an email.')
        user = self.model(username=username,
                          email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password,
                         **kwargs):
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an   email.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):

    def like_post(self, post):
        return self.posts_liked.add(post)

    def remove_like_post(self, post):
        return self.posts_liked.remove(post)

    def has_liked_post(self, post):
        return self.posts_liked.filter(pk=post.pk).exists()

    def add_friend(self, friend):
        return self.friends.add(friend)

    def delete_friend(self, friend):
        return self.friends.remove(friend)

    public_id = models.UUIDField(db_index=True, unique=True,
                                 default=uuid.uuid4, editable=False)
    username = models.CharField(db_index=True,
                                max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    city = models.CharField(max_length=30)
    bio = models.CharField(max_length=1000)
    birthday = models.DateTimeField(null=True)
    posts_liked = models.ManyToManyField("post.Post", related_name='liked_by', null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    friends = models.ManyToManyField("user.User", null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return f"{self.username}"