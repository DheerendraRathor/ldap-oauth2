from django import forms
from .models import InstituteAddress, Program
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat


class ProfilePictureForm(forms.Form):
    profile_picture = forms.ImageField()

    def clean_profile_picture(self):
        pp = self.cleaned_data['profile_picture']
        content_type = pp.content_type.split('/')[0]
        if content_type in ['image']:
            if pp._size > 5242880:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
                filesizeformat(5242880), filesizeformat(pp._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))
        return pp


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
