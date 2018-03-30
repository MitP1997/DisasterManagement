from __future__ import unicode_literals
import logging

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from .models import *
from forms import *
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
import urllib2
import json
from fcm_django.models import FCMDevice

from django.forms.formsets import formset_factory

from django.contrib.auth import login, logout
from django.contrib import auth


logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

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
        context["Civilians"] = Civilians.objects.filter(current_shelter=Shelter.objects.get(id=self.kwargs.get('pk')))
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
    paginate_by = 5
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
    success_url = '/civilian-registered-successfully/'

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
    success_url = "/system-user-registered-successfully/"

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
    success_url = "/registered-at-shelter-successfully/"

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
        print context
        return context

    def post(self, request, *args, **kwargs):
        allocate_at_shelter_form= CivilianAllocationForm(request.POST)
        if allocate_at_shelter_form.is_valid():
            try:
                civilian = Civilians.objects.get(aadhar_number=allocate_at_shelter_form.cleaned_data.get('aadhar_number'))
            except ObjectDoesNotExist:
                civilian = Civilians.objects.get(contact=allocate_at_shelter_form.cleaned_data.get('mobile_number'))
            # get or create on AllocationToFamilies for civilian.family
            allocation_to_family, created = AllocationToFamilies.objects.get_or_create(family=civilian.family)

            length = len(request.get_full_path().split("/"))
            allocation_to_be_done = request.get_full_path().split("/")[length-2]

            count = allocate_at_shelter_form.cleaned_data.get('count')

            if allocation_to_be_done == 'food':
                allocation_to_family.updateOrCreateFood(created,count)
            elif allocation_to_be_done == 'bedding':
                allocation_to_family.updateOrCreateBedding(created,count)
            elif allocation_to_be_done == 'firstaid':
                allocation_to_family.updateOrCreateFirstAid(created,count)
            elif allocation_to_be_done == 'water':
                allocation_to_family.updateOrCreateWater(created,count)
            return self.form_valid(allocate_at_shelter_form, system_user)

    def form_valid(self, form, form_object):
        # Additional system user registration functionaity here (Maybe an Email??)
        return super(AllocationAtShelterFormView, self).form_valid(form, form_object)

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

    def assignShelter(civilian):
        block_of_civilian = civilian.block
        assigned_shelter = BlocksDict.object.get(block = block_of_civilian).shelter
        civilian.updateAssignedShelter(assigned_shelter)
        message = ""
        Alert().alertForShelterAssigning(civilian,assigned_shelter,message)

class Notifications():
    def notify(devices,msg_body):
        devices.send_message(title="NotificationTitle", body=""+msg_body)

class Alert():
    def alertForShelterAssigning(civilian,shelter,message):
        url = 'http://api.msg91.com/api/sendhttp.php?authkey=196077A8m64pIIW5a72c40d&sender=SIHC18&route=4&country=91&message'+message+'&flash=1&unicode=1&mobiles=91'+civilian.contact
        response = urllib2.urlopen(url).read()
        devices = Civilians.objects.get(device_id = civilian.device_id)
        Notifications().notify(devices,"notification-body")
        return

def userLogout(request):
    if request.user.is_authenticated():
        logout(request)
        return redirect('../login/')
    else:
        return HttpResponseRedirect('../login/')

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
