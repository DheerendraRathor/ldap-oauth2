from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm
from core.mixins import SensitivePostParametersMixin

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus


class LoginView(SensitivePostParametersMixin, View):
    """
    GET: If user is already logged in then redirect to 'next' parameter in query_params
        Else render the login form
    POST:
        Validate form, login user
    """
    form_class = LoginForm
    template_name = 'account/login.html'

    def get(self, request):
        next_ = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
        if next_ == '':
            next_ = settings.LOGIN_REDIRECT_URL
        if request.user.is_authenticated():
            return redirect(next_)
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        next_ = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
        if next_ == '':
            next_ = settings.LOGIN_REDIRECT_URL
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']

            user = authenticate(username=username, password=password)
            if user is not None:
                if remember:
                    # Yearlong Session
                    request.session.set_expiry(24 * 365 * 3600)
                else:
                    request.session.set_expiry(0)
                login(request, user)
                return redirect(next_)
            else:
                form.add_error(None, "Unable to authorize user. Try again!")
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        next_ = request.GET.get('next')
        if next_ is None:
            return redirect('index')
        next_ = quote_plus(next_)
        login_url = reverse('account:login')
        redirect_to = '%s?next=%s' % (login_url, next_) if next_ else login_url
        return HttpResponseRedirect(redirect_to)
