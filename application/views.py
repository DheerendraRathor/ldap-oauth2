from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin
from .forms import RegistrationForm, AllowFormWithRecaptch
from oauth2_provider.views.application import ApplicationOwnerIsUserMixin
from oauth2_provider.models import get_application_model as get_oauth2_application_model
from oauth2_provider.views import AuthorizationView


class ApplicationRegistrationView(LoginRequiredMixin, CreateView):

    form_class = RegistrationForm
    template_name = "application/application_form_registration.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ApplicationRegistrationView, self).form_valid(form)


class ApplicationDetailView(ApplicationOwnerIsUserMixin, DetailView):

    context_object_name = 'application'
    template_name = 'application/application_detail.html'


class ApplicationListView(ApplicationOwnerIsUserMixin, ListView):

    context_object_name = 'applications'
    template_name = 'application/application_list.html'


class ApplicationUpdateView(LoginRequiredMixin, UpdateView):
    """
    View used to update an application owned by the request.user
    """
    form_class = RegistrationForm
    context_object_name = 'application'
    template_name = "application/application_form.html"

    def get_queryset(self):
        return get_oauth2_application_model().objects.filter(user=self.request.user)


class ApplicationDeleteView(ApplicationOwnerIsUserMixin, DeleteView):
    """
    View used to update an application owned by the request.user
    """
    context_object_name = 'application'
    template_name = "application/application_confirm_delete.html"
    success_url = reverse_lazy('oauth:list')


class CustomAuthorizationView(AuthorizationView):

    form_class = AllowFormWithRecaptch