# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django_extensions.db.models import TimeStampedModel
from fcm_django.models import FCMDevice

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

class BlocksData(models.Model):
    start_latitude = models.FloatField()
    start_longitude = models.FloatField()
    end_latitude = models.FloatField()
    end_longitude = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    x = models.IntegerField()
    y = models.IntegerField()

    def get_block(self, latitude, longitude):
        block = BlocksData.objects.get(start_latitude__lte = latitude ,start_longitude__lte = longitude, end_latitude__gte = latitude, end_longitude__gte = longitude )
        return block

    def create(self,start_lat,start_long,end_lat,end_long,x,y):
        self.start_latitude = start_lat
        self.start_longitude = start_long
        self.end_latitude = end_lat
        self.end_longitude = end_long
        self.latitude = (start_lat + end_lat)*1.000000/2
        self.longitude = (start_long + end_long)*1.000000/2
        self.x = x
        self.y = y
        self.save()


class Shelter(models.Model):
    name = models.CharField(max_length=100)
    total_capacity_of_people = models.IntegerField()
    # TODO: Add active feild and expecte capacity
    capacity_occupied =  models.IntegerField(default=0)
    shelter_latitude = models.DecimalField(max_digits=9,decimal_places=6)
    shelter_longitude = models.DecimalField(max_digits=9,decimal_places=6)
    shelter_type = models.CharField(max_length=10,choices = SHELTER_TYPE_CHOICES,default='g')
    block = models.ForeignKey(BlocksData, blank = True, null = True)

    # def save(self):
    #     self.block = BlocksData().get_block(self.shelter_latitude, self.shelter_longitude)
    #     super(Shelter,self).save()

    def create(self,shelter_form):
        self.name = shelter_form.cleaned_data.get('name')
        self.total_capacity_of_people = shelter_form.cleaned_data.get('total_capacity_of_people')
        self.shelter_latitude = shelter_form.cleaned_data.get('shelter_latitude')
        self.shelter_longitude = shelter_form.cleaned_data.get('shelter_longitude')
        self.block = BlocksData().get_block(shelter_form.cleaned_data.get('shelter_latitude'), shelter_form.cleaned_data.get('shelter_longitude'))
        self.save()


    def updateOccupiedCapacity(self,capacity):
        self.capacity_occupied = self.capacity_occupied + capacity
        self.save()

    def updateTotalCapacity(self,capacity):
        self.total_capacity_of_people = self.total_capacity_of_people + capacity
        self.save()

class BlocksDict(models.Model):
    block = models.ForeignKey(BlocksData)
    shelter = models.ForeignKey(Shelter, blank = True, null = True)

    def create(self,block,shelter):
        self.block = block
        self.shelter = shelter
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
    assigned_shelter = models.ForeignKey(Shelter, related_name='assigned_shelter', null = True, blank = True)
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    longitude = models.DecimalField(max_digits=9,decimal_places=6)
    block = models.ForeignKey(BlocksData, blank = True, null = True)
    # TODO: Add devceId

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
        self.latitude = civilian_registration_form.cleaned_data.get('latitude')
        self.longitude = civilian_registration_form.cleaned_data.get('longitude')
        self.block = BlocksData().get_block(civilian_registration_form.cleaned_data.get('latitude'), civilian_registration_form.cleaned_data.get('longitude'))
        self.save()

    def updateAssignedShelter(self,shelter):
        self.assigned_shelter = shelter
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
