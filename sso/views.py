from django.views.generic import RedirectView


class IndexRedirectView(RedirectView):

    pattern_name = 'account:login'
