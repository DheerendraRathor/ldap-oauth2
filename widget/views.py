from django.views.generic import TemplateView
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator


class LoginWidget(TemplateView):
    template_name = 'widget/login.html'

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

        return self.render_to_response(context)

    @method_decorator(xframe_options_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginWidget, self).dispatch(request, *args, **kwargs)


