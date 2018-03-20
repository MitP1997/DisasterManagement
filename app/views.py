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
"""

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
