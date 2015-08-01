from django.shortcuts import redirect, render
from django.views.generic import View
from .forms import LoginForm
from django.conf import settings
from django.contrib.auth import authenticate, login, logout


class LoginView(View):
    form_class = LoginForm
    template_name = 'account/login.html'

    def get(self, request):
        next = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
        if request.user.is_authenticated():
            return redirect(next)
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        next = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
        if next == '':
            next = settings.LOGIN_REDIRECT_URL
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']

            if remember:
                # Yearlong Session
                request.session.set_expiry(24*265*3600)
            else:
                request.session.set_expiry(0)

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next)
            else:
                form.add_error(None, "Unable to authorize user. Try again!")
        return render(request, self.template_name, {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('account:login')

