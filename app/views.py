from __future__ import unicode_literals
import logging

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils import timezone
from .models import *
from .serializers import *
from forms import *
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
import urllib2
import json
import re
import operator
from fcm_django.models import FCMDevice
import requests
from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth import login, logout
from django.contrib import auth
from googleplaces import GooglePlaces, types, lang
from rest_framework.response import Response
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import googlemaps
from django.forms.formsets import formset_factory
from django.db.models import Sum

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

# class GooglePlacesApi(View):
#     gmaps = googlemaps.Client(key='AIzaSyA8qHwF1krHNFP0N8A4gZEnyLLSvO9iPcw')
#
#     def get(self, request, *args, **kwargs):
#
#         query_result = self.getNearbyHospitals("London","USA")
#         data = []
#         if query_result.has_attributions:
#             print query_result.html_attributions
#
#         for place in query_result.places:
#             # Returned *1 page* of places from a query are place summaries.
#             data['name'] = place.name
#             data['loc'] = place.geo_location
#             data['id'] = place.place_id
#
#             place.get_details()
#             # Referencing any of the attributes below, prior to making a call to
#             # get_details() will raise a googleplaces.GooglePlacesAttributeError.
#             data['details'] =place.details # A dict matching the JSON response from Google.
#             data['num'] = place.local_phone_number
#             print place.international_phone_number
#             data['website'] = place.website
#             data['url'] = place.url
#
#         return HttpResponse(data)
#
#
#     def testQuery(query_result):
#         if query_result.has_attributions:
#             print query_result.html_attributions
#
#         for place in query_result.places:
#             # Returned *1 page* of places from a query are place summaries.
#             print place.name
#             print place.geo_location
#             print place.place_id
#
#             place.get_details()
#             # Referencing any of the attributes below, prior to making a call to
#             # get_details() will raise a googleplaces.GooglePlacesAttributeError.
#             print place.details # A dict matching the JSON response from Google.
#             print place.local_phone_number
#             print place.international_phone_number
#             print place.website
#             print place.url
#
#
#     def getNearbyHospitals(self, latitude, longitude):
#         geocode_result = self.gmaps.geocode({latitude,longitude})
#         location_ = geocode_result[0]['geometry']['location']
#
#         # query_result = google_places.nearby_search(
#         # location=''+latitude+','+longitude, keyword='hosital',
#         # radius=20000, types=[types.TYPE_FOOD])
#         # query_result_type_hospital = self.gmaps.places(location=''+latitude+','+longitude,  radius=20000, types='hospital')
#         return query_result_type_health = self.gmaps.places_nearby(location=location_,keyword = 'health',rank_by='distance',type='hospital')

class AdminHome(ListView):
    template_name = 'Admin-Portal/admin_home.html'
    model = Shelter
    context_object_name = 'shelter_list'

    def get_context_data(self, **kwargs):

        context = super(AdminHome, self).get_context_data(**kwargs)
        context["Stock"] = Stocks.objects.filter()
        return context

class AdminShelter(DetailView):
    template_name = 'Admin-Portal/shelter_detail.html'
    model = Shelter
    context_object_name = 'shelter'

    def get_context_data(self, **kwargs):

        context = super(AdminShelter, self).get_context_data(**kwargs)
        context["civilian_list1"] = Civilians.objects.filter(current_shelter=Shelter.objects.get(id=self.kwargs.get('pk')))
        context["civilian_list2"] = Civilians.objects.filter(assigned_shelter=Shelter.objects.get(id=self.kwargs.get('pk')))
        context["Officials"] = SystemUsers.objects.filter(shelter=Shelter.objects.get(id=self.kwargs.get('pk')),user_role='o')
        context["Supplier"] = SystemUsers.objects.filter(shelter=Shelter.objects.get(id=self.kwargs.get('pk')),user_role='s')
        context["Stock"] = Stocks.objects.filter(shelter=Shelter.objects.get(id=self.kwargs.get('pk')))
        context["shelter_list"] = Shelter.objects.filter()
        return context

