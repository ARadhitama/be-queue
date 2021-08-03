from api.applications.base import BaseError
from api.applications.queue import QueueApp
from django.db import reset_queries
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from api.db_manager import get_session, is_valid_category, json_response_error
from api.global_var import *
from api.external_api.raja_api import *
from api.applications.company import CompanyApp
from api.applications.service import ServiceApp

import json

class QueueUserView(View):
    # get queue number 
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
        
        queue_app = QueueApp(user_data['id'])

        try:
            result = queue_app.get_user_queue(service_id)
        except Exception as e:
            return json_response_error(e)

        queue_app = QueueApp(user_data['id'])

        try:
            result = queue_app.get_user_queue(data['service_id'])
        except Exception as e:
            return json_response_error(e)

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

        queue_app = QueueApp(user_data['id'])

        try:
            result = queue_app.queue_to_service(data['service_id'])
        except Exception as e:
            return json_response_error(e)

        return JsonResponse({"queue_number": result})


class QueueServiceView(View): # DONE
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

        queue_app = QueueApp(user_data['id'])
        
        try:
            result = queue_app.get_current_queue(data['service_id'])
        except Exception as e:
            return json_response_error(e)

        return JsonResponse(result, safe=False)

    
class GetAllServiceOnLocationView(View):    # DONE
    # get service based on location 
    def post(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)
        print(user_data)
        try:
            data = json.loads(request.body)
            category_id = data['category_id']
            filter = data['filter']
        except Exception:
            return json_response_error(INVALID_PARAM)

        service_app = ServiceApp(user_data['id'])
        try:
            if filter == 'kabupaten':
                result = service_app.get_all_service_on_location_arr(data['category_id'], user_data['kabupaten'], data['filter'])
            elif filter == 'kecamatan':
                result = service_app.get_all_service_on_location_arr(data['category_id'], user_data['kecamatan'], data['filter'])
            elif filter == 'kelurahan':
                result = service_app.get_all_service_on_location_arr(data['category_id'], user_data['kelurahan'], data['filter'])
            else:
                return json_response_error("invalid_location")
        except Exception as e:
            return json_response_error(e.message)

        return JsonResponse(result, safe=False)


class GetAllServiceOnCompanyView(View): # DONE
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
            result = service_app.get_all_service_on_company_arr(data['company_id'])
        except Exception as e:
            return json_response_error(e.message)

        return JsonResponse(result, safe=False)


class GetServiceDataView(View): # DONE
    # get clicked service data
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

        service_app = ServiceApp(user_data['id'])
        try:
            service_data = service_app.get_service_detail_dict(data['service_id'])
        except Exception:
            return json_response_error(DB_ERROR)
        
        if not service_data:
            return json_response_error("no_available_services")

        return JsonResponse(service_data[0], safe=False)
    

class CreateServiceView(View):  #DONE
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
    
        # check is company owner
        company_app = CompanyApp(user_data['id'])
        is_owner = company_app.is_company_owner(data['company_id'])

        if not is_owner:
            return json_response_error("not_owner")
        
        # check valid category
        valid_category = is_valid_category(data['category_id'])
        if not valid_category:
            return json_response_error("wrong_category")

        created = False

        service_app = ServiceApp(user_data['id'])
        try:
            created = service_app.create_service(data)
        except Exception as e:
            return json_response_error(e)

        if created:  
            return JsonResponse({"message": SUCCESS})
        else:
            return json_response_error(DB_ERROR)


class CompanyView(View):    # DONE
    # get user company
    def get(self, request):
        try:
            user_data = get_session(request.headers.get('authorization', None))
        except:
            return json_response_error(NOT_LOGGED_IN)

        company_app = CompanyApp(user_data['id'])
        try:
            result = company_app.get_all_company_data_arr()
        except Exception:
            return json_response_error(DB_ERROR)
        
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
            name=data['name'],
            email=data['email'],
            address=data['address'],
            kabupaten_id=data['kabupaten_id'],
            kabupaten_name=data['kabupaten_name'],
            kecamatan_id=data['kecamatan_id'],
            kecamatan_name=data['kecamatan_name'],
            kelurahan_id=data['kelurahan_id'],
            kelurahan_name=data['kelurahan_name'],
            phone_number=data['phone_number'],
            description=data['description'],
        except Exception:
            return json_response_error(INVALID_PARAM)

        created = False
        
        company_app = CompanyApp(user_data['id'])
        try:
            created = company_app.create_company(data)
        except Exception as e:
            return json_response_error(e)
        
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