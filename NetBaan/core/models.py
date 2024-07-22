from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings
from django.db.models import Q


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username'], name='unique_username')
        ]


class Books(models.Model):
    title = models.CharField(max_length=200, null=False)
    author = models.CharField(max_length=200, null=False)
    genre = models.CharField(max_length=50, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author', 'genre'], name='unique_book')
        ]

    def __str__(self):
        return self.title


class Reviews(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(rating__gte=1) & Q(rating__lte=5), name='rating_range'),
            models.UniqueConstraint(fields=['book', 'user'], name='unique_user_book_review')
        ]



