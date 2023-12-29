import json
from rest_framework import generics
from .serializers import UserSerializer
from .models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views import View
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class UserSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
