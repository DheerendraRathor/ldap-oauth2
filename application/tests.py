from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, mock
from django.utils.timezone import now
from oauth2_provider.models import AccessToken

from account.models import UserProfile

from .admin import ApplicationAdmin
from .models import Application, application_logo


class ApplicationModelTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username='username', password='password')
        UserProfile.objects.create(user=self.u1)
        self.application1 = Application.objects.create(
            name='application1',
            description='testapp',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://localhost:7000/',
            logo='app_logo/1235.png',
            user=self.u1,
        )
        self.application2 = Application.objects.create(
            name='application2',
            description='testapp',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://localhost:6000/',
            user=self.u1,
        )

    def tearDown(self):
        self.u1.delete()
        self.application1.delete()
        self.application2.delete()

    def test_application_get_absolute_url(self):
        url1 = self.application1.get_absolute_url()
        self.assertEqual('/oauth/applications/1/', url1)

        url2 = self.application2.get_absolute_url()
        self.assertEqual('/oauth/applications/2/', url2)

    def test_get_logo_url(self):
        url1 = self.application1.get_logo_url()
        self.assertEqual('%sapp_logo/1235.png' % settings.MEDIA_URL, url1)

        url2 = self.application2.get_logo_url()
        self.assertEqual(None, url2)

    def test_user_count(self):
        user_count_1 = self.application1.get_user_count()
        user_count_2 = self.application2.get_user_count()

        self.assertEqual(user_count_1, 0)
        self.assertEqual(user_count_2, 0)

    def test_model_unicode(self):
        self.assertEqual(str(self.application1), 'application1')
        self.assertEqual(str(self.application2), 'application2')

        application3 = Application.objects.create(
            description='testapp',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://localhost:5000/',
            user=self.u1,
        )

        self.assertNotEqual(str(application3), '')

    def test_validation_error_on_clean(self):
        application4 = Application(
            name='resource_owner_password_based_app',
            description='testapp',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=self.u1,
            redirect_uris='http://localhost:4000'
        )

        self.assertRaises(ValidationError, application4.clean)

    def test_application_logo_upload(self):
        with mock.patch('uuid.uuid4') as uuid_mock:
            uuid_mock.return_value = '1234567890'
            filename = application_logo(self.application1, 'hola.png')
            self.assertNotEqual(filename, 'app_logo/1234567890.png')

    def test_application_logo_default_ext(self):
        with mock.patch('uuid.uuid4') as uuid_mock:
            uuid_mock.return_value = '987654321'
            filename = application_logo(self.application1, 'hola')
            self.assertNotEqual(filename, 'app_logo/987654321.png')


class ApplicationAdminTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username='username', password='password')
        self.application1 = self.application1 = Application.objects.create(
            name='application1',
            description='testapp',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://localhost:7000/',
            logo='app_logo/1235.png',
            user=self.u1,
        )
        self.app_admin = ApplicationAdmin(Application, AdminSite())

    def tearDown(self):
        self.u1.delete()
        self.application1.delete()

    def test_get_user_count_zero_user(self):
        self.assertEqual(0, self.app_admin.total_users(self.application1))

    def test_get_user_count_one_user(self):
        access_token1 = AccessToken.objects.create(user=self.u1, application=self.application1, token='123',
                                                   expires=now())
        access_token2 = AccessToken.objects.create(user=self.u1, application=self.application1, token='123456',
                                                   expires=now())
        self.assertEqual(self.app_admin.total_users(self.application1), 1)

        access_token1.delete()
        access_token2.delete()

    def test_get_use_count_multiple_user(self):
        u2 = User.objects.create(username='u2', password='p2')
        access_token1 = AccessToken.objects.create(user=self.u1, application=self.application1, token='123',
                                                   expires=now())
        access_token2 = AccessToken.objects.create(user=u2, application=self.application1, token='123456',
                                                   expires=now())

        self.assertEqual(self.app_admin.total_users(self.application1), 2)

        access_token1.delete()
        access_token2.delete()
