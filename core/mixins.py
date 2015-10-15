from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View
from django.utils.decorators import method_decorator


class SensitivePostParametersMixin(View):

    @method_decorator(sensitive_post_parameters('password', ))
    def dispatch(self, request, *args, **kwargs):
        return super(SensitivePostParametersMixin, self).dispatch(request, *args, **kwargs)
