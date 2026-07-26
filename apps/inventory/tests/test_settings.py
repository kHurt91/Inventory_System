from django.conf import settings
from django.test import SimpleTestCase


class SettingsTests(SimpleTestCase):
    def test_secret_key_is_set_and_not_the_old_hardcoded_value(self):
        self.assertTrue(settings.SECRET_KEY)
        self.assertFalse(settings.SECRET_KEY.startswith('django-insecure-'))

    def test_debug_is_a_bool(self):
        self.assertIsInstance(settings.DEBUG, bool)

    def test_allowed_hosts_is_a_list(self):
        self.assertIsInstance(settings.ALLOWED_HOSTS, list)

    def test_jwt_authentication_is_configured(self):
        self.assertIn(
            'rest_framework_simplejwt.authentication.JWTAuthentication',
            settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'],
        )

    def test_django_filter_backend_is_configured(self):
        self.assertIn(
            'django_filters.rest_framework.DjangoFilterBackend',
            settings.REST_FRAMEWORK['DEFAULT_FILTER_BACKENDS'],
        )
