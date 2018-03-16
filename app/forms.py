from django import forms

class FamilyRegister(forms.Form):
    last_name = forms.CharField(label='Last Name',max_length=100 )
    number_of_members = forms.IntegerField(label='Number of members')
