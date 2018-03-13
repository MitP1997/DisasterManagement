# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# Table Shelter: id, total capacity of people, capacity used, Food packets needed, first aid packets needed

# Table Civilians: all biodata, family ID etc
# Table Users : all bio data, access level
# Table Supplier logs: id, name, quantity supplied, type(food, first aid etc)
# Table Current stock: current food packets, current first aid packets

class Shelter(models.Model):
    current_stock = models.ForeignKey(CurrentStock)
    total_capacity_of_people =  models.IntegerField()
    capacity_used =  models.IntegerField()
    food_packets_needed = models.IntegerField()
    first_aid_packets_needed = models.IntegerField()
    shelter_latitude = models.DecimalField()
    shelter_longitude = models.DecimalField()
    shelter_type = models.CharField(choices = SHELTER_TYPE_CHOICES)

    SHELTER_TYPE_CHOICES =(
        ('g','government'),
        ('a','ad-hoc'),
    )

class CurrentStock(models.Model):
    food_packets_available = models.IntegerField()
    first_aid_packets_available = models.IntegerField()
    bedding_packets_available = models.IntegerField()
    water_available = models.IntegerField()

class SystemUsers(AbstractUser):
    shelter_id = models.ForeignKey(Shelter)
    first_name = models.CharField(max_length=100 )
    last_name = models.CharField(max_length=100 )
    contact = models.IntegerField()
    email = models.CharField(max_length=100)
    add_line_1 = models.CharField(max_length=100)
    add_line_2 = models.CharField(max_length=100 , blank = True , null = True)
    add_line_3 = models.CharField(max_length=100 , blank = True , null = True)
    gender = models.CharField( choices = GENDER_CHOICES)
    aadhar_number = models.IntegerField()
    user_role = models.CharField( choices = ROLE_CHOICES)

    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    ROLE_CHOICES = (
        ('a', 'Admin'),
        ('o', 'Operator'),
        ('s', 'Supplier'),
    )

class Civilians(models.Model):
    family_id = models.ForeignKey(Families)
    current_shelter = models.ForeignKey(Shelter)
    allocated_shelter = models.ForeignKey(Shelter)
    first_name = models.CharField(max_length=100 )
    last_name = models.CharField(max_length=100 )
    contact = models.IntegerField()
    email = models.CharField(max_length=100)
    add_line_1 = models.CharField(max_length=100)
    add_line_2 = models.CharField(max_length=100, blank = True, null = True)
    add_line_3 = models.CharField(max_length=100, blank = True, null = True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    gender = models.CharField(choices = GENDER_CHOICES)
    aadhar_number = models.IntegerField()
    blood_group = models.CharField(max_length=100)
    parent_gaurdian = models.CharField(max_length=100)

    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )

class Families(models.Model):
    last_name = last_name = models.CharField(max_length=100 )
    number_of_members = contact = models.IntegerField()

class SupplierLogs(models.Model):
    name = models.CharField(max_length=100)
    quantity_supplied = models.IntegerField()
    supply_type = models.CharField( choices = SUPPLY_TYPE_CHOICES)

    SUPPLY_TYPE_CHOICES = (
        ('fp','food_packet'),
        ('fa','first_aid'),
        ('b','beddings'),
        ('w','water'),
    )
