from django.db import models
from datetime import datetime
from django import forms

class Member(models.Model):
    first = models.CharField(max_length=200)
    last = models.TextField(null=True)
    number = models.TextField(null=True)
    email = models.TextField(null=True)
    role = models.CharField(choices=[('admin', 'Admin - can delete members'), ('regular', 'Regular - cant delete members')], max_length=200, null=True)

    b = models.CharField(max_length=7, default='0000000', editable=False)
    created_at = models.DateTimeField( default=datetime.now())

    def __str__(self):
        return self.first 

 

    class Meta:
        ordering = ['created_at']


class MemberForm(forms.ModelForm):
    
    role = forms.ChoiceField(choices=Member._meta.get_field('role').choices, widget=forms.RadioSelect(attrs={'class': 'role-select'})
)

    class Meta:
        model = Member
        fields = ['first', 'last', 'number', 'email', 'role']
        widgets = {
            'first': forms.TextInput(attrs={'size': 40, 'class': 'form-field', 'placeholder': 'First Name'}),
            'last': forms.TextInput(attrs={'size': 40, 'class': 'form-field', 'placeholder': 'Last Name'}),
            'number': forms.TextInput(attrs={'size': 40, 'class': 'form-field', 'placeholder': 'Phone Number'}),
            'email': forms.TextInput(attrs={'size': 40, 'class': 'form-field', 'placeholder': 'Email Address'}),
            'role': forms.RadioSelect(attrs={'class': 'role-select', 'label_class': 'role-label'}),
        }
      
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # check if this is a new instance (no primary key yet)
            self.initial['role'] = 'regular'  # set the default value of the role field to "regular"
        self.fields['first'].label = False  # set label to False for the first field
        self.fields['last'].label = False  # set label to False for the last field
        self.fields['number'].label = False  # set label to False for the number field
        self.fields['email'].label = False  # set label to False for the email field
        self.fields['role'].label = 'Role'



