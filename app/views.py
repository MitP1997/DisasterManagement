from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from django.views.generic import *

class AdminHome(ListView):
    template_name = 'Admin-Portal/admin_home.html'
    model = Shelter
    context_object_name = 'shelter_list'


class AdminShelter(DetailView):
    template_name = 'Admin-Portal/shelter_detail.html'
    model = Shelter

    def get_context_data(self, **kwargs):
     
        context = super(AdminShelter, self).get_context_data(**kwargs)
        context["Civilians"] = Civilians.objects.filter(current_shelter=self.kwargs.get('pk'))
        context["Officials"] = SystemUsers.objects.filter(shelter=self.kwargs.get('pk'),user_role='o')
        context["Supplier"] = SystemUsers.objects.filter(shelter=self.kwargs.get('pk'),user_role='s')
        return context

class AdminCivilians(ListView):
    template_name = 'Admin-Portal/admin_civilians.html'
    model = Civilians
    context_object_name = 'civilian_list'


class AdminSuppliers(ListView):
    template_name = 'Admin-Portal/admin_suppliers.html'
    model = SupplierLogs
    paginate_by = 5
    context_object_name = 'suppliers_list'
        
    def get_context_data(self, **kwargs):
        
        context = super(AdminSuppliers, self).get_context_data(**kwargs)
        context["Supplier"] = SystemUsers.objects.filter(user_role='s').values()
        return context


class AdminOfficals(ListView):
    template_name = 'Admin-Portal/admin_officials.html'
    model = SystemUsers
    paginate_by = 5
    context_object_name = 'officials_list'

    def get_context_data(self, **kwargs):
        context = super(AdminOfficals, self).get_context_data(**kwargs)
        context['officials_list'] = SystemUsers.objects.filter(user_role='o')
        return context

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
