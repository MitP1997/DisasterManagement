from django import forms

class FamilyRegisterationForm(forms.Form):
    last_name = forms.CharField(
        label='Last Name',
        max_length=100,
        required=True )
    number_of_members = forms.IntegerField(
        label='Number of members',
        required=True )

class OfficialRegistrationForm(forms.Form):
    """
    Complete form for official registration
    """
    def __init__(self,*args,**kwargs):
        self.system_user=kwargs.pop('system_user',None)
        super(OfficialRegistrationForm,self).__init__(*args,**kwargs)
        self.fields['aadhar_number']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Aadhar Number of the official'
            }),
            # initial=self.user.name,
            required=True,
            help_text="DOB"
        )

        self.fields['gender']=forms.CharField(
            max_length=1,
            widget=forms.TextInput(attrs={
                'title':'Gender of the official'
            }),
            help_text="Gender"
        )
        self.fields['contact']=forms.IntegerField(
            max_length=100,
            widget=forms.NumberInput(attrs={
                'title':'Phone Number of the official '
            }),
            required=True,
            help_text="Guardian's Name"
        )
        self.fields['address_line_1']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Address Line 1 of the official'
            }),
            required=True,
            help_text="Address Line 1"
        )
        self.fields['address_line_2']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Address Line 2 of the official'
            }),
            help_text="Address Line 2"
        )
        self.fields['address_line_2']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Address Line 3 of the official'
            }),
            help_text="Address Line 3"
        )

class CivilianRegistrationForm(forms.Form):
    """
    Complete form for civilian registration
    """
    def __init__(self,*args,**kwargs):
        self.system_user=kwargs.pop('system_user',None)
        super(CivilianRegistrationForm,self).__init__(*args,**kwargs)
        self.fields['dob']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'DOB of the civilian'
            }),
            required=True,
            help_text="DOB"
        )
        self.fields['gender']=forms.CharField(
            max_length=1,
            widget=forms.TextInput(attrs={
                'title':'Gender of the Civilian'
            }),
            required=True,
            help_text="Gender"
        )
        self.fields['guardians_name']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Guardian of the Civilian'
            }),
            required=True,
            help_text="Guardian's Name"
        )
        self.fields['contact']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Contact of the Civilian'
            }),
            required=True,
            help_text="Contact Number"
        )
        self.fields['email']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Email Id of the Civilian'
            }),
            required=True,
            help_text="Email Id"
        )
