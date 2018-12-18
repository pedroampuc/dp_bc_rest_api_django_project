from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import CreateUserSerializer, TransactionSerializer
from rest_framework import viewsets
from .models import Transaction

import requests

CLIENT_ID = 'y2CEp2mR6FHJK866pBWJC0w1eV0ZOD64PM4uNfoX'
CLIENT_SECRET = 'GmmpAcTqwVvpf9zdvPIfbKkh6crJu2vpeQVzk6SUEBtYPprgLmdTzTWTTzLIj9Oi75VOeQzKgR2lgpLLAlRHaiM8lcv1vBjpwWltrqvOz2OOIpVGMI2HZ6J0yvukWhIv'
GET_TOKEN_URL = "http://127.0.0.1:8000/o/token/"
# Create your views here.


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
        Registers user to the server. Input should be in the format:
        {"username": "username", "password": "1234abcd"}
    '''
    # Put the data from the request into the serializer
    print('serializer')
    serializer = CreateUserSerializer(data=request.data)
    #Validate the data
    print('serializer2 ')
    if serializer.is_valid():
        # if valid save
        print('serializer3')
        serializer.save()
        # receive token from created user
        res = requests.request("POST", str(GET_TOKEN_URL), json= {
            'grant_type': 'client_credentials',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        },)
        return Response(res.json())
    print('serializer4')
    return Response(serializer.errors)

@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(
        str(GET_TOKEN_URL),
        json={
            'grant_type': 'client_credentials',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },)
    return Response(r.json())

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Registers user to the server. Input should be in the format:
    {"refresh_token": "<token>"}
    '''
    r = requests.post(
    str(GET_TOKEN_URL),
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },)
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    r = requests.post(
        str(GET_TOKEN_URL),
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    # If it goes well return sucess message (would be empty otherwise)
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    # Return the error if it goes badly
    return Response(r.json(), r.status_code)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
