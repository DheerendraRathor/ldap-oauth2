from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View


class SensitivePostParametersMixin(View):

    @method_decorator(sensitive_post_parameters('password', ))
    def dispatch(self, request, *args, **kwargs):
        return super(SensitivePostParametersMixin, self).dispatch(request, *args, **kwargs)


class FormErrorPageMixin(View):
    form_template = 'user_resources/form_error.html'
    form_title = 'Sex'
    action_url = ''

    def get_context_data(self):
        return {
            'form_title': self.form_title,
            'action_url': self.action_url,
        }

    def render(self, context_dict=None):
        if context_dict is None:
            context_dict = {}
        context = self.get_context_data()
        context.update(context_dict)
        return render(self.request, self.form_template, context)
