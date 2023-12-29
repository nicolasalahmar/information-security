from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models


class University(models.Model):
    name = models.CharField(max_length=100)


class User(AbstractBaseUser):
    class Roles(models.TextChoices):
        Professor = ('p', 'Professor')
        Student = ('s', 'Student')

    name = models.CharField(max_length=100, unique=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Roles.choices, default='', null=False, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'name'

