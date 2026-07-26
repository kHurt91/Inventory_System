from types import SimpleNamespace
from unittest.mock import Mock

from django.test import SimpleTestCase

from apps.inventory.permissions import IsStaffOrReadOnly


class IsStaffOrReadOnlyTests(SimpleTestCase):
    def setUp(self):
        self.permission = IsStaffOrReadOnly()
        self.view = None

    def _request(self, method, is_authenticated, is_staff):
        user = Mock(is_authenticated=is_authenticated, is_staff=is_staff)
        return SimpleNamespace(method=method, user=user)

    def test_unauthenticated_get_is_denied(self):
        request = self._request('GET', is_authenticated=False, is_staff=False)
        self.assertFalse(self.permission.has_permission(request, self.view))

    def test_authenticated_non_staff_get_is_allowed(self):
        request = self._request('GET', is_authenticated=True, is_staff=False)
        self.assertTrue(self.permission.has_permission(request, self.view))

    def test_authenticated_non_staff_post_is_denied(self):
        request = self._request('POST', is_authenticated=True, is_staff=False)
        self.assertFalse(self.permission.has_permission(request, self.view))

    def test_authenticated_staff_post_is_allowed(self):
        request = self._request('POST', is_authenticated=True, is_staff=True)
        self.assertTrue(self.permission.has_permission(request, self.view))
