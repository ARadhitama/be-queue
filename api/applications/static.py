from api import models as M
from oauth import models as oauth


class StaticApp:
    @staticmethod
    def get_provinces() -> list:
        return list(oauth.Province.objects.all())

    @staticmethod
    def get_cities(province: str) -> list:
        return list(oauth.City.objects.filter(province__name=province).all())

    @staticmethod
    def get_categories() -> list:
        return list(M.ServiceCategory.objects.all())

    @staticmethod
    def get_services_by_categories(category: str) -> list:
        return list(M.Service.objects.filter(category__name=category).all())

    def get_services_by_city(self, category: str, city: str) -> list:
        services = self.get_services_by_categories(category)

        res = []
        for s in services:
            if s.city == city:
                res.append(s)
        return res

    def get_services_by_province(self, category: str, province: str) -> list:
        services = self.get_services_by_categories(category)

        res = []
        for s in services:
            if s.province == province:
                res.append(s)
        return res

    @staticmethod
    def get_service_details(service_id: int) -> M.Service:
        return M.Service.objects.filter(id=service_id).first()
