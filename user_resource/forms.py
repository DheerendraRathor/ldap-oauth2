from django import forms
from .models import InstituteAddress, Program


class InstituteAddressForm(forms.ModelForm):
    class Meta:
        model = InstituteAddress
        fields = ['hostel', 'room']
        widgets = {
            'hostel': forms.Select(
                attrs={'class': 'form-control', },
            ),
            'room': forms.TextInput(
                attrs={'class': 'form-control', },
            ),
        }


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['department', 'join_year', 'graduation_year', 'degree']
        widgets = {
            'department': forms.Select(
                attrs={'class': 'form-control', },
            ),
            'join_year': forms.NumberInput(
                attrs={'class': 'form-control', },
            ),
            'graduation_year': forms.NumberInput(
                attrs={'class': 'form-control', },
            ),
            'degree': forms.Select(
                attrs={'class': 'form-control', },
            ),
        }
