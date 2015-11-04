from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from core.utils import SEXES, get_choices_with_blank_dash

from .models import InstituteAddress, Program


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
    sex = forms.ChoiceField(choices=get_choices_with_blank_dash(SEXES), required=False,
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
    def clean(self):
        cleaned_data = super(ProgramForm, self).clean()
        join_year = cleaned_data.get('join_year')
        graduation_year = cleaned_data.get('graduation_year')

        if join_year and graduation_year:
            if graduation_year <= join_year:
                validation_err = forms.ValidationError(_('How come you graduated before you joined?'), code='bad_input')
                self.add_error('graduation_year', validation_err)

            if join_year >= graduation_year:
                validation_err = forms.ValidationError(
                    _('How come you joined after you graduated? You must be in alternate timeline!'), code='bade_input')
                self.add_error('join_year', validation_err)

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
        labels = {
            'department': 'Discipline',
            'graduation_year': '(Expected) Graduation Year',
        }
