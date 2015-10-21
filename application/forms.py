from django import forms

from .models import Application


class RegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Application
        fields = (
            'name', 'description', 'logo', 'website', 'privacy_policy', 'client_id', 'client_secret', 'client_type',
            'authorization_grant_type', 'redirect_uris')
        widgets = {
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, }
            ),
            'logo': forms.ClearableFileInput(
                attrs={'class': 'form-control', 'accept': 'image/*', }
            ),
            'website': forms.URLInput(
                attrs={'class': 'form-control', }
            ),
            'privacy_policy': forms.URLInput(
                attrs={'class': 'form-control', }
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
