from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models


class ServerKeys(models.Model):
    server_public_key = models.CharField(max_length=10000, null=True, default=None)
    server_private_key = models.CharField(max_length=10000, null=True, default=None)

class University(models.Model):
    name = models.CharField(max_length=100)


class User(AbstractBaseUser):
    class Roles(models.TextChoices):
        Professor = ('p', 'Professor')
        Student = ('s', 'Student')

    name = models.CharField(max_length=100, unique=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Roles.choices, default='', null=False, blank=True)
    national_id = models.CharField(max_length=100, unique=True, null=True, default=None)
    phone = models.CharField(max_length=100, null=True, default=None)
    mobile = models.CharField(max_length=100, null=True, default=None)
    address = models.CharField(max_length=100, null=True, default=None)
    client_public_key = models.CharField(max_length=10000, null=True, default=None)
    session_key = models.CharField(max_length=10000, null=True, default=None)

    objects = UserManager()

    USERNAME_FIELD = 'name'

