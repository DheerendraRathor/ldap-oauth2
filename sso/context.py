from django.conf import settings


def project_url(request):
    return {'PROJECT_URL': settings.PROJECT_URL}
