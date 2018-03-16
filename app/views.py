import logging

from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import *

from forms import OfficialRegistrationForm, CivilianRegistrationForm
from django.forms.formsets import formset_factory
from django.views.generic.edit import FormView

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

# Create your views here.
class DonationListView(ListView):
    queryset = DonationModel.objects.filter(receiver='')
    template_name = 'donationApp/donation_list.html'

class DonationDetailView(DetailView):
    model = DonationModel
    template_name = 'donationApp/donation_detail.html'

class OfficialRegistrationFormView(FormView):
    template_name = 'html_official_register.html'
    form_class = OfficialRegistrationForm
    success_url = '/OfficialRegisteredSuccessfully/'

    def get_form_kwargs(self):
        logger.info('called get form kwargs')
        kwargs=super(OfficialRegistrationFormView,self).get_form_kwargs()
        try:
            system_user=SystemUsers.objects.get(email=self.request.user.email)
            kwargs['system_user']=system_user
        except:
            #object does not exist
            raise
        return kwargs

    def get_context_data(self, **kwargs):
        logger.info('called get context')
        context=super(OfficialRegistrationFormView,self).get_context_data()
        form=self.get_form(self.form_class)
        context['form']=form
        # FoodItemFormset=formset_factory(FoodItemForm,extra=1, can_delete=True)
        # food_formset=FoodItemFormset()
        # context['food_formset']=food_formset
        return context

    def post(self, request, *args, **kwargs):
        system_user = SystemUser.objects.get(email=request.user.email)
        logger.info(user)
        system_user=SystemUser()
        # official_registeration_form= OfficialRegistrationForm(request.POST,user=user)
        official_registeration_form= OfficialRegistrationForm(request.POST,user=user)

        if official_registeration_form.is_valid():
            system_user.name=official_registeration_form.cleaned_data.get('name')
            system_user.email=official_registeration_form.cleaned_data.get('email')
            system_user.password=official_registeration_form.cleaned_data.get('password')
            system_user.aadhar_number=official_registeration_form.cleaned_data.get('aadhar_number')
            system_user.dob=official_registeration_form.cleaned_data.get('dob')
            system_user.gender=official_registeration_form.cleaned_data.get('gender')
            system_user.contact=official_registeration_form.cleaned_data.get('contact')
            system_user.address_line_1=official_registeration_form.cleaned_data.get('address_line_1')
            system_user.address_line_2=official_registeration_form.cleaned_data.get('address_line_2')
            system_user.address_line_3=official_registeration_form.cleaned_data.get('address_line_3')
            system_user.save()

            return self.form_valid(official_registeration_form,system_user)

    def form_valid(self, form,donation_object):
        # Additional system user registration functionaity here (Maybe an Email??)
        return super(OfficialRegistrationFormView, self).form_valid(form)


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
