from django import forms
from django.contrib.auth import login
from django.contrib import auth


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

class CivilianRegistrationForm(forms.Form):
    """
    Complete form for civilian registration
    """
    def __init__(self,*args,**kwargs):
        self.system_user=kwargs.pop('system_user',None)
        super(CivilianRegistrationForm,self).__init__(*args,**kwargs)
        self.fields['family_id']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'Family ID'
            }),
            required=False,
        )
        self.fields['aadhar_number']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'Aadhar Number'
            }),
            required=True,
        )
        self.fields['first_name']=forms.CharField(
            max_length=30,
            widget=forms.TextInput(attrs={
                'title':'First Name'
            }),
        )
        self.fields['middle_name']=forms.CharField(
            max_length=30,
            widget=forms.TextInput(attrs={
                'title':'Middle Name'
            }),
            required=False,
        )
        self.fields['last_name']=forms.CharField(
            max_length=30,
            widget=forms.TextInput(attrs={
                'title':'Last Name'
            }),
        )
        self.fields['contact']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Contact '
            }),
            required=True,
        )
        self.fields['dob']=forms.DateField(
            widget=forms.DateInput(attrs={
                'title':'Date of Birth'
            }),
            required=True,
        )
        self.fields['gender']=forms.CharField(
            max_length=10,
            widget=forms.Select(choices = GENDER_CHOICES, attrs={
                'title':'Gender'
            }),
        )
        self.fields['blood_group']=forms.CharField(
            widget=forms.TextInput(attrs={
                'title':'Blood Group'
            }),
            required=True,
        )
        self.fields['address_line_1']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Address Line 1'
            }),
            required=True,
        )
        self.fields['address_line_2']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Address Line 2'
            }),
            required=False,
        )
        self.fields['address_line_3']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Address Line 3 '
            }),
            required=False,
        )
        self.fields['city']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'City'
            }),
            required=True,
        )
        self.fields['state']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'State'
            }),
            required=True,
        )
        self.fields['country']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Country'
            }),
            required=True,
        )
        self.fields['pincode']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'Pincode'
            }),
            required=True,
        )
        self.fields['latitude']=forms.DecimalField(
            widget=forms.NumberInput(attrs={
                'title':'Latitude'
            }),
            required=True,
        )
        self.fields['longitude']=forms.DecimalField(
            widget=forms.NumberInput(attrs={
                'title':'Longitude'
            }),
            required=True,
        )

class SystemUserRegistrationForm(forms.Form):
    """
    Complete form for official registration
    """
    def __init__(self,*args,**kwargs):
        self.system_user=kwargs.pop('system_user',None)
        super(SystemUserRegistrationForm,self).__init__(*args,**kwargs)
        self.fields['aadhar_number']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'Aadhar Number'
            }),
            required=True,
        )
        self.fields['password']=forms.CharField(
            widget=forms.PasswordInput(attrs={
                'title':'Password'
            }),
            required=True,
        )
        self.fields['confirm_password']=forms.CharField(
            widget=forms.PasswordInput(attrs={
                'title':'Confirm Password'
            }),
            required=True,
        )

    def clean(self):
        cleaned_data = super(SystemUserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class CivilianAtShelterForm(forms.Form):
    """
    Complete form for civilian at shelter
    """
    def __init__(self,*args,**kwargs):
        self.system_user=kwargs.pop('system_user',None)
        super(CivilianAtShelterForm,self).__init__(*args,**kwargs)
        self.fields['aadhar_number']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'Aadhar Number'
            }),
            required=False,
        )
        self.fields['mobile_number']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'Mobile Number'
            }),
            required=False,
        )

    def clean(self):
        cleaned_data = super(CivilianAtShelterForm, self).clean()
        try:
            aadhar_number = cleaned_data.get("aadhar_number")
        except ObjectDoesNotExist:
            pass
        try:
            mobile_number = cleaned_data.get("mobile_number")
        except ObjectDoesNotExist:
            pass
        if (aadhar_number is None) and (mobile_number is None): # both were not entered
            raise forms.ValidationError("Enter either of the data")

        return cleaned_data

class CivilianAllocationForm(forms.Form):
    """
    Complete form for civilian at shelter
    """
    def __init__(self,*args,**kwargs):
        self.system_user=kwargs.pop('system_user',None)
        super(CivilianAtShelterForm,self).__init__(*args,**kwargs)
        self.fields['aadhar_number']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'Aadhar Number'
            }),
            required=False,
        )
        self.fields['mobile_number']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'Mobile Number'
            }),
            required=False,
        )
        self.fields['count'] = forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'Total packets given'
            }),
            required=True,
        )

class LoginForm(forms.Form):
    """
    Complete form for login of system users
    """
    def __init__(self,*args,**kwargs):
        self.system_user=kwargs.pop('system_user',None)
        super(LoginForm,self).__init__(*args,**kwargs)
        self.fields['aadhar_number']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'Aadhar Number'
            }),
            required=True,
        )
        self.fields['password']=forms.CharField(
            widget=forms.PasswordInput(attrs={
                'title':'Password'
            }),
            required=True,
        )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("aadhar_number")
        password = cleaned_data.get("password")
        user = auth.authenticate(username=cleaned_data.get('aadhar_number'), password=cleaned_data.get('password'))
        if user is None:
            raise forms.ValidationError("Invalid Login")

        return cleaned_data
