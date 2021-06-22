from django.contrib import admin
from django.urls import path, include
from api import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('queue_user/', csrf_exempt(views.QueueUserView.as_view())),
    path('queue_service/', csrf_exempt(views.QueueServiceView.as_view())),
    path('location_service/', csrf_exempt(views.GetAllServiceOnLocationView.as_view())),
    path('company_service/', csrf_exempt(views.GetAllServiceOnCompanyView.as_view())),
    path('service_data/', csrf_exempt(views.GetServiceDataView.as_view())),
    path('create_service/', csrf_exempt(views.CreateServiceView.as_view())),
    path('company/', csrf_exempt(views.CompanyView.as_view())),

]