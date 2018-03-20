from django import forms


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
