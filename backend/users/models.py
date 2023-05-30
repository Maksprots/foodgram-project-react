from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Логин',
        max_length=settings.MAX_LEN_USER_FIELD,
        unique=True)
    email = models.EmailField(
        verbose_name='Email',
        max_length=settings.MAX_LEN_USER_EMAIL,
        unique=True)
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.MAX_LEN_USER_FIELD, )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.MAX_LEN_USER_FIELD)
    password = models.CharField(
        verbose_name='Пароль',
        max_length=settings.MAX_LEN_USER_FIELD)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}, {self.email}'
