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
    total_capacity_of_people =  models.IntegerField()
    capacity_used =  models.IntegerField()
    food_packets_needed = models.IntegerField()
    first_aid_packets_needed = models.IntegerField()
    shelter_latitude = models.DecimalField()
    shelter_longitude = models.DecimalField()
    shelter_type = #gov or ad-hoc

class SystemUsers(AbstractUser):
    first_name = models.CharField(max_length=100 )
    last_name = models.CharField(max_length=100 )
    contact = models.IntegerField()
    email = models.CharField(max_length=100)
    add_line_1 = models.CharField(max_length=100)
    add_line_2 = models.CharField(max_length=100 , blank = True , null = True)
    add_line_3 = models.CharField(max_length=100 , blank = True , null = True)
    gender =
    aadhar_number = models.IntegerField()
    shelter_id =
    user_role =



class Civilians(models.Model):
    first_name = models.CharField(max_length=100 )
    last_name = models.CharField(max_length=100 )
    contact = models.IntegerField()
    email = models.CharField(max_length=100)
    add_line_1 = models.CharField(max_length=100)
    add_line_2 = models.CharField(max_length=100 , blank = True , null = True)
    add_line_3 = models.CharField(max_length=100 , blank = True , null = True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    gender =
    aadhar_number = models.IntegerField()
    family_id =
    blood_group =
    parent_gaurdian = models.CharField(max_length=100)

class Families(models.Model):
    last_name =
    number_of_members =

class SupplierLogs(models.Model):
    name = models.CharField(max_length=100)
    quantity_supplied = models.CharField(max_length=100)
    supply_type =

class CurrentStock(models.Model):
    food_packets_available = models.IntegerField()
    first_aid_packets_available = models.IntegerField()
