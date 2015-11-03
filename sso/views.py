from django.core.mail.message import make_msgid
from django.templatetags.static import static
from django.views.generic import TemplateView

from account.models import UserProfile
from core.utils import DEGREES, HOSTELS, SEXES, SORTED_DISCIPLINES, TabNav


class IndexView(TemplateView):
    template_name = 'sso/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated():
            context['base_template'] = 'sso/logged_in.html'
        else:
            context['base_template'] = 'sso/root.html'

        return self.render_to_response(context)


tabs_list = [
    ('basic', 'Basic', 'basic.html'),
    ('api', 'APIs', 'api.html'),
    ('widgets', 'Widgets', 'widget.html'),
    ('best-practices', 'Best Practices', 'practices.html'),
    ('libraries', 'Libraries', 'library.html'),
]


class DocView(TemplateView):
    template_name = 'sso/5-minutes-doc.html'
    tabs = [TabNav(tab[0], tab[1], tab[2], 'doc', tab[0] == 'basic') for tab in tabs_list]

    def get_context_data(self, **kwargs):
        context = super(DocView, self).get_context_data(**kwargs)
        context['login_js_url'] = static('widget/js/login.min.js')
        context['Message_ID'] = make_msgid()
        context['SORTED_DISCIPLINES'] = SORTED_DISCIPLINES
        context['DEGREES'] = DEGREES
        context['HOSTELS'] = HOSTELS
        context['SEXES'] = SEXES
        context['USER_TYPES'] = UserProfile.objects.values_list('type').distinct()

        # Mark all tabs as inactive
        for tab_ in self.tabs:
            tab_.is_active = False

        tab = context.get('tab', '')
        for tab_ in self.tabs:
            if tab == tab_.tab_name:
                tab = tab_
                break
        else:
            tab = self.tabs[0]
        tab.is_active = True
        context['tabs'] = self.tabs
        context['active_tab'] = tab
        return context
