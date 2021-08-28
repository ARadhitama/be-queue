from django.contrib import admin
from django.urls import path, include
from api import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('check_queue/', csrf_exempt(views.CheckQueueView.as_view())),
    path('queue_user/', csrf_exempt(views.QueueUserView.as_view())),
    path('queue_service/', csrf_exempt(views.QueueServiceView.as_view())),
    path('location_service/', csrf_exempt(views.GetAllServiceOnLocationView.as_view())),
    path('owned_service/', csrf_exempt(views.GetAllOwnedServiceView.as_view())),
    path('service_data/', csrf_exempt(views.GetServiceDataView.as_view())),
    path('create_service/', csrf_exempt(views.CreateServiceView.as_view())),
    path('kabupaten/', csrf_exempt(views.KabupatenView.as_view())),
    path('kecamatan/', csrf_exempt(views.KecamatanView.as_view())),
    path('kelurahan/', csrf_exempt(views.KelurahanView.as_view())),
    path('test/', csrf_exempt(views.TestView.as_view()))
]