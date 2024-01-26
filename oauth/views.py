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
        'phone_number': user_check.phone_number,
        'province': user_check.province,
        'city': user_check.city,
        'user_type': user_check.user_type
    }

    jwt_token = jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)

    return JsonResponse({'token': jwt_token}, status=200)


@csrf_exempt
def check_login(request):
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
def signup(request):
    try:
        data = json.loads(request.body)
        password = data['password']
        username = data['username']
        phone_number = data['phone_number']
        province = data['province']
        city = data['city']
        user_type = data['user_type']
    except Exception as e:
        return JsonResponse({'message': str(e)})

    try:
        UserProfile.objects.create_user(username, password, phone_number, province, city, user_type)
    except IntegrityError:
        return JsonResponse({"message": "User already exist"}, status=400)

    return JsonResponse({"message": "User created"}, status=200)


