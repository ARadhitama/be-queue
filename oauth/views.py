from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import IntegrityError

import jwt
import json

from oauth.models import UserProfile

def get_user_data(user_id):
    return UserProfile.objects.filter(id=user_id).first()

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
        'username': user_check.username,
        'email': user_check.email,
        'kabupaten': user_check.kabupaten,
        'kecamatan': user_check.kecamatan,
        'kelurahan': user_check.kelurahan,
        'status_ban': user_check.status_ban,
        'foto_ktp': user_check.foto_ktp
    }

    jwt_token = jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)

    return JsonResponse({'token': jwt_token}, status=200)


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
        kabupaten = data['kabupaten']
        kecamatan = data['kecamatan']
        kelurahan = data['kelurahan']

    except Exception as e:
        return JsonResponse({'message': str(e)})

    try:
        UserProfile.objects.create_user(username, password, email, kabupaten, kecamatan, kelurahan)
    except IntegrityError:
        return JsonResponse({"message": "User already exist"}, status=400)

    return JsonResponse({"message": "User created"}, status=200)


