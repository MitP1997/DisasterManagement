# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django_extensions.db.models import TimeStampedModel

SHELTER_TYPE_CHOICES =(
    ('g','government'),
    ('a','ad-hoc'),
)

GENDER_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('o', 'Other'),
)

ROLE_CHOICES = (
    ('a', 'Admin'),
    ('o', 'Operator'),
    ('s', 'Supplier'),
)

SUPPLY_TYPE_CHOICES = (
    ('fp','food_packet'),
    ('fa','first_aid'),
    ('b','beddings'),
    ('w','water'),
)

class Shelter(models.Model):
    name = models.CharField(max_length=100)
    total_capacity_of_people = models.IntegerField()
    capacity_occupied =  models.IntegerField(default=0)
    shelter_latitude = models.DecimalField(max_digits=9,decimal_places=6)
    shelter_longitude = models.DecimalField(max_digits=9,decimal_places=6)
    shelter_type = models.CharField(max_length=10,choices = SHELTER_TYPE_CHOICES,default='g')

    def create(self,shelter_form):
        self.name = shelter_form.cleaned_data.get('name')
        self.total_capacity_of_people = shelter_form.cleaned_data.get('total_capacity_of_people')
        self.shelter_latitude = shelter_form.cleaned_data.get('shelter_latitude')
        self.shelter_longitude = shelter_form.cleaned_data.get('shelter_longitude')
        self.save()

    def updateOccupiedCapacity(self,capacity):
        self.capacity_occupied = self.capacity_occupied + capacity
        self.save()

    def updateTotalCapacity(self,capacity):
        self.total_capacity_of_people = self.total_capacity_of_people + capacity
        self.save()

class Stocks(models.Model):
    shelter = models.ForeignKey(Shelter)
    food_packets_available = models.IntegerField()
    food_packets_needed = models.IntegerField(default=0)
    first_aid_packets_available = models.IntegerField()
    first_aid_packets_needed = models.IntegerField(default=0)
    bedding_packets_available = models.IntegerField()
    bedding_packets_needed = models.IntegerField(default=0)
    water_available = models.IntegerField()
    water_needed = models.IntegerField(default=0)

    def create(self,stock_form):
        self.shelter = Shelter.objects.get(id=stock_form.cleaned_data.get('shelter_id'))
        self.food_packets_available = stock_form.cleaned_data.get('food_packets_available')
        self.first_aid_packets_available = stock_form.cleaned_data.get('first_aid_packets_available')
        self.bedding_packets_available = stock_form.cleaned_data.get('bedding_packets_available')
        self.water_available = stock_form.cleaned_data.get('water_available')
        self.save()

    def updateFoodPacketsNeeded(self,quantity):
        self.food_packets_needed=self.food_packets_needed+quantity
        self.save()

    def updateFirstAidPacketsNeeded(self,quantity):
        self.first_aid_packets_needed=self.first_aid_packets_needed+quantity
        self.save()

    def updateBeddingPacketsNeeded(self,quantity):
        self.bedding_packets_needed=self.bedding_packets_needed+quantity
        self.save()

    def updateWaterNeeded(self,quantity):
        self.water_needed=self.water_needed+quantity
        self.save()

    def updateFoodPacketsAvailable(self,quantity):
        self.food_packets_available=self.food_packets_available+quantity
        self.save()

    def updateFirstAidPacketsAvailable(self,quantity):
        self.first_aid_packets_available=self.first_aid_packets_available+quantity
        self.save()

    def updateBeddingPacketsAvailable(self,quantity):
        self.bedding_packets_available=self.bedding_packets_available+quantity
        self.save()

    def updateWaterAvailable(self,quantity):
        self.water_available=self.water_available+quantity
        self.save()

class Families(models.Model):
    last_name = models.CharField(max_length=30)
    number_of_members = models.IntegerField(default = 1)

    def create(self,last_name):
        self.last_name = last_name
        self.save()

    def updateCount(self):
        self.number_of_members = self.number_of_members+1
        self.save()

