from django.db import reset_queries
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from api.db_manager import get_session, json_response_error
from api.global_var import *

import json

class QueueUserView(View):
    # get queue number 
    def get(self, request):
        try:
            print(request.headers.get('authorization', None))
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)
        
        result = {
            "service_name": "asdasdsa",
            "service_phone": "081232113",
            "service_address": "asdasdasdasdada",
            "service_price" : 100000,
            "service_description": "adasdasdasd",
            "current_queue_number": 3,
            "user_queue_number": 5
        }
        return JsonResponse(result, safe=False)
    
    # queue to a service
    def post(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)

        try:
            data = json.loads(request.body)
            service_id = data['service_id']
        except Exception:
            return json_response_error(INVALID_PARAM)

        return JsonResponse({"queue_number": 10})


class QueueServiceView(View):
    # get current queue
    def post(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)

        try:
            data = json.loads(request.body)
            service_id = data['service_id']
        except Exception:
            return json_response_error(INVALID_PARAM)

        user_data = {
            "id": 1,
            "name": "asdadads",
            "number": 5
        }

        result = [
            user_data,
            user_data,
            user_data,
            user_data,
        ]

        return JsonResponse(result, safe=False)

    
class GetAllServiceOnLocationView(View):
    # get service based on location
    def get(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)
        
        service_data = {
            "service_id": 1,
            "service_name": "sdadsad",
            "service_image": "sdasdsad"
        }

        result = [
            service_data,
            service_data,
            service_data
        ]

        return JsonResponse(result, safe=False)


class GetAllServiceOnCompanyView(View):
    # get service based on company
    def get(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)
        
        try:
            data = json.loads(request.body)
            company_id = data['company_id']
        except Exception:
            return json_response_error(INVALID_PARAM)

        service_data = {
            "service_id": 1,
            "service_name": "sdadsad",
            "service_image": "sdasdsad"
        }

        result = [
            service_data,
            service_data,
            service_data
        ]

        return JsonResponse(result, safe=False)


class GetServiceDataView(View):
    # get clicked service data
    def get(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)
        
        try:
            data = json.loads(request.body)
            service_id = data['service_id']
        except Exception:
            return json_response_error(INVALID_PARAM)

        result = {
            "service_name": "asdasdsa",
            "service_phone": "081232113",
            "service_address": "asdasdasdasdada",
            "service_price" : 100000,
            "service_description": "adasdasdasd",
            "service_open_time": "12.30",
            "service_close_time": "15.30",
            "current_queue_number": 5,
            "last_queue_number": 10
        }

        return JsonResponse(result, safe=False)
    

class CreateServiceView(View):
    # make new service, post category, ownner, company
    def post(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)

        try:
            data = json.loads(request.body)
            company_id = data['company_id'],
            category_id = data['category_id'],
            service_name = data['service_name'],
            description = data['description'],
            price = data['price'],
            open_time = data['open_time'],
            close_time = data['close_time'],
        except Exception:
            return json_response_error(INVALID_PARAM)
        
        return JsonResponse({"message": SUCCESS})


class CompanyView(View):
    # get user company
    def get(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)

        company_data = {
            "id": 1,
            "name": "asdasdd",
            "description": "adasdsadsad",
            "email": "adsadasd",
            "kota": "asdasd",
            "no_hp": "0123123213"
        }

        result = [
            company_data,
            company_data,
            company_data
        ]

        return JsonResponse(result, safe=False)
    # make new company
    def post(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)
        
        try:
            data = json.loads(request.body)
            owner_id = user_data['id'],
            name = data['name'],
            description = data['description'],
            email=data['email'],
            kota=data['kota'],
            no_hp=['no_hp']
        except Exception:
            return json_response_error(INVALID_PARAM)

        return JsonResponse({"message": SUCCESS})