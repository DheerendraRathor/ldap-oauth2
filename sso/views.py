from django.views.generic import TemplateView
from django.templatetags.static import static
from django.core.mail.message import make_msgid
from core.utils import SORTED_DISCIPLINES, DEGREES, HOSTELS, SEXES
from account.models import UserProfile


class IndexView(TemplateView):
    template_name = 'sso/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated():
            context['base_template'] = 'sso/logged_in.html'
        else:
            context['base_template'] = 'sso/root.html'

        return self.render_to_response(context)


class DocView(TemplateView):
    template_name = 'sso/5-minutes-doc.html'

    def get_context_data(self, **kwargs):
        context = super(DocView, self).get_context_data(**kwargs)
        context['login_js_url'] = static('widget/js/login.min.js')
        context['Message_ID'] = make_msgid()
        context['SORTED_DISCIPLINES'] = SORTED_DISCIPLINES
        context['DEGREES'] = DEGREES
        context['HOSTELS'] = HOSTELS
        context['SEXES'] = SEXES
        context['USER_TYPES'] = UserProfile.objects.values_list('type').distinct()
        return context
