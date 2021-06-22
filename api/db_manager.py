from oauth.models import *
from api.models import *
from django.conf import settings
from api.global_var import *
from django.http import JsonResponse

import jwt

def get_session(token):
    try:
        data = jwt.decode(
            token,
            settings.JWT_SECRET,
            settings.JWT_ALGORITHM
        )
        return data
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        raise Exception(NOT_LOGGED_IN)

def json_response_error(message):
    return JsonResponse({"message": message}, status=400)