class Civilians(models.Model):
    family = models.ForeignKey(Families)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank = True, null = True)
    last_name = models.CharField(max_length=30)
    contact = models.IntegerField()
    dob = models.DateField()
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100 , blank = True , null = True)
    address_line_3 = models.CharField(max_length=100 , blank = True , null = True)
    gender = models.CharField(max_length=10, choices = GENDER_CHOICES,default='m')
    aadhar_number = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.IntegerField()
    blood_group = models.CharField(max_length=100)
    current_shelter = models.ForeignKey(Shelter, related_name='current_shelter', null = True, blank = True)
    allocated_shelter = models.ForeignKey(Shelter, related_name='allocated_shelter', null = True, blank = True)

    def create(self,civilian_registration_form):
        try:
            self.family = Families.objects.get(id=civilian_registration_form.cleaned_data.get('family_id'))
            self.family.updateCount()
        except ObjectDoesNotExist:
            family = Families()
            family.create(civilian_registration_form.cleaned_data.get('last_name'))
            self.family = family
        self.first_name = civilian_registration_form.cleaned_data.get('first_name')
        if civilian_registration_form.cleaned_data.get('middle_name') is not None:
            self.middle_name = civilian_registration_form.cleaned_data.get('middle_name')
        self.last_name = civilian_registration_form.cleaned_data.get('last_name')
        self.contact = civilian_registration_form.cleaned_data.get('contact')
        self.dob = civilian_registration_form.cleaned_data.get('dob')
        self.address_line_1 = civilian_registration_form.cleaned_data.get('address_line_1')
        if civilian_registration_form.cleaned_data.get('address_line_2') is not None:
            self.address_line_2 = civilian_registration_form.cleaned_data.get('address_line_2')
        if civilian_registration_form.cleaned_data.get('address_line_3') is not None:
            self.address_line_3 = civilian_registration_form.cleaned_data.get('address_line_3')
        self.gender = civilian_registration_form.cleaned_data.get('gender')
        self.aadhar_number = civilian_registration_form.cleaned_data.get('aadhar_number')
        self.city = civilian_registration_form.cleaned_data.get('city')
        self.state = civilian_registration_form.cleaned_data.get('state')
        self.country = civilian_registration_form.cleaned_data.get('country')
        self.pincode = civilian_registration_form.cleaned_data.get('pincode')
        self.blood_group = civilian_registration_form.cleaned_data.get('blood_group')
        self.save()

    def updateCurrentShelter(self,shelter):
        self.current_shelter = shelter
        self.save()

class SystemUsers(AbstractUser):
    civilian = models.ForeignKey(Civilians, blank = True, null = True)
    shelter = models.ForeignKey(Shelter,blank=True,null=True)
    user_role = models.CharField(max_length=10, choices = ROLE_CHOICES, blank = True , null = True)

    def create(self,registration_form,role):
        self.civilian=Civilians.objects.get(aadhar_number=registration_form.cleaned_data.get('aadhar_number'))
        self.user_role = role
        self.username = registration_form.cleaned_data.get('aadhar_number')
        self.set_password(registration_form.cleaned_data.get('password'))
        self.save()

class SupplierLogs(models.Model):
    supplier = models.ForeignKey(SystemUsers)
    quantity_supplied = models.IntegerField()
    supply_type = models.CharField(max_length=10, choices = SUPPLY_TYPE_CHOICES)

    def create(self,log_dict):
        self.supplier = SystemUsers.objects.get(id=log_dict['supplier_id'])
        self.quantity_supplied = log_dict['quantity_supplied']
        self.supply_type = log_dict['supply_type']
        self.save()

class AllocationToFamilies(TimeStampedModel):
    family = models.ForeignKey(Families)
    given_food_packets_count = models.IntegerField(default=0)
    given_bedding_packets_count = models.IntegerField(default=0)
    given_firstaid_packets_count = models.IntegerField(default=0)
    given_water_packets_count = models.IntegerField(default=0)

    def updateOrCreateFood(self,created,count):
        self.given_food_packets_count = self.given_food_packets_count + count
        self.save()

    def updateOrCreateBedding(self,created,count):
        self.given_bedding_packets_count = self.given_bedding_packets_count + count
        self.save()

    def updateOrCreateFirstAid(self,created,count):
        self.given_firstaid_packets_count = self.given_firstaid_packets_count + count
        self.save()

    def updateOrCreateWater(self,created,count):
        self.given_water_packets_count = self.given_water_packets_count + count
        self.save()
