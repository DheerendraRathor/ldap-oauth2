import django.utils.six as six
from django.conf import settings
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase, override_settings

from account.models import UserProfile
from application.models import Application

from .templatetags.absolute_url import absolute_url
from .templatetags.model_media import model_field_media_url
from .utils import TabNav, attr_to_dict, get_default_scopes


class CoreUtilsTest(TestCase):
    @override_settings(OAUTH2_DEFAULT_SCOPES=['basic', 'profile'])
    def test_default_scopes(self):
        application1 = Application(
            name='application1',
            description='testapp',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://localhost:7000/',
            is_anonymous=True,
            required_scopes='send_mail picture',
        )
        six.assertCountEqual(self, ['send_mail', 'picture'], get_default_scopes(application1))
        application2 = Application(
            name='application2',
            description='testapp',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://localhost:7000/',
            required_scopes='send_mail picture',
        )
        six.assertCountEqual(self, settings.OAUTH2_DEFAULT_SCOPES, get_default_scopes(application2))

    def test_attr_to_dict(self):
        application1 = Application(
            name='application1',
            description='testapp',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://localhost:7000/',
            is_anonymous=True,
            required_scopes='send_mail picture',
        )
        result_dict = attr_to_dict(application1)
        self.assertDictContainsSubset({
            'name': 'application1',
            'description': 'testapp',
            'client_type': 'confidential',
            'authorization_grant_type': 'authorization-code',
            'redirect_uris': 'http://localhost:7000/',
            'is_anonymous': True,
            'required_scopes': 'send_mail picture',
        }, result_dict)

        dict_test = {'key': 'foo', 'value': 'bar'}
        self.assertDictEqual(dict_test, attr_to_dict(dict_test))

        self.assertDictEqual({'foo': 'bar'}, attr_to_dict('bar', key='foo'))

    def test_tab_nav_cls(self):
        self.assertRaises(ValueError, TabNav, None)
        self.assertRaises(ValueError, TabNav, 'basic')
        self.assertTrue(TabNav('basic', base_url='doc'))

        basic_tab = TabNav('basic', base_url='doc')
        self.assertEqual(basic_tab.name, 'Basic')
        self.assertEqual(basic_tab.template_name, 'basic.html')
        self.assertFalse(basic_tab.is_default)
        self.assertFalse(basic_tab.is_active)
        self.assertEqual(basic_tab.url, '/doc/basic/')
        self.assertEqual(basic_tab.tab_name, 'basic')

        default_tab = TabNav('default', base_url='doc', is_default=True, name='Le Default',
                             template_name='defacto.html')
        self.assertEqual(default_tab.name, 'Le Default')
        self.assertEqual(default_tab.template_name, 'defacto.html')
        self.assertTrue(default_tab.is_default)
        self.assertEqual(default_tab.url, '/doc/')
        self.assertEqual(default_tab.tab_name, '')


class CoreTemplateTagsTest(TestCase):
    @override_settings(MEDIA_URL='/media/')
    def test_templatetags_model_field_media_url(self):
        u1 = User.objects.create(username='foo', password='bar')
        userprofile = UserProfile.objects.create(user=u1, profile_picture='app/12345.png')
        media_url = model_field_media_url(userprofile.profile_picture)
        self.assertEqual(media_url, '/media/app/12345.png')

        userprofile.delete()
        userprofile = UserProfile.objects.create(user=u1)
        self.assertEqual(None, model_field_media_url(userprofile.profile_picture))

        userprofile.delete()
        u1.delete()

    def test_templatetags_absolute_url(self):
        request = RequestFactory().get('/index/')
        context = {'request': request}
        url1 = '/root/url/'
        self.assertEqual('http://testserver/root/url/', absolute_url(context, url1))
        url2 = 'non/root/url/'
        self.assertEqual('http://testserver/index/non/root/url/', absolute_url(context, url2))
