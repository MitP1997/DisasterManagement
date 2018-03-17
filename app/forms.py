from django import forms

class OfficialRegistrationForm(forms.Form):
    """
    Complete form for official registration
    """
    def __init__(self,*args,**kwargs):
        self.system_user=kwargs.pop('system_user',None)
        super(OfficialRegistrationForm,self).__init__(*args,**kwargs)
        self.fields['aadhar_number']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'Aadhar Number of the official'
            }),
            required=True,
            #help_text="Aadhar Number"
        )


class CivilianRegistrationForm(forms.Form):
    """
    Complete form for civilian registration
    """
    def __init__(self,*args,**kwargs):
        self.system_user=kwargs.pop('system_user',None)
        super(CivilianRegistrationForm,self).__init__(*args,**kwargs)
        self.fields['aadhar_number']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'Aadhar Number of the official'
            }),
            required=True,
            #help_text="Aadhar Number"
        )
        self.fields['email']=forms.EmailField(
            max_length=100,
            widget=forms.EmailInput(attrs={
                'title':'Email Id of the Civilian'
            }),
            required=True,
        )
        self.fields['first_name']=forms.CharField(
            max_length=30,
            widget=forms.TextInput(attrs={
                'title':'First Name'
            }),
            #help_text="Gender"
        )
        self.fields['middle_name']=forms.CharField(
            max_length=30,
            widget=forms.TextInput(attrs={
                'title':'Middle Name'
            }),
            required=False,
            #help_text="Gender"
        )
        self.fields['last_name']=forms.CharField(
            max_length=30,
            widget=forms.TextInput(attrs={
                'title':'Last Name'
            }),
            #help_text="Gender"
        )
        self.fields['password']=forms.CharField(
            max_length=30,
            widget=forms.PasswordInput(attrs={
                'title':'Password'
            }),
            #help_text="Gender"
        )
        self.fields['dob']=forms.DateField(
            widget=forms.DateInput(attrs={
                'title':'DOB of the civilian'
            }),
            required=True,
        )
        self.fields['gender']=forms.CharField(
            max_length=1,
            widget=forms.TextInput(attrs={
                'title':'Gender of the Civilian'
            }),
            required=True,
        )
        self.fields['guardians_name']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Guardian of the Civilian'
            }),
            required=True,
        )
        self.fields['contact']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Contact of the Civilian'
            }),
            required=True,
        )
        self.fields['address_line_1']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Address Line 1 of the official'
            }),
            required=True,
            #help_text="Address Line 1"
        )
        self.fields['address_line_2']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Address Line 2 of the official'
            }),
            required=False,
            #help_text="Address Line 2"
        )
        self.fields['address_line_3']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Address Line 3 of the official'
            }),
            required=False,
            #help_text="Address Line 3"
        )
        self.fields['city']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'City'
            }),
            required=True,
            #help_text="Address Line 1"
        )
        self.fields['state']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'State'
            }),
            required=True,
            #help_text="Address Line 2"
        )
        self.fields['country']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Country'
            }),
            required=True,
            #help_text="Address Line 3"
        )
        self.fields['pincode']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'pincode'
            }),
            required=True,
            #help_text="Address Line 3"
        )
        self.fields['blood_group']=forms.CharField(
            widget=forms.TextInput(attrs={
                'title':'Blood Group'
            }),
            required=True,
            #help_text="Address Line 3"
        )
        self.fields['parent_gaurdian']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'parent gaurdian'
            }),
            required=True,
            #help_text="Address Line 3"
        )

class FamilyRegistrationForm(forms.Form):
    """
    Complete form for family registration
    """

    def __init__(self,*args,**kwargs):
        super(FamilyRegistrationForm,self).__init__(*args,**kwargs)
        self.fields['head_name']=forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'title':'Head of the family'
            }),
            required=True,
        )
        self.fields['number_of_members']=forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'title':'Number of family members'
            }),
            required=True,
        )
        self.fields['family_address_line_1']=forms.CharField(
            widget=forms.TextInput(attrs={
                'title':'Address Line 1 of the family'
            }),
            required=True,
        )
        self.fields['family_address_line_2']=forms.CharField(
            widget=forms.TextInput(attrs={
                'title':'Address Line 2 of the family'
            }),
            required=False,
        )
        self.fields['family_address_line_3']=forms.CharField(
            widget=forms.TextInput(attrs={
                'title':'Address Line 3 of the family'
            }),
            required=False,
        )
