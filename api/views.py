from django.shortcuts import render
from django.views import View
from django.http import JsonResponse


class QueueUserView(View):
    def get(self, request):
        # get nomor 
        
        return JsonResponse(result, safe=False)
    
    def post(self, request):

        return JsonResponse({"msg": "queue success"})


class QueueServiceView(View):
    def get(self, request):
        # get current queue

        return JsonResponse(result, safe=False)

    
class ServiceView(View):
    def get(self, request):
        # get service based on location

        return JsonResponse(resul, safe=False)
    def post(self, request):
        # make new service, post category, ownner, company
        return