from django.db import reset_queries
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from api.db_manager import get_session, json_response_error
from api.global_var import *
from api.external_api.raja_api import *
from api.applications.company import CompanyApp
from api.applications.service import ServiceApp

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
        
        service_app = ServiceApp(user_data['id'])
        try:
            result = service_app.get_all_service_on_location_dict(user_data['kota'])
        except Exception:
            return json_response_error(DB_ERROR)

        # service_data = {
        #     "service_id": 1,
        #     "service_name": "sdadsad",
        #     "service_image": "sdasdsad"
        # }
        
        # result = [
        #     service_data,
        #     service_data,
        #     service_data
        # ]

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

        service_app = ServiceApp(user_data['id'])
        try:
            result = service_app.get_all_service_on_company_dict(company_id)
        except Exception:
            return json_response_error(DB_ERROR)

        # service_data = {
        #     "service_id": 1,
        #     "service_name": "sdadsad",
        #     "service_image": "sdasdsad"
        # }

        # result = [
        #     service_data,
        #     service_data,
        #     service_data
        # ]

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

        service_app = ServiceApp(user_data['id'])
        try:
            service_data = service_app.get_service_detail_dict(service_id)
        except Exception:
            return json_response_error(DB_ERROR)

        return service_data[0]

        # result = {
        #     "service_name": "asdasdsa",
        #     "service_phone": "081232113",
        #     "service_address": "asdasdasdasdada",
        #     "service_price" : 100000,
        #     "service_description": "adasdasdasd",
        #     "service_open_time": "12.30",
        #     "service_close_time": "15.30",
        #     "current_queue_number": 5,
        #     "last_queue_number": 10
        # }

        # return JsonResponse(result, safe=False)
    

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
        
        created = False

        service_app = ServiceApp(user_data['id'])
        try:
            created = service_app.create_service(
                company_id,
                category_id,
                service_name,
                description,
                price,
                open_time,
                close_time
            )
        except Exception as e:
            return json_response_error(e)

        if created:  
            return JsonResponse({"message": SUCCESS})
        else:
            return json_response_error(DB_ERROR)


class CompanyView(View):
    # get user company
    def get(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)

        company_app = CompanyApp(user_data['id'])
        try:
            result = company_app.get_all_company_data_dict()
        except Exception:
            return json_response_error(DB_ERROR)

        # company_data = {
        #     "id": 1,
        #     "name": "asdasdd",
        #     "description": "adasdsadsad",
        #     "email": "adsadasd",
        #     "kota": "asdasd",
        #     "no_hp": "0123123213"
        # }

        # result = [
        #     company_data,
        #     company_data,
        #     company_data
        # ]

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

        created = False

        company_app = CompanyApp(user_data['id'])
        try:
            created = company_app.create_company(data)
        except Exception as e:
            return json_response_error(e)
        print(created)
        if created:  
            return JsonResponse({"message": SUCCESS})
        else:
            return json_response_error(DB_ERROR)


class KabupatenView(View):
    def get(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)

        result = get_kabupaten()

        return JsonResponse(result, safe=False)


class KecamatanView(View):
    def post(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)

        try:
            data = json.loads(request.body)
            kabupaten_id = data['kabupaten_id']
        except Exception:
            return json_response_error(INVALID_PARAM)

        result = get_kecamatan(kabupaten_id)

        return JsonResponse(result, safe=False)


class KelurahanView(View):
    def post(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)

        try:
            data = json.loads(request.body)
            kecamatan_id = data['kecamatan_id']
        except Exception:
            return json_response_error(INVALID_PARAM)

        result = get_kelurahan(kecamatan_id)

        return JsonResponse(result, safe=False)


class TestView(View):
    def get(self, request):
        provinsi = get_kabupaten()
        result = get_kelurahan(3172040)
        return JsonResponse(result, safe=False)