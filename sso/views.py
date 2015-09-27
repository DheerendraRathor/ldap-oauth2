from django.views.generic import RedirectView, TemplateView


class IndexRedirectView(RedirectView):
    pattern_name = 'account:login'


class DocView(TemplateView):
    template_name = 'sso/5-minutes-doc.html'
