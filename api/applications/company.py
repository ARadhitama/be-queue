from .base import Application, BaseError
from .user import UserApp

from api.global_var import *
from api.models import Company

class CompanyApp(Application):
    def __init__(self, id):
        self.__id = id
        self.__user = UserApp(id)

    def create_company(self, data):
        try:
            Company.objects.create(
                owner_id=self.__id,
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
            )
            return True
        except Exception:
            raise BaseError(DB_ERROR)
    
    def get_all_company_data_arr(self):
        try:
            company_dict = Company.objects.filter(owner_id=self.__id).values().all()
        except Exception:
            raise BaseError(DB_ERROR)

        result = []

        for company in company_dict:   
            company_data = {
                "id": company['id'],
                "name": company['name'],
                "email": company['email'],
                "address": company['address'],
                "kabupaten_id": company['kabupaten_id'],
                "kabupaten_name": company['kabupaten_name'],
                "kecamatan_id": company['kecamatan_id'],
                "kecamatan_name": company['kecamatan_name'],
                "kelurahan_id": company['kelurahan_id'],
                "kelurahan_name": company['kelurahan_name'],
                "phone_number": company['phone_number'],
                "description": company['description']
            }
            result.append(company_data)

        return result

    def get_company_data(self, company_id):
        return Company.objects.filter(id=company_id).first()


    def is_company_owner(self, company_id):
        company = Company.objects.filter(id=company_id, owner_id=self.__id).values().all()

        if not company:
            return False
        return True