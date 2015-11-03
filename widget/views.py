import re

from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import TemplateView


class LoginWidget(TemplateView):
    template_name = 'widget/login.html'
    hex_color_regex = re.compile(r'^(?:[0-9a-fA-F]{3}){1,2}$')

    def get_context_data(self, **kwargs):
        context = super(LoginWidget, self).get_context_data(**kwargs)
        context['button_div_bg_color'] = '#303F9F'
        context['button_anchor_color'] = '#FFFFFF'
        context['logout_anchor_color'] = '#727272'
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        query_params = []
        for query_param in ['client_id', 'scope', 'redirect_uri', 'state', 'response_type']:
            value = request.GET.get(query_param)
            if value:
                query_params.append('%s=%s' % (query_param, value))
        query = '&'.join(query_params)
        context['query'] = query

        new_window = request.GET.get('new_window')
        if new_window in ['true', 'yes', 'True', '1']:
            new_window = True
        else:
            new_window = False
        context['new_window'] = new_window

        for color_face in ['button_div_bg_color', 'button_anchor_color', 'logout_anchor_color']:
            color_val = request.GET.get(color_face)
            if color_val and self._verify_hex_color(color_val):
                context[color_face] = '#%s' % color_val

        return self.render_to_response(context)

    @method_decorator(xframe_options_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginWidget, self).dispatch(request, *args, **kwargs)

    def _verify_hex_color(self, hex_val):
        return self.hex_color_regex.match(hex_val) is not None
