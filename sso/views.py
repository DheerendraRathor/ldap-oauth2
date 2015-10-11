from django.views.generic import RedirectView, TemplateView
from django.templatetags.static import static


class IndexRedirectView(RedirectView):
    pattern_name = 'account:login'


class DocView(TemplateView):
    template_name = 'sso/5-minutes-doc.html'

    def get_context_data(self, **kwargs):
        context = super(DocView, self).get_context_data(**kwargs)
        context['login_js_url'] = static('widget/js/login.min.js')
        return context
