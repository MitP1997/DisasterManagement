from __future__ import unicode_literals
import logging

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from forms import *
from django.views.generic.edit import FormView


from django.forms.formsets import formset_factory
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

# Create your views here.
"""
class DonationListView(ListView):
    queryset = DonationModel.objects.filter(receiver='')
    template_name = 'donationApp/donation_list.html'

class DonationDetailView(DetailView):
    model = DonationModel
    template_name = 'donationApp/donation_detail.html'
"""
class OfficialRegistrationFormView(FormView):
    template_name = 'official_register.html'
    form_class = OfficialRegistrationForm
    success_url = '/official-registered-successfully/'

    def get_form_kwargs(self):
        logger.info('called get form kwargs')
        kwargs=super(OfficialRegistrationFormView,self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        logger.info('called get context')
        context=super(OfficialRegistrationFormView,self).get_context_data()
        form=self.get_form(self.form_class)
        context['form']=form
        return context

    def post(self, request, *args, **kwargs):
        official_registration_form= OfficialRegistrationForm(request.POST)
        if official_registration_form.is_valid():
            system_user=SystemUsers()
            system_user.create(official_registration_form)
            return self.form_valid(official_registration_form,system_user)

    def form_valid(self, form,form_object):
        # Additional system user registration functionaity here (Maybe an Email??)
        return super(OfficialRegistrationFormView, self).form_valid(form)

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

class FamilyRegistrationFormView(FormView):
    template_name = 'family_register.html'
    form_class = FamilyRegistrationForm
    success_url = '/family-registered-successfully/'

    def get_form_kwargs(self):
        logger.info('called get form kwargs')
        kwargs=super(FamilyRegistrationFormView,self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        logger.info('called get context')
        context=super(FamilyRegistrationFormView,self).get_context_data()
        form=self.get_form(self.form_class)
        context['form']=form
        return context

    def post(self, request, *args, **kwargs):
        family_registration_form= FamilyRegistrationForm(request.POST)

        if family_registration_form.is_valid():
            family=Families()
            family.create(family_registration_form)
            return self.form_valid(family_registration_form,family)

    def form_valid(self, form,form_object):
        # Additional system user registration functionaity here (Maybe an Email??)
        return super(FamilyRegistrationFormView, self).form_valid(form)

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
#
# class Civilian():
#     data = {}
#
#     def __init__(self):
#         self.data = {}
#
#     def registerFamily(self,request):
#         if request.method == "GET":
#             return render(request,'register_family.html')
#         else:
#             family = Families()
#             family.create(request.POST) # This function is to reduce the LOC here in views.py
#             if request.POST.get('api') is not None:
#                 self.data['family_id'] = family.id
#                 response = Globals().success(self.data)
#             else:
#                 response = redirect('register-family')
#             return response
#
#     def registerCivilian(self,request):
#         if request.method == "GET":
#             return render(request,'register_civilian.html')
#         else:
#             civilian = Civilians()
#             civilian.create(request.POST)
#             if request.POST.get('api') is not None:
#                 self.data['civilian_id'] = civilian.id
#                 response = Globals().success(self.data)
#             else:
#                 response = redirect('register-civilian')
#             return response


def DemandSupply():
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