class AdminCivilians(ListView):
    template_name = 'Admin-Portal/admin_civilians.html'
    model = Civilians
    context_object_name = 'civilian_list'

    def get_context_data(self, **kwargs):

        context = super(AdminCivilians, self).get_context_data(**kwargs)
        context["shelter_list"] = Shelter.objects.filter()
        return context

class AdminSuppliers(ListView):
    template_name = 'Admin-Portal/admin_suppliers.html'
    model = SupplierLogs
    context_object_name = 'suppliers_list'

    def get_context_data(self, **kwargs):

        context = super(AdminSuppliers, self).get_context_data(**kwargs)
        context["Supplier"] = SystemUsers.objects.filter(user_role='s').values()
        context["shelter_list"] = Shelter.objects.filter()
        return context

class AdminOfficals(ListView):
    template_name = 'Admin-Portal/admin_officials.html'
    model = SystemUsers
    paginate_by = 5
    context_object_name = 'officials_list'

    def get_context_data(self, **kwargs):
        context = super(AdminOfficals, self).get_context_data(**kwargs)
        context['officials_list'] = SystemUsers.objects.filter(user_role='o')
        context["shelter_list"] = Shelter.objects.filter()
        return context

class OfficialShelter(DetailView):
    template_name = 'Official-Portal/shelter_detail.html'
    model = Shelter
    context_object_name = 'shelter'

    def get_context_data(self, **kwargs):

        context = super(OfficialShelter, self).get_context_data(**kwargs)
        context["Civilians"] = Civilians.objects.filter(current_shelter=Shelter.objects.get(id=self.kwargs.get('pk')))
        context["Officials"] = SystemUsers.objects.filter(shelter=Shelter.objects.get(id=self.kwargs.get('pk')),user_role='o')
        context["Supplier"] = SystemUsers.objects.filter(shelter=Shelter.objects.get(id=self.kwargs.get('pk')),user_role='s')
        context["Stock"] = Stocks.objects.filter(shelter=Shelter.objects.get(id=self.kwargs.get('pk')))
        context["shelter"] = Shelter.objects.get(id=self.kwargs.get('pk'))
        return context

class OfficialCivilians(ListView):
    template_name = 'Official-Portal/official_civilians.html'
    model = Civilians
    context_object_name = 'civilian_list'

    def get_context_data(self, **kwargs):

        context = super(OfficialCivilians, self).get_context_data(**kwargs)
        context["civilian_list1"] = Civilians.objects.filter(current_shelter=Shelter.objects.get(id=self.kwargs.get('pk')))
        context["civilian_list2"] = Civilians.objects.filter(assigned_shelter=Shelter.objects.get(id=self.kwargs.get('pk')))
        context["shelter"] = Shelter.objects.get(id=self.kwargs.get('pk'))
        return context

