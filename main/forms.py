# from dataclasses import fields
# from tkinter import Widget
# from django import forms
# from .models import Person, Family, SpouseInfo

# class PersonForm(forms.ModelForm):
#     class Meta:
#         model = Person
#         fields = ['name', 'dob','gender']
#         widgets =   {
#                         'name' : forms.TextInput(attrs={'class':'form-field d-flex align-items-center', 'type':'text'}),
#                         'dob' : forms.DateInput(attrs={'class':'form-field d-flex align-items-center', 'type':'date'}),
#                         'gender' : forms.Select(attrs={'class':'form-field d-flex align-items-center', 'type':'select'}, choices=(['{{ model.person.gender }}'])),
#                     }
# class FamilyForm(forms.ModelForm):
#     class Meta:
#         model = Family
#         fields = ['father', 'mother', 'children']
#         widgets = {
#                     'father':forms.Select(attrs={'class':'form-field d-flex align-items-center', 'type':'select'},choices=(['{{ model.father }}'])),
#                     'mother':forms.Select(attrs={'class':'form-field d-flex align-items-center', 'type':'select'},choices=(['{{ model.mother }}'])),
#                     'children':forms.SelectMultiple(attrs={'class':'form-field d-flex align-items-center', 'type':'select'},choices=(['{{ model.children }}'])),
#         }
# class SpouseInfoForm(forms.ModelForm):
#     class Meta:
#         model = SpouseInfo
#         fields = ['person', 'spouse_name', 'spouse_fathername', 'spouse_village']
#         widgets = {
#             'person': forms.Select(attrs={'class':'form-field d-flex align-items-center', 'type':'select'},choices=(['{{ model.spouse_name }}'])),
#             'spouse_name': forms.TextInput(attrs={'class': 'form-field d-flex align-items-center', 'type': 'text'}),
#             'spouse_fathername': forms.TextInput(attrs={'class': 'form-field d-flex align-items-center', 'type': 'text'}),
#             'spouse_village': forms.TextInput(attrs={'class': 'form-field d-flex align-items-center', 'type': 'text'}),

#         }

#         }

# from django import forms
# class FilePathForm(forms.Form):
#     file_path = forms.CharField(label='File Path', max_length=255)