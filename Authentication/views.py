import json

from rest_framework import generics

from .enc import encrypt, decrypt
from .serializers import UserSerializer
from .models import User
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator


class UserSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    return Response("this is university home page", status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_sign_up(request):
    cipher_body = request.body.decode('utf-8')
    body = decrypt(cipher_body, request.user.national_id)
    body = json.loads(body)

    request.user.mobile = body.get('mobile')
    request.user.phone = body.get('phone')
    request.user.address = body.get('address')

    request.user.save()

    res = json.dumps({'message': 'complete sign up completed successfully'})
    cipher_text = encrypt(res, request.user.national_id)

    return Response(cipher_text, status=200)