class CivilianRegistrationFormView(FormView):
    template_name = 'civilian_register.html'
    form_class = CivilianRegistrationForm
    success_url = '/civilian-register/'

    def get_form_kwargs(self):
        logger.info('called get form kwargs')
        kwargs=super(CivilianRegistrationFormView,self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        logger.info('called get context')
        context=super(CivilianRegistrationFormView,self).get_context_data()
        form=self.get_form(self.form_class)
        context['form']=form
        return context

    def post(self, request, *args, **kwargs):
        civilian_registration_form= CivilianRegistrationForm(request.POST)
        if civilian_registration_form.is_valid():
            civilian=Civilians()
            civilian.create(civilian_registration_form)
            return self.form_valid(civilian_registration_form,civilian)

    def form_valid(self, form, form_object):
        # Additional system user registration functionaity here (Maybe an Email??)
        return super(CivilianRegistrationFormView, self).form_valid(form)

class SystemUserRegistrationFormView(FormView):
    template_name = "system_user_register.html"
    form_class = SystemUserRegistrationForm
    success_url = "/login/"

    def get_form_kwargs(self):
        logger.info('called get form kwargs')
        kwargs=super(SystemUserRegistrationFormView,self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        logger.info('called get context')
        context=super(SystemUserRegistrationFormView,self).get_context_data()
        form=self.get_form(self.form_class)
        context['form']=form
        return context

    def post(self, request, *args, **kwargs):
        system_user_registration_form= SystemUserRegistrationForm(request.POST)
        if system_user_registration_form.is_valid():
            system_user = SystemUsers()
            length = len(request.get_full_path().split("/"))
            print request.get_full_path().split("/")[length-2]
            system_user.create(system_user_registration_form,request.get_full_path().split("/")[length-2])
            return self.form_valid(system_user_registration_form, system_user)

    def form_valid(self, form, form_object):
        # Additional system user registration functionaity here (Maybe an Email??)
        return super(SystemUserRegistrationFormView, self).form_valid(form)

class LoginFormView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/admin-home/"

    def get_form_kwargs(self):
        logger.info('called get form kwargs')
        kwargs=super(LoginFormView,self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        logger.info('called get context')
        context=super(LoginFormView,self).get_context_data()
        form=self.get_form(self.form_class)
        context['form']=form
        return context

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=login_form.cleaned_data.get('aadhar_number'), password=login_form.cleaned_data.get('password'))
            login(request,user)
            if user.user_role == 'o':
                self.success_url = '/official-home/'+str(user.shelter_id)+'/'
            elif user.user_role == 's':
                self.success_url = '/supplier-home/'
            return self.form_valid(login_form, user)

    def form_valid(self, form, form_object):
        # Additional system user registration functionaity here (Maybe an Email??)
        return super(LoginFormView, self).form_valid(form)

class CivilianUpdateShelterDetailView(DetailView):
    model = Civilians
    template_name = 'civilian_update_shelter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time'] = timezone.now()
        return context

    def get(self, request, *args, **kwargs):
        civilian_aadhar_number = request.GET.get('aadhar_number')
        shelter_id = request.user.shelter.id
        civilian = Civilian.objects.get(aadhar_number=civilian_aadhar_number)
        civilian.updateAssignedShelter(Shelter.objects.get(id=shelter_id))
        return redirect('shelter-updated-successfully') ##TODO update final redirect

class RegisterAtShelterFormView(FormView):
    template_name = "Official-Portal/register_at_shelter.html"
    form_class = CivilianAtShelterForm
    success_url = "/official-civilians/"


    def get(self, request, *args, **kwargs):
        self.success_url =  "/official-civilians/"+self.kwargs.get('pk')

    def get_form_kwargs(self):
        logger.info('called get form kwargs')
        kwargs=super(RegisterAtShelterFormView,self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        logger.info('called get context')
        context=super(RegisterAtShelterFormView,self).get_context_data()
        form=self.get_form(self.form_class)
        context['form']=form
        return context

    def post(self, request, *args, **kwargs):
        register_at_shelter_form= CivilianAtShelterForm(request.POST)
        if register_at_shelter_form.is_valid():
            try:
                civilian = Civilians.objects.get(aadhar_number=register_at_shelter_form.cleaned_data.get('aadhar_number'))
            except ObjectDoesNotExist:
                civilian = Civilians.objects.get(contact=register_at_shelter_form.cleaned_data.get('mobile_number'))
            civilian.updateCurrentShelter(request.user.shelter)
            current_shelter = request.user.shelter
            current_shelter.updateOccupiedCapacity(1)
            assigned_shelter = civilian.assigned_shelter
            assigned_shelter.updateExpectedCapacity(-1)
            return self.form_valid(register_at_shelter_form, system_user)

    def form_valid(self, form, form_object):
        # Additional system user registration functionaity here (Maybe an Email??)
        return super(RegisterAtShelterFormView, self).form_valid(form)

## TODO show the list of members and the count of that particular family before submission
class AllocationAtShelterFormView(FormView):
    template_name = "Official-Portal/allocate_at_shelter.html"
    form_class = CivilianAllocationForm
    success_url = "/allocated-at-shelter-successfully/"

    def get_form_kwargs(self):
        logger.info('called get form kwargs')
        kwargs=super(AllocationAtShelterFormView,self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        logger.info('called get context')
        context=super(AllocationAtShelterFormView,self).get_context_data()
        form=self.get_form(self.form_class)
        context["shelter"] = Shelter.objects.get(id=self.kwargs.get('pk'))
        context['form']=form
        context['time']=timezone.now()
        return context

    def post(self, request, *args, **kwargs):
        allocate_at_shelter_form= CivilianAllocationForm(request.POST)
        if allocate_at_shelter_form.is_valid():
            try:
                civilian = Civilians.objects.get(aadhar_number=allocate_at_shelter_form.cleaned_data.get('aadhar_number'))
            except ObjectDoesNotExist:
                civilian = Civilians.objects.get(contact=allocate_at_shelter_form.cleaned_data.get('mobile_number'))
            # get or create on AllocationToFamilies for civilian.family
            print(request.user.shelter)
            allocation_to_family, created = AllocationToFamilies.objects.get_or_create(family=civilian.family,shelter=request.user.shelter)

            length = len(request.get_full_path().split("/"))
            allocation_to_be_done = request.get_full_path().split("/")[length-2]

            count = allocate_at_shelter_form.cleaned_data.get('count')

            if allocation_to_be_done == 'food':
                allocation_to_family.updateOrCreateFood(created,count,request.user.shelter)
            elif allocation_to_be_done == 'bedding':
                allocation_to_family.updateOrCreateBedding(created,count,request.user.shelter)
            elif allocation_to_be_done == 'firstaid':
                allocation_to_family.updateOrCreateFirstAid(created,count,request.user.shelter)
            elif allocation_to_be_done == 'water':
                allocation_to_family.updateOrCreateWater(created,count,request.user.shelter)
            return self.form_valid(allocate_at_shelter_form, system_user)

    def form_valid(self, form, form_object):
        # Additional system user registration functionaity here (Maybe an Email??)
        return super(AllocationAtShelterFormView, self).form_valid(form, form_object)

class ShelterRegistrationFormView(FormView):
    template_name = "Admin-Portal/shelter_register.html"
    form_class = ShelterRegistrationForm
    success_url = "/shelter-register/"

    def get_form_kwargs(self):
        logger.info('called get form kwargs')
        kwargs=super(ShelterRegistrationFormView,self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        logger.info('called get context')
        context=super(ShelterRegistrationFormView,self).get_context_data()
        form=self.get_form(self.form_class)
        context['form']=form
        context['time']=timezone.now()
        return context

    def post(self, request, *args, **kwargs):
        shelter_registration_form= ShelterRegistrationForm(request.POST)
        if shelter_registration_form.is_valid():
            Shelter().create(shelter_registration_form)
            return self.form_valid(shelter_registration_form)

    def form_valid(self, form):
        # Additional system user registration functionaity here (Maybe an Email??)
        return super(ShelterRegistrationFormView, self).form_valid(form)

class SupplierFormView(FormView):
    template_name = "supplier_form.html"
    form_class = SupplierForm
    success_url = "/supply-made/"

    def get_form_kwargs(self):
        logger.info('called get form kwargs')
        kwargs=super(SupplierFormView,self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        logger.info('called get context')
        context=super(SupplierFormView,self).get_context_data()
        form=self.get_form(self.form_class)
        context['form']=form
        context['time']=timezone.now()
        return context

    def post(self, request, *args, **kwargs):
        supplier_form= SupplierForm(request.POST)
        if supplier_form.is_valid():
            try:
                food_count = supplier_form.cleaned_data.get('food_count')
                food_required_count = Stocks.objects.aggregate(Sum('food_packets_needed'))
                food_requirement_dict = {}
                for shelter in Shelter.objects.all():
                    try:
                        obj = Stocks.objects.get(shelter=shelter)
                        food_requirement_dict[''+obj.shelter.name] = obj.food_packets_needed
                    except ObjectDoesNotExist:
                        pass
                food_allocation = self.getWeightedDict(food_requirement_dict,food_count)
                for key,value in food_allocation:
                    shelter = Shelter.objects.get(name=key)
                    stock_obj = Stocks.objects.get(shelter=shelter)
                    stock_obj.updateFoodPacketsNeeded(-value)
                    stock_obj.updateFoodPacketsAvailable(value)
            except ObjectDoesNotExist:
                pass
            try:
                first_aid_count = supplier_form.cleaned_data.get('first_aid_count')
                first_aid_required_count = Stocks.objects.aggregate(Sum('first_aid_packets_needed'))
                first_aid_requirement_dict = {}
                for shelter in Shelter.objects.all():
                    try:
                        obj = Stocks.objects.get(shelter=shelter)
                        first_aid_requirement_dict[''+obj.shelter.name] = obj.first_aid_packets_needed
                    except ObjectDoesNotExist:
                        pass
                first_aid_allocation = self.getWeightedDict(first_aid_requirement_dict,food_count)
                for key,value in first_aid_allocation:
                    shelter = Shelter.objects.get(name=key)
                    stock_obj = Stocks.objects.get(shelter=shelter)
                    stock_obj.updateFirstAidPacketsNeeded(-value)
                    stock_obj.updateFirstAidPacketsAvailable(value)
            except ObjectDoesNotExist:
                pass
            try:
                bedding_count = supplier_form.cleaned_data.get('bedding_count')
                bedding_required_count = Stocks.objects.aggregate(Sum('bedding_packets_needed'))
                bedding_requirement_dict = {}
                for shelter in Shelter.objects.all():
                    try:
                        obj = Stocks.objects.get(shelter=shelter)
                        bedding_requirement_dict[''+obj.shelter.name] = obj.bedding_packets_needed
                    except ObjectDoesNotExist:
                        pass
                bedding_allocation = self.getWeightedDict(bedding_requirement_dict,bedding_count)
                for key,value in bedding_allocation:
                    shelter = Shelter.objects.get(name=key)
                    stock_obj = Stocks.objects.get(shelter=shelter)
                    stock_obj.updateBeddingPacketsNeeded(-value)
                    stock_obj.updateBeddingPacketsAvailable(value)
            except ObjectDoesNotExist:
                pass
            try:
                water_count = supplier_form.cleaned_data.get('water_count')
                water_required_count = Stocks.objects.aggregate(Sum('water_needed'))
                water_requirement_dict = {}
                for shelter in Shelter.objects.all():
                    try:
                        obj = Stocks.objects.get(shelter=shelter)
                        water_requirement_dict[''+obj.shelter.name] = obj.water_needed
                    except ObjectDoesNotExist:
                        pass
                water_allocation = self.getWeightedDict(water_requirement_dict,water_count)
                for key,value in water_allocation:
                    shelter = Shelter.objects.get(name=key)
                    stock_obj = Stocks.objects.get(shelter=shelter)
                    stock_obj.updateWaterNeeded(-value)
                    stock_obj.updateWaterAvailable(value)
            except ObjectDoesNotExist:
                pass

            return self.form_valid(supplier_form)

    def form_valid(self, form):
        # Additional system user registration functionaity here (Maybe an Email??)
        return super(SupplierFormView, self).form_valid(form)

    def tsp(self,source):

        shelters = Shelter.objects.all()
        # for shelter in shelters:
        #     shelter = BlockDictComputation().get_nearest_shelter(source.block.x, source.block.y)
        return [shelters]

    def getWeightedDict(self,shelter_dict,distribution_value):
        total = 0.0
        for shelter,value in shelter_dict.iteritems():
            total = total + value
        weighted_dict = {}
        for shelter,value in shelter_dict.iteritems():
            weighted_dict[shelter] = math.floor(distribution_value*value/total)
        return weighted_dict

class Globals():
    response = {}
    response['status'] = 0
    response['data'] = {}
    data = {}
    start_latitude = 6
    end_latitude = 12
    start_longitude = 92
    end_longitude = 94
    degree_to_km = 120
    a_minute_to_km = 2
    block_side = 2
    start_x = 0
    start_y = 0
    temp_blocks = BlocksData.objects.all()
    temp_x = 0
    for block in temp_blocks:
        if block.x < temp_x:
            break
        else:
            temp_x = block.x
    end_x = temp_x
    end_y = (temp_blocks.count())/end_x

    def manhattan_distance(self, sx, sy, ex, ey):
        return abs(ex - sx) + abs(ey - sy)

    def frange(self, start, end=None, inc=None):
        if end == None:
            end = start + 0.0
            start = 0.0
        if inc == None:
            inc = 1.0
        L = []
        while 1:
            next = start + len(L) * inc
            if inc > 0 and next >= end:
                break
            elif inc < 0 and next <= end:
                break
            L.append(next)
        return L

    def success(self,arr):
        response = self.response
        response['status'] = 1
        response['data'] = arr
        return HttpResponse(json.dumps(response), status=200, content_type="application/json")

class PreDRAPComputation(View):

    def get(self,request,*args,**kwargs):
        start_latitude = Globals.start_latitude
        end_latitude = Globals.end_latitude
        start_longitude = Globals.start_longitude
        end_longitude = Globals.end_longitude
        increment = Globals.block_side*1.000000/Globals.degree_to_km

        duplicate_lat = start_latitude
        duplicate_long = start_longitude

        start_time = timezone.now()
        y = 0
        for i in Globals().frange(duplicate_lat, end_latitude + increment, increment):
            x = 0
            for j in Globals().frange(duplicate_long, end_longitude + increment, increment):
                block = BlocksData()
                block.create(i,j,i+increment,j+increment,x,y)
                x = x + 1
            y = y + 1
        end_time = timezone.now()
        return HttpResponse("Start "+str(start_time)+"\nEnd "+str(end_time))

class BlockDictComputation(View):

    def get_nearest_shelter(self, x, y):
        shelters = Shelter.objects.all()
        nearest_shelter = None
        min_dist = BlocksData.objects.all().count()
        for i in range(len(shelters)):
            new_dist = Globals().manhattan_distance(x, y, shelters[i].block.x, shelters[i].block.y)
            if new_dist <= min_dist:
                min_dist = new_dist
                nearest_shelter = shelters[i]

        return nearest_shelter

    def get(self,request,*args,**kwargs):
        increment = Globals.block_side*1.000000/Globals.degree_to_km
        all_blocks = BlocksData.objects.all()
        all_blocks_count = all_blocks.count()
        ending_block = all_blocks[all_blocks_count-1]
        starting_block = all_blocks[0]
        start_y = starting_block.y
        start_x = starting_block.x
        end_y = ending_block.y
        end_x = ending_block.x

        for i in Globals().frange(start_y, end_y + 1, 1):
            for j in Globals().frange(start_x, end_x + 1, 1):
                nearest_shelter = BlockDictComputation().get_nearest_shelter(i,j)
                block = BlocksData.objects.get(x = j, y = i)
                blockDict = BlocksDict()
                blockDict.create(block, nearest_shelter)

        return HttpResponse("Done")

class ExecuteDRAP(View):

    def get(self, request, *args, **kwargs):
        civilians = Civilians.objects.all()
        for civilian in civilians:
            assignShelter(civilian)
        return

    def getNextRadialShelter(self,block_of_civilian,assigned_shelter):
        dist = []
        if block_of_civilian.y is not Globals().end_y:
            t_block = BlocksData(x = block_of_civilian.x, y = ((block_of_civilian.y) + 1) )
            t_shelter = BlocksDict.objects.get(block = t_block).shelter
            dist[0] = Globals().manhattan_distance(t_shelter.block.x, t_shelter.block.y, t_block.x, t_block.y )

        if block_of_civilian.y is not Globals().start_y:
            b_block = BlocksData(x = block_of_civilian.x, y = ((block_of_civilian.y) - 1) )
            b_shelter = BlocksDict.objects.get(block = b_block).shelter
            dist[1] = Globals().manhattan_distance(b_shelter.block.x, b_shelter.block.y, b_block.x, b_block.y )

        if block_of_civilian.x is not Globals().start_x:
            l_block = BlocksData(x = ((block_of_civilian.x) - 1), y = block_of_civilian.y )
            l_shelter = BlocksDict.objects.get(block = l_block).shelter
            dist[2] = Globals().manhattan_distance(l_shelter.block.x, l_shelter.block.y, l_block.x, l_block.y )

        if block_of_civilian.x is not Globals().end_x:
            r_block = BlocksData(x = ((block_of_civilian.x) + 1), y = block_of_civilian.y )
            r_shelter = BlocksDict.objects.get(block = r_block).shelter
            dist[3] = Globals().manhattan_distance(r_shelter.block.x, r_shelter.block.y, r_block.x, r_block.y )

        minimum_dist = 100000
        for i in range(len(dist)):
            if minimum_dist <= dist[i]:
                minimum_dist = dist[i]
                if i == 0:
                    assigned_shelter = t_shelter
                elif i == 1:
                    assigned_shelter = b_shelter
                elif i == 2:
                    assigned_shelter = l_shelter
                else:
                    assigned_shelter = r_shelter
        return assigned_shelter

    def assignShelter(civilian):
        # TODO: Add assisting people count
        if civilian.assigned_shelter is not None:
            threshold = 0.9
            block_of_civilian = civilian.block
            to_be_assigned_shelter = BlocksDict.object.get(block = block_of_civilian).shelter
            if to_be_assigned_shelter.is_full:
                to_be_assigned_shelter = self.getNextRadialShelter(block_of_civilian,to_be_assigned_shelter)
            else:
                civilian.updateAssignedShelter(to_be_assigned_shelter)
                if float((to_be_assigned_shelter.capacity_occupied + to_be_assigned_shelter.expected_capacity)/(to_be_assigned_shelter.total_capacity_of_people)) > threshold:
                    to_be_assigned_shelter.updateIsFull(True)

            message = ""
            Alert().alertForShelterAssigning(civilian,to_be_assigned_shelter,message)
            assignShelter(civilian)
        else:
            return


class test(View):

    def get(self,request,*args,**kwargs):
        # print request.POST.get('device_id')
        devices = FCMDevice.objects.all()
        devices.send_message(title="Title", body="Message")
        devices.send_message(title="Title", body="Message", data={"test": "test"})
        devices.send_message(data={"test": "test"})
        print("sent")
        return HttpResponse(json.dumps({"a":1,"b":2}))
# class Notifications():
#     def notify(devices,message):
#         devices.send_message(title="NotificationTitle", body=""+message)

class Alert():
    # TODO: Get Proper Message
    def alertForShelterAssigning(civilian,shelter,message):
        authkey = '196077A8m64pIIW5a72c40d'
        url = 'http://api.msg91.com/api/sendhttp.php?authkey='+authkey+'&sender=SIHC18&route=4&country=91&message'+message+'&flash=1&unicode=1&mobiles=91'+civilian.contact
        response = urllib2.urlopen(url).read()

        devices = Civilians.objects.get(device_id = civilian.device_id)
        devices.send_message(title="NotificationTitle", body=""+message)
        # Notifications().notify(devices,"notification-body")
        return

'''
API's start here
'''

# Create your views here.
class CivilianViewSet(viewsets.ModelViewSet):

    queryset = Civilians.objects.all()
    serializer_class = CivilianSerializer

class ShelterViewSet(viewsets.ModelViewSet):

    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer

class GetShelters(View):

    def post(self,request,*args,**kwargs):
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        block = BlocksData().get_block(latitude,longitude)
    # if block.in_disaster == True:
    #     nearest_block = BlocksDict.objects.get(block = block).shelter
    #     serialized_block = serialize('json', [nearest_block])
    #     return JsonResponse({'success': True, 'data': json.loads(serialized_block)})
    # else :
        j=0
        shelters = Shelter.objects.all()
        shelter_dict = {}
        for shelter in shelters:
            dist = Globals().manhattan_distance(block.x, block.y, shelter.block.x, shelter.block.y)
            shelter_dict[(shelter.id,dist)] = shelter
        sorted_shelters = sorted(list(shelter_dict.items()), key=lambda x: x[0][1])
        sorted_shelters = [each[1] for each in sorted_shelters]
        logger.info(sorted_shelters)
        #sorted_shelters = {'asd':sorted_shelters}
        serialized_sorted_shelters = serialize('json',sorted_shelters)
        return JsonResponse({'success': True, 'data': json.loads(serialized_sorted_shelters)})

class AddAdHoc(View):

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        request_data = json.loads(body_unicode)

        shelter = Shelter.create(request.POST)

        response_data = {}
        response_data['name'] = request.POST.get('name')
        response_data['total_capacity_of_people'] = request.POST.get('total_capacity_of_people')
        response_data['shelter_latitude'] = request.POST.get('shelter_latitude')
        response_data['shelter_longitude'] = request.POST.get('shelter_longitude')

        return JsonResponse({'success': True, 'data': json.loads(response_data)})

class GetCivilianData(View):
    def post(self, request, *args, **kwargs):
        aadhar_valid = True
        phone_valid = True
        try:
            civilian = Civilians.objects.get(aadhar_number = request.POST.get('aadhar_number'))
        except ObjectDoesNotExist:
            aadhar_valid = False
            try:
                civilian = Civilians.objects.get(contact = request.POST.get('contact'))
            except ObjectDoesNotExist:
                    phone_valid = False
        if not aadhar_valid and not phone_valid:
                return JsonResponse({'success': False})
        return JsonResponse({'success': True, 'data':json.loads(serialize('json',[civilian]))})

'''
API's end here
'''

class MessageHandler(View):

    def shelterAllocator(sender,message,civilian):
        if message[0] == "N" or message[0] == "n":
            pincode = message[1:]
            address = "" + pincode
            api_key = ""# TODO: Add geocoding Api google https://developers.google.com/maps/documentation/geocoding/intro
            api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key='+api_key)
            api_response_dict = api_response.json()

            if api_response_dict['status'] == 'OK':
                latitude = api_response_dict['results'][0]['geometry']['location']['lat']
                longitude = api_response_dict['results'][0]['geometry']['location']['lng']
            shelter = getblocks(latitude, longitude)
            ## TODO get nearest shelter block
            new_message = ""# TODO: Add a message
            Alert().alertForShelterAssigning(civilian,shelter,new_message)

    def post(self,request,*args,**kwargs):
        sender = request.POST.get('number')[3:].strip()
        message = request.POST.get('message').strip()
        civilian = Civilians.objects.get(aadhar_number = request.POST.get('aadhar_number'))

        if 'SHEL' in message:
            message = re.sub('[\s+]', '', message[4:])
            shelterAllocator(sender,message,civilian)

class UserLogout(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('../login/')

# def DemandSupply():
    # fetch available with self
    # fetch required List
    #
    # if sum of required is greater than self:
    #       weighted distribution
    #       forward the request to another supplier
    # else:
    #       assign the required
    # update the requirements for every shelters
    # TSP
