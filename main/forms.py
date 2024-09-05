from random import choices
from typing import Iterable
from django import forms

class PersonForm(forms.Form):
    # Section 1: Your Details
    your_name = forms.CharField(
        label="Your Full Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'તમારુ પુરુ નામ દાખલ કરો'})
    )
    your_email = forms.EmailField(
    label="Your Email",
    required=True,
    error_messages={
        'required': 'ઈમેલ દાખલ કરવું ફરજિયાત છે.',  # Custom message for empty email
        'invalid': 'તમારું ઈમેલ સરનામું અમાન્ય છે.'  # Custom message for invalid email format
    },
    widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'તમારુ ઈમેલ દાખલ કરો'})
    )

    # Section 2: Person's Details to Add to CSV
    person_name = forms.CharField(
        label="Full Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'પૂરુ નામ'})
    )
    gender = forms.ChoiceField(
        label="જાતિ",
        required=True,
        choices=[('Male', 'પુરુષ'), ('Female', 'સ્ત્રી')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    dob = forms.DateField(
        label="Date of Birth",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'DD-MM-YYYY'}),
        input_formats=['%d-%m-%Y'],  # Specifies the input format as DD-MM-YYYY
    )
    father_name = forms.CharField(
        label="Father's Full Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "બાપુસાહેબ નુ પુરુ નામ દાખલ કરો"})
    )
    mother_name = forms.CharField(
        label="Mother's Full Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "બાસાહેબ નુ પુરુ નામ દાખલ કરો"})
    )
    marital_status = forms.ChoiceField(
        label="વૈવાહિક સ્થિતિ",
        required=True,
        choices=[('married', 'પરણિત'), ('not_married', 'અપરણિત')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    # Section 3: Spouse Information
    num_spouse = forms.ChoiceField(
        label="Number of Spouses",
        choices=[('0','0'),('1', '1'), ('2', '2'), ('3', '3'), ('4+', '4+')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    num_children = forms.ChoiceField(
        label = "સંતાનો ની સંખિયા",
        choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4+', '4+')],
        widget=forms.Select(attrs={'class':'form-select'})
    )

    # Section 4: Children Information
    def __init__(self, *args, **kwargs):
        num_children = int(kwargs.pop('num_children', 0))
        num_spouse = int(kwargs.pop('num_spouse', 0))
        super().__init__(*args, **kwargs)

        # Dynamically add fields for each child
        for i in range(1, num_children + 1):
            self.fields[f'child_name_{i}'] = forms.CharField(
                label=f"સંતાન - {i} નુ પૂરુ નામ",
                max_length=100,
                required=True,
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "સંતાન નુ પૂરુ નામ દાખલ કરો."})
            )
            self.fields[f'child_gender_{i}'] = forms.ChoiceField(
                label=f"સંતાન - {i} ની જાતિ",
                choices=[('male', 'પુરુષ'), ('female', 'સ્ત્રી')],
                required=True,
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
            )
            self.fields[f'child_marital_status_{i}'] = forms.ChoiceField(
                label=f"સંતાન - {i} ની વૈવાહિક સ્થિતિ",
                choices=[('married', 'પરણિત'), ('not_married', 'અપરણિત')],
                required=True,
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
            )

        # Dynamically add fields for each spouse
        for i in range(1, num_spouse + 1):
            self.fields[f'spouse_name_{i}'] = forms.CharField(
                label=f"રાણીસાહેબ/જમાઈસાહેબ - {i} નું પૂરુ નામ",
                max_length=100,
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "રાણીસાહેબ / જમાઈસાહેબ નુ પૂરુ નામ દાખલ કરો."})
            )
            self.fields[f'spouse_father_name_{i}'] = forms.CharField(
                label=f"Spouse {i}'s Father's Full Name",
                max_length=100,
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter spouse's father's name"})
            )
            self.fields[f'spouse_village_{i}'] = forms.CharField(
                label=f"Spouse {i}'s Village",
                max_length=100,
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter spouse's village"})
            )