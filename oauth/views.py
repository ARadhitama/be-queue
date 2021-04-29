from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import IntegrityError

import jwt
import json

from oauth.models import UserProfile


@csrf_exempt
def login_account(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
    except Exception as e:
        return JsonResponse({'message': str(e)})

    user_check = authenticate(request, username=username, password=password)

    if user_check is None:
        return JsonResponse({'message': "invalid username/password"}, status=401)

    payload = {
        'id': user_check.id,
        'username': user_check.username
    }

    jwt_token = jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)

    return JsonResponse({'token': jwt_token.decode('utf-8')}, status=200)


@csrf_exempt
def check_account(request):
    try:
        jwt_token = request.headers.get('authorization', None)
    except Exception as e:
        return JsonResponse({'message': str(e)})

    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return JsonResponse({'message': "Invalid Token"}, status=401)
    else:
        return JsonResponse({'message': "Not Authorized"}, status=401)
    return JsonResponse(payload, status=200)


@csrf_exempt
def create_new_user(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        email = data['email']
        provinsi = data['provinsi']
        kota = data['kota']

    except Exception as e:
        return JsonResponse({'message': str(e)})

    try:
        UserProfile.objects.create_user(username, password, email, provinsi, kota)
    except IntegrityError:
        return JsonResponse({"message": "User already exist"}, status=400)

    return JsonResponse({"message": "User created"}, status=200)