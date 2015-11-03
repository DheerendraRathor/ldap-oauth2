import django.utils.six as six
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, mock

from .models import UserProfile, user_profile_picture

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus




class LoginViewTestCase(TestCase):
    login_url = reverse('account:login')
    login_redirect_url = reverse(settings.LOGIN_REDIRECT_URL)
    next_ = reverse('oauth2_provider:list')
    template_name = 'account/login.html'

    def setUp(self):
        self.test_user = User.objects.create_user(username='test_user', password='test123')
        self.userprofile = UserProfile.objects.create(user=self.test_user)

    def tearDown(self):
        self.client.logout()
        self.test_user.delete()

    def test_userprofile_unicode(self):
        self.assertEqual(str(self.userprofile), self.test_user.username)

    def test_application_logo_upload(self):
        with mock.patch('uuid.uuid4') as uuid_mock:
            uuid_mock.return_value = '1234567890'
            filename = user_profile_picture(self.test_user, 'hola.png')
            self.assertNotEqual(filename, 'app_logo/1234567890.png')

    def test_application_logo_default_ext(self):
        with mock.patch('uuid.uuid4') as uuid_mock:
            uuid_mock.return_value = '987654321'
            filename = user_profile_picture(self.test_user, 'hola')
            self.assertNotEqual(filename, 'app_logo/987654321.png')

    def test_user_already_logged_in_get(self):
        """
        Tests the redirect on opening login page when user is already logged in.
        Request must be redirected to settings.LOGIN_REDIRECT_URL when get query 'next' is not present
        """
        self._user_login()
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.login_redirect_url)

    def test_user_already_logged_in_get_with_next(self):
        """
        Tests the redirect on opening login page when user is already logged in.
        Request must be redirected to get query param 'next'
        """
        self._user_login()
        response = self.client.get('%s?next=%s' % (self.login_url, self.next_))
        self.assertRedirects(response, self.next_)

    def test_user_already_logged_in_get_with_empty_next(self):
        """
        Tests the redirect on opening login page when user is already logged in.
        Request must be redirected to get query param 'next'
        """
        self._user_login()
        response = self.client.get('%s?next=%s' % (self.login_url, ''))
        self.assertRedirects(response, self.login_redirect_url)

    def test_user_not_logged_in_get(self):
        """
        Test in case user is not logged in. Should return 200 status for 'account:login' page
        """
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(response.status_code, 200)

    def test_user_not_logged_in_get_with_next(self):
        """
        Should not redirect in case 'next' is present in query param and user is not logged in
        """
        response = self.client.get('%s?next=%s' % (self.login_url, self.next_))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)

    def test_user_not_logged_in_without_next(self):
        """
        Test when ?next= is not present in URL. Rendered form should have hidden input with name next and value ''
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        six.assertRegex(self, response.content.decode('utf-8'), r'name=[\'"]next[\'"].*?value=[\'"]{2}')

    def test_post_request_correct_credentials(self):
        response = self.client.post(self.login_url, {'username': 'test_user', 'password': 'test123'})
        self.assertRedirects(response, self.login_redirect_url)

    def test_post_request_correct_credentials_with_next(self):
        """
        Posting data with next in action URL. Should be redirect to next
        """
        response = self.client.post(self.login_url, {'username': 'test_user', 'password': 'test123', 'next': '/user/'})
        self.assertRedirects(response, '/user/')

    def test_post_request_correct_credentials_with_empty_next(self):
        """
        Posting data with empty next in action URL. Should be redirect to login_redirect_url
        """
        response = self.client.post(self.login_url, {'username': 'test_user', 'password': 'test123', 'next': ''})
        self.assertRedirects(response, self.login_redirect_url)

    def test_post_request_incorrect_credentials(self):
        response = self.client.post(self.login_url, {'username': 'test', 'password': 'test123'})
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(response.status_code, 200)

    def test_post_request_correct_credentials_remember_me(self):
        response = self.client.post(self.login_url, {'username': 'test_user',
                                                     'password': 'test123', 'remember': True})
        self.assertRedirects(response, self.login_redirect_url)
        session = self.client.session
        self.assertEqual(session.get_expiry_age(), 24 * 365 * 3600)

    def _user_login(self):
        self.client.login(username='test_user', password='test123')


class LogoutViewTestCase(TestCase):
    logout_url = reverse('account:logout')
    login_url = reverse('account:login')
    root_url = reverse('index')
    user_home = reverse('user:home')

    def setUp(self):
        User.objects.create_user(username='test_user', password='test123')

    def test_user_logged_in(self):
        """
        Logout should redirect to login page
        """
        self.client.login(username='test_user', password='test123')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.root_url)

    def test_user_not_logged_in(self):
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.root_url)

    def test_logout_with_next(self):
        response = self.client.get('%s?next=%s' % (self.logout_url, self.user_home))
        self.assertRedirects(response, '%s?next=%s' % (self.login_url, quote_plus(self.user_home)))

    def test_post(self):
        """
        Assert that POST method is not allowed for logout. Response code should be 405
        """
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 405)
