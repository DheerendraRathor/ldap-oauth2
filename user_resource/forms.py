from django import forms
from .models import InstituteAddress, Program
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from core.utils import SEX_CHOICES


class ProfilePictureForm(forms.Form):
    profile_picture = forms.ImageField()

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data['profile_picture']
        content_type = profile_picture.content_type.split('/')[0]
        if content_type in ['image']:
            if profile_picture.size > 5242880:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
                    filesizeformat(5242880), filesizeformat(profile_picture.size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))
        return profile_picture


class SexUpdateForm(forms.Form):
    sex = forms.ChoiceField(choices=SEX_CHOICES, required=False,
                            widget=forms.Select(
                                attrs={'class': 'form-control', },
                            ))


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
