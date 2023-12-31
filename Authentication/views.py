import base64
import json

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from rest_framework import generics

from .enc import encrypt, decrypt
from university_project.Server.confidentiality_tools import generate_server_keys
from .serializers import UserSerializer
from .models import User, ServerKeys
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def key_exchange(request):
    server_public_key = ServerKeys.objects.first().server_public_key

    request.user.client_public_key = json.loads(request.body.decode('utf-8')).get("client_public_key")
    request.user.save()

    return Response(server_public_key, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def receive_session_key_from_client(request):
    encrypted_session_key = json.loads(request.body.decode('utf-8')).get("encrypted_session_key")
    encrypted_session_key = base64.b64decode(encrypted_session_key)

    private_key = RSA.import_key(ServerKeys.objects.first().server_private_key)
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_session_key = cipher.decrypt(encrypted_session_key).decode()
    request.user.session_key = decrypted_session_key
    request.user.save()

    return Response("Session Key Accepted", status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_projects(request):
    cipher_body = request.body.decode('utf-8')
    body = decrypt(cipher_body, request.user.session_key)
    body = json.loads(body)

    print("Project Received Successfully : ",body)
    return Response("Projects Received", status=200)