from django.urls import path
from api import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("test/", csrf_exempt(views.TestView.as_view())),
    path("info/", csrf_exempt(views.Info.as_view())),
    path("province/", csrf_exempt(views.ProvinceView.as_view())),
    path("city/", csrf_exempt(views.CityView.as_view())),
    path("category/", csrf_exempt(views.CategoryView.as_view())),
    path("services/", csrf_exempt(views.Services.as_view())),
    path("create_service/", csrf_exempt(views.CreateServiceView.as_view())),
    path("service_detail/", csrf_exempt(views.ServiceDetailsView.as_view())),
    path("owned_services/", csrf_exempt(views.GetAllOwnedServiceView.as_view())),
    path("delete_service/", csrf_exempt(views.DeleteServiceView.as_view())),
    path("edit_service/", csrf_exempt(views.EditServiceView.as_view())),
    path("open_service/", csrf_exempt(views.OpenService.as_view())),
    path("close_service/", csrf_exempt(views.CloseService.as_view())),
    # DONE
    path("check_queue/", csrf_exempt(views.CheckQueueView.as_view())),
    path("queue/", csrf_exempt(views.Queue.as_view())),
    path("history/", csrf_exempt(views.HistoryView.as_view())),
    path("cancel/", csrf_exempt(views.CancelQueueView.as_view())),
]
