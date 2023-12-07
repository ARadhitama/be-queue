from django.contrib import admin
from django.urls import path, include
from api import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("info/", csrf_exempt(views.Info.as_view())),
    path("category/", csrf_exempt(views.CategoryView.as_view())),
    path("services/", csrf_exempt(views.Services.as_view())),
    path("service_details/", csrf_exempt(views.ServiceDetailsView.as_view())),
    path("check_queue/", csrf_exempt(views.CheckQueueView.as_view())),
    path("queue/", csrf_exempt(views.QueueUserView.as_view())),
    path("history/", csrf_exempt(views.QueueUserView.as_view())),
    path("cancel/", csrf_exempt(views.CheckQueueView.as_view())),
    path("create_services/", csrf_exempt(views.CheckQueueView.as_view())),
    path("owned_services/", csrf_exempt(views.CheckQueueView.as_view())),
    path("edit_services/", csrf_exempt(views.CheckQueueView.as_view())),
    path("delete_services/", csrf_exempt(views.CheckQueueView.as_view())),
]
