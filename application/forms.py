from django import forms

from .models import Application


class RegistrationForm(forms.ModelForm):
    """
    TODO: add docstring
    """

    class Meta:
        model = Application
        fields = (
            'name', 'description', 'logo', 'client_id', 'client_secret', 'client_type', 'authorization_grant_type',
            'redirect_uris')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', }
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, }
            ),
            'logo': forms.ClearableFileInput(
                attrs={'class': 'form-control', 'accept': 'image/*', }
            ),
            'client_id': forms.TextInput(
                attrs={'class': 'form-control', }
            ),
            'client_secret': forms.TextInput(
                attrs={'class': 'form-control', }
            ),
            'client_type': forms.Select(
                attrs={'class': 'form-control', }
            ),
            'authorization_grant_type': forms.Select(
                attrs={'class': 'form-control', }
            ),
            'redirect_uris': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, }
            )
        }
