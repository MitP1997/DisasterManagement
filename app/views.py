from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import *

class Globals():
    response = {}
    response['status'] = 0
    response['data'] = {}
    data = {}

    def success(self,arr):
        response = self.response
        response['status'] = 1
        response['data'] = arr
        return HttpResponse(json.dumps(response), status=200, content_type="application/json")

class Civilian():
    data = {}

    def __init__(self):
        self.data = {}

    def registerFamily(self,request):
        if request.method == "GET":
            return render(request,'register_family.html')
        else:
            family = Families()
            family.create(request.POST) # This function is to reduce the LOC here in views.py
            if request.POST.get('api') is not None:
                self.data['family_id'] = family.id
                response = Globals().success(self.data)
            else:
                response = redirect('register-family')
            return response

    def registerCivilian(self,request):
        if request.method == "GET":
            return render(request,'register_civilian.html')
        else:
            civilian = Civilians()
            civilian.create(request.POST)
            if request.POST.get('api') is not None:
                self.data['civilian_id'] = civilian.id
                response = Globals().success(self.data)
            else:
                response = redirect('register-civilian')
            return response
