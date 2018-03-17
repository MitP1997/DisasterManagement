# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# Table Shelter: id, total capacity of people, capacity used, Food packets needed, first aid packets needed

# Table Civilians: all biodata, family ID etc
# Table Users : all bio data, access level
# Table Supplier logs: id, name, quantity supplied, type(food, first aid etc)
# Table Current stock: current food packets, current first aid packets


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
    total_capacity_of_people = models.IntegerField()
    capacity_used =  models.IntegerField()
    food_packets_needed = models.IntegerField()
    first_aid_packets_needed = models.IntegerField()
    shelter_latitude = models.DecimalField(max_digits=9,decimal_places=6)
    shelter_longitude = models.DecimalField(max_digits=9,decimal_places=6)
    shelter_type = models.CharField(max_length=10,choices = SHELTER_TYPE_CHOICES)

class CurrentStock(models.Model):
    current_stock = models.ForeignKey(Shelter)
    food_packets_available = models.IntegerField()
    first_aid_packets_available = models.IntegerField()
    bedding_packets_available = models.IntegerField()
    water_available = models.IntegerField()


class Families(models.Model):
    head_name = models.CharField(max_length=100 )
    number_of_members = models.IntegerField()
    family_address_line_1 = models.CharField(max_length=100)
    family_address_line_2 = models.CharField(max_length=100 , blank = True , null = True)
    family_address_line_3 = models.CharField(max_length=100 , blank = True , null = True)

    def create(self,family_registration_form):
        self.head_name = family_registration_form.cleaned_data.get('head_name')
        self.number_of_members = family_registration_form.cleaned_data.get('number_of_members')
        self.family_address_line_1 = family_registration_form.cleaned_data.get('family_address_line_1')
        self.family_address_line_2 = family_registration_form.cleaned_data.get('family_address_line_2')
        self.family_address_line_3 = family_registration_form.cleaned_data.get('family_address_line_3')
        self.save()

class Civilians(AbstractUser):
    family = models.ForeignKey(Families, null = True, blank = True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank = True, null = True)
    last_name = models.CharField(max_length=30)
    contact = models.IntegerField(blank = True , null = True)
    dob = models.DateField( blank = True , null = True)
    address_line_1 = models.CharField(max_length=100, blank = True , null = True)
    address_line_2 = models.CharField(max_length=100 , blank = True , null = True)
    address_line_3 = models.CharField(max_length=100 , blank = True , null = True)
    gender = models.CharField(max_length=10, choices = GENDER_CHOICES,default='m')
    aadhar_number = models.IntegerField(blank = True , null = True)
    city = models.CharField(max_length=100, null = True, blank = True)
    state = models.CharField(max_length=100, null = True, blank = True)
    country = models.CharField(max_length=100, null = True, blank = True)
    pincode = models.IntegerField(blank = True, null = True)
    blood_group = models.CharField(max_length=100, null = True, blank = True)
    parent_gaurdian = models.CharField(max_length=100, blank = True, null = True)
    current_shelter = models.ForeignKey(Shelter, related_name='current_shelter', null = True, blank = True)
    allocated_shelter = models.ForeignKey(Shelter, related_name='allocated_shelter', null = True, blank = True)

    def create(self,civilian_registration_form):
        self.first_name = civilian_registration_form.cleaned_data.get('first_name')
        self.middle_name = civilian_registration_form.cleaned_data.get('middle_name')
        self.last_name = civilian_registration_form.cleaned_data.get('last_name')
        self.contact = civilian_registration_form.cleaned_data.get('contact')
        self.dob = civilian_registration_form.cleaned_data.get('dob')
        self.email = civilian_registration_form.cleaned_data.get('email')
        self.username = civilian_registration_form.cleaned_data.get('email')
        self.address_line_1 = civilian_registration_form.cleaned_data.get('address_line_1')
        self.address_line_2 = civilian_registration_form.cleaned_data.get('address_line_2')
        self.address_line_3 = civilian_registration_form.cleaned_data.get('address_line_3')
        self.city = civilian_registration_form.cleaned_data.get('city')
        self.state = civilian_registration_form.cleaned_data.get('state')
        self.country = civilian_registration_form.cleaned_data.get('country')
        self.pincode = civilian_registration_form.cleaned_data.get('pincode')
        self.gender = civilian_registration_form.cleaned_data.get('gender')
        self.aadhar_number = civilian_registration_form.cleaned_data.get('aadhar_number')
        self.blood_group = civilian_registration_form.cleaned_data.get('blood_group')
        self.parent_gaurdian = civilian_registration_form.cleaned_data.get('parent_gaurdian')
        self.set_password(civilian_registration_form.cleaned_data.get('password'))
        self.save()

class SystemUsers(models.Model):
    civilian = models.ForeignKey(Civilians)
    shelter = models.ForeignKey(Shelter,blank=True,null=True)
    user_role = models.CharField(max_length=10, choices = ROLE_CHOICES, blank = True , null = True)

    def create(self,registration_form):
        self.civilian=Civilian.objects.get(username = registration_form.cleaned_data.get('email'))
        self.user_role=registration_form.cleaned_data.get('role')
        self.save()

class SupplierLogs(models.Model):
    supplier = models.ForeignKey(SystemUsers)
    quantity_supplied = models.IntegerField()
    supply_type = models.CharField(max_length=10, choices = SUPPLY_TYPE_CHOICES)
