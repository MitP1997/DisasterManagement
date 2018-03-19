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


def shelderadd(request):
    shelter = Shelter()
    
    
    supplier1 = SystemUsers()
    supplier1_logs = SupplierLogs()

    # supplier2= SystemUsers()
    # supplier2_logs = SupplierLogs()

    
    official1 = SystemUsers()
    # official2 = SystemUsers()
    
    
    shelter.total_capacity_of_people = 100
    shelter.capacity_used = 0
    shelter.food_packets_needed = 40
    shelter.first_aid_packets_needed = 8
    shelter.shelter_latitude = 12.506951
    shelter.shelter_longitude = 92.9138505
    shelter.shelter_type = 'g'
    shelter.save()
    
    fam = Families()
    fam.last_name = "kothari"
    fam.number_of_members = 4
    fam.save()

    Civilian1 = Civilians()
    Civilian1.family = fam
    Civilian1.current_shelter = shelter
    Civilian1.first_name = "aman"
    Civilian1.last_name = "kothari"
    Civilian1.contact = 9822012345
    Civilian1.email = "amankothari@gmail.com"
    Civilian1.add_line_1 = "bhandup"
    Civilian1.city = "mumbai"
    Civilian1.state = "Maharashtra"
    Civilian1.country = "India"
    Civilian1.pincode = 49
    Civilian1.gender = "m"
    Civilian1.aadhar_number = 123456789012
    Civilian1.blood_group = "A+"
    Civilian1.parent_gaurdian = "subhash"
    Civilian1.save()


    Civilian2 = Civilians()
    Civilian2.family = fam
    Civilian2.current_shelter = shelter
    Civilian2.first_name = "sujar"
    Civilian2.last_name = "kothari"
    Civilian2.contact = 9811012345
    Civilian2.email = "sujalkothari@gmail.com"
    Civilian2.add_line_1 = "bhandup"
    Civilian2.city = "mumbai"
    Civilian2.state = "Maharashtra"
    Civilian2.country = "India"
    Civilian2.pincode = 40
    Civilian2.gender = "m"
    Civilian2.aadhar_number = 123450089012
    Civilian2.blood_group = "A+"
    Civilian2.parent_gaurdian = "subhash"
    Civilian2.save()

    supplier1.shelter = shelter
    supplier1.username = "vishal"
    supplier1.contact = 123
    supplier1.add_line_1 = "portblair"
    supplier1.gender = 'm'
    supplier1.aadhar_number = 123234123
    supplier1.user_role = 's'
    supplier1.save()

    supplier1_logs.supplier = supplier1
    supplier1_logs.quantity_supplied = 123
    supplier1_logs.supply_type = 'fp'
    supplier1_logs.save()

    # supplier2.shelter = shelter
    # supplier2.contact = 456
    # supplier2.add_line_1 = "rangat"
    # supplier2.gender = 'f'
    # supplier2.aadhar_number = 123234
    # supplier2.user_role = 's'
    # supplier2.save()

    # supplier2_logs.supplier = supplier2
    # supplier2_logs.quantity_supplied = 12
    # supplier2_logs.supply_type = 'fa'
    # supplier2_logs.save()

    official1.shelter = shelter
    official1.username = "mit"
    official1.contact = 1111111111
    official1.add_line_1 = "carnicobar"
    official1.gender = 'm'
    official1.aadhar_number = 12003412
    official1.user_role = 'o'
    official1.save()

    # official2.shelter = shelter
    # official2.contact = 2222222222
    # official2.add_line_1 = "carnicobar"
    # official2.gender = 'f'
    # official2.aadhar_number = 12345678
    # official2.user_role = 'o'
    # official2.save()

    context = {
        'new_shelter_id': shelter.id,
    }
    return HttpResponse(context, request)