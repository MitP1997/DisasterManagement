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
    template_name = 'donationApp/donate_form.html'
    form_class = OfficialRegistrationForm
    success_url = '/registeredSuccessfully/'

    def get_form_kwargs(self):
        logger.info('called get form kwargs')
        kwargs=super(OfficialRegistrationFormView,self).get_form_kwargs()
        try:
            user=UserModel.objects.get(email=self.request.user.email)
            kwargs['user']=user
        except:
            #object does not exist
            raise
        return kwargs

    def get_context_data(self, **kwargs):
        logger.info('called get context')
        context=super(DonationFormView,self).get_context_data()
        form=self.get_form(self.form_class)
        context['form']=form
        FoodItemFormset=formset_factory(FoodItemForm,extra=1, can_delete=True)
        food_formset=FoodItemFormset()
        context['food_formset']=food_formset
        return context

    def post(self, request, *args, **kwargs):
        user = UserModel.objects.get(email=request.user.email)
        logger.info(user)
        donation=DonationModel()
        donor_form= DonorDetailsForm(request.POST,user=user)
        FoodItemFormset=formset_factory(FoodItemForm)
        fooditem_formset=FoodItemFormset(request.POST)

        if donor_form.is_valid() and fooditem_formset.is_valid():
            donation.donor=donor_form.cleaned_data.get('donor_name')
            donation.donor_address=donor_form.cleaned_data.get('donor_address')
            donation.donor_email=user.email
            donation.donor_contact=donor_form.cleaned_data.get('donor_contact')

            food_items={}
            for forms in fooditem_formset:
                food_items[forms.cleaned_data.get('food_name')]=forms.cleaned_data.get('food_quantity')

            donation.donation_items=food_items
            donation.save()

            return self.form_valid(donor_form,donation)

    def form_valid(self, form,donation_object):
        e=EmailMessage()
        e.subject="New Donation Made!"
        e.body="View the detailed donation from {} here: {}".format(form.donor,donation_object.get_absolute_url())
        e.to=UserModel.objects.filter(user_type='receiver')
        e.send()
        return super(DonationFormView, self).form_valid(form)


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
