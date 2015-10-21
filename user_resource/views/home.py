from collections import defaultdict

from braces.views import LoginRequiredMixin
from django.http.response import HttpResponse, HttpResponseBadRequest
import json
from django.forms.models import model_to_dict
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, View
from oauth2_provider.models import AccessToken, get_application_model as get_oauth2_application_model
from oauth2_provider.settings import oauth2_settings

from ..forms import InstituteAddressForm, ProgramForm, ProfilePictureForm, SexUpdateForm
from ..models import ContactNumber, InstituteAddress, Program, SecondaryEmail


class UserApplicationListView(LoginRequiredMixin, ListView):
    template_name = 'user_resources/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        user = self.request.user
        access_tokens = AccessToken.objects.filter(user=user).prefetch_related('application')

        application_scope_dict = defaultdict(set)

        for access_token in access_tokens:
            scopes = access_token.scope
            scopes = scopes.split()
            application_scope_dict[access_token.application] |= set(scopes)

        application_scope_detail_dict = {}
        for application, scopes in application_scope_dict.items():
            application_scope_detail_dict[application] = [oauth2_settings.SCOPES.get(scope, None) for scope in scopes if
                                                          oauth2_settings.SCOPES.get(scope, None)]

        return application_scope_detail_dict


class ApplicationRevokeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        application = get_object_or_404(get_oauth2_application_model(), pk=pk)
        if not application.is_anonymous:
            user = request.user
            AccessToken.objects.filter(user=user, application_id=pk).delete()
        return redirect('user:settings')


class UserHomePageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        try:
            insti_address_form = InstituteAddressForm(initial=model_to_dict(user.insti_address))
        except (AttributeError, InstituteAddress.DoesNotExist):
            insti_address_form = InstituteAddressForm()

        try:
            program_form = ProgramForm(initial=model_to_dict(user.program))
        except (AttributeError, Program.DoesNotExist):
            program_form = ProgramForm()

        try:
            sex_update_form = SexUpdateForm(initial={'sex': user.userprofile.sex})
        except AttributeError:
            sex_update_form = SexUpdateForm()

        mobile_numbers = ContactNumber.objects.all().filter(user=user).order_by('-id')
        secondary_emails = SecondaryEmail.objects.all().filter(user=user).order_by('-id')
        user_profile = user.userprofile
        gpo_email = user.email
        ldap_number = user_profile.mobile
        roll_number = user_profile.roll_number

        return render(request, 'user_resources/home.html',
                      {
                          'insti_address_form': insti_address_form,
                          'program_form': program_form,
                          'mobile_numbers': mobile_numbers,
                          'secondary_emails': secondary_emails,
                          'gpo_email': gpo_email,
                          'ldap_number': ldap_number,
                          'roll_number': roll_number,
                          'sex_update_form': sex_update_form,
                      }
                      )


class UpdateUserSex(LoginRequiredMixin, View):
    def post(self, request):
        sex_update_form = SexUpdateForm(request.POST)
        if sex_update_form.is_valid():
            sex = sex_update_form.cleaned_data['sex']
            userprofile = request.user.userprofile
            userprofile.sex = sex
            userprofile.save()
        return redirect('user:home')


class UpdateUserProfilePicture(LoginRequiredMixin, View):
    def post(self, request):
        pp_form = ProfilePictureForm(request.POST, request.FILES)
        if pp_form.is_valid():
            profile_picture = pp_form.cleaned_data['profile_picture']
            userprofile = request.user.userprofile
            userprofile.profile_picture = profile_picture
            userprofile.save()
            response = {'url': userprofile.profile_picture.url}
            return HttpResponse(json.dumps(response))
        else:
            return HttpResponseBadRequest(json.dumps(pp_form.errors))


class UpdateInstiAddressView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        try:
            insti_address = user.insti_address
        except InstituteAddress.DoesNotExist:
            insti_address = None
        form = InstituteAddressForm(data=request.POST, instance=insti_address)
        if form.is_valid():
            insti_address = form.save(commit=False)
            insti_address.user = user
            insti_address.save()
        return redirect('user:home')


class UpdateProgramView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        try:
            program = user.program
        except Program.DoesNotExist:
            program = None
        form = ProgramForm(data=request.POST, instance=program)
        if form.is_valid():
            program = form.save(commit=False)
            program.user = user
            program.save()
        return redirect('user:home')


class UpdateMobileNumberView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        mobiles = request.POST.getlist('phone')
        mobiles = set([mobile for mobile in mobiles if mobile != ''])
        saved_mobiles = set([contact.number for contact in user.contacts.all()])
        mobiles_to_update = mobiles - saved_mobiles
        mobiles_to_delete = saved_mobiles - mobiles
        if mobiles_to_update:
            ContactNumber.objects.bulk_create([ContactNumber(user=user, number=number) for number in mobiles_to_update])
        if mobiles_to_delete:
            ContactNumber.objects.filter(user=user).filter(number__in=mobiles_to_delete).delete()
        return redirect('user:home')


class UpdateSecondaryEmailView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        emails = request.POST.getlist('email')
        emails = set([email for email in emails if email != ''])
        saved_emails = set([secondary_email.email for secondary_email in user.secondary_emails.all()])
        emails_to_update = emails - saved_emails
        emails_to_delete = saved_emails - emails
        if emails_to_update:
            SecondaryEmail.objects.bulk_create([SecondaryEmail(user=user, email=email) for email in emails_to_update])
        if emails_to_delete:
            SecondaryEmail.objects.filter(user=user).filter(email__in=emails_to_delete).delete()
        return redirect('user:home')
