from unittest import mock
from unittest.mock import Mock

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from apps.inventory.models import EquipmentList, InventoryTransactions, Parts, Suppliers
from apps.inventory.views import (
    EquipmentListViewSet,
    InventoryTransactionViewSet,
    PartsViewSet,
    SupplierViewSet,
)


class MockedQuerysetReadTests(APITestCase):
    """Exercise the read path without touching the (unmanaged, migration-less) real tables."""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = Mock(is_authenticated=True, is_staff=False)

    def _get_list(self, viewset_cls, queryset_none, url):
        with mock.patch.object(viewset_cls, 'get_queryset', return_value=queryset_none):
            request = self.factory.get(url)
            force_authenticate(request, user=self.user)
            response = viewset_cls.as_view({'get': 'list'})(request)
        return response

    def test_parts_list_with_empty_mocked_queryset(self):
        response = self._get_list(PartsViewSet, Parts.objects.none(), '/api/parts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], [])

    def test_inventory_transactions_list_with_empty_mocked_queryset(self):
        response = self._get_list(
            InventoryTransactionViewSet, InventoryTransactions.objects.none(), '/api/inventory-transactions/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], [])

    def test_equipment_list_with_empty_mocked_queryset(self):
        response = self._get_list(EquipmentListViewSet, EquipmentList.objects.none(), '/api/equipment/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], [])

    def test_suppliers_list_with_empty_mocked_queryset(self):
        response = self._get_list(SupplierViewSet, Suppliers.objects.none(), '/api/suppliers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], [])


class WritePermissionTests(APITestCase):
    """Permission check runs before any queryset is touched, so no DB access happens here."""

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_non_staff_post_to_parts_is_forbidden(self):
        request = self.factory.post('/api/parts/', {'part_description': 'Test'})
        force_authenticate(request, user=Mock(is_authenticated=True, is_staff=False))
        response = PartsViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 403)

    def test_anonymous_get_to_parts_is_unauthorized(self):
        request = self.factory.get('/api/parts/')
        response = PartsViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 401)


class InventoryTransactionWriteRestrictionTests(APITestCase):
    """InventoryTransactions is an immutable ledger: no PATCH/PUT/DELETE routes exist."""

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_patch_returns_405(self):
        request = self.factory.patch('/api/inventory-transactions/1/', {'quantity': 1})
        force_authenticate(request, user=Mock(is_authenticated=True, is_staff=True))
        response = InventoryTransactionViewSet.as_view({'get': 'retrieve'})(request, pk=1)
        self.assertEqual(response.status_code, 405)

    def test_delete_returns_405(self):
        request = self.factory.delete('/api/inventory-transactions/1/')
        force_authenticate(request, user=Mock(is_authenticated=True, is_staff=True))
        response = InventoryTransactionViewSet.as_view({'get': 'retrieve'})(request, pk=1)
        self.assertEqual(response.status_code, 405)

    def test_created_by_is_set_from_request_user_not_client_input(self):
        request = self.factory.post(
            '/api/inventory-transactions/',
            {'transaction_type': 'Issue', 'quantity': 1, 'created_by': 999},
            format='json',
        )
        real_user = Mock(is_authenticated=True, is_staff=True, pk=42)
        force_authenticate(request, user=real_user)
        with mock.patch('apps.inventory.serializers.record_transaction') as mock_record:
            mock_record.return_value = Mock(
                id=1, part=None, part_id=None, transaction_type='Issue', quantity=1,
                signed_quantity=-1, created_time=None, created_by=None, created_by_id=None,
                source_reference=None,
            )
            InventoryTransactionViewSet.as_view({'post': 'create'})(request)
            _, kwargs = mock_record.call_args
            self.assertEqual(kwargs['created_by'], real_user)


class TokenObtainTests(APITestCase):
    """django.contrib.auth tables have real migrations, so this is safe to hit the test DB."""

    def test_token_obtain_pair_success(self):
        User.objects.create_user(username='tokentestuser', password='tokentestpass123')
        response = self.client.post(
            '/api/token/',
            {'username': 'tokentestuser', 'password': 'tokentestpass123'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
