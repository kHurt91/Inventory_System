from unittest import mock
from unittest.mock import Mock

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from apps.inventory.models import (
    EquipmentList,
    InventoryTransactions,
    Parts,
    PurchaseOrder,
    PurchaseOrderLine,
    RepairHistory,
    Suppliers,
)
from apps.inventory.purchasing_services import InvalidPurchaseOrderStateError
from apps.inventory.views import (
    EquipmentListViewSet,
    InventoryTransactionViewSet,
    PartsViewSet,
    PurchaseOrderLineViewSet,
    PurchaseOrderViewSet,
    RepairHistoryViewSet,
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

    def test_repair_history_list_with_empty_mocked_queryset(self):
        response = self._get_list(RepairHistoryViewSet, RepairHistory.objects.none(), '/api/repair-history/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], [])

    def test_purchase_orders_list_with_empty_mocked_queryset(self):
        response = self._get_list(PurchaseOrderViewSet, PurchaseOrder.objects.none(), '/api/purchase-orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], [])

    def test_purchase_order_lines_list_with_empty_mocked_queryset(self):
        response = self._get_list(
            PurchaseOrderLineViewSet, PurchaseOrderLine.objects.none(), '/api/purchase-order-lines/'
        )
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

    def test_non_staff_post_to_purchase_orders_is_forbidden(self):
        request = self.factory.post('/api/purchase-orders/', {'supplier': 1})
        force_authenticate(request, user=Mock(is_authenticated=True, is_staff=False))
        response = PurchaseOrderViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 403)


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


class PurchaseOrderActionTests(APITestCase):
    """submit/receive delegate to purchasing_services; get_object/get_serializer are mocked
    out so these never touch the unmanaged Suppliers/Parts tables during serialization."""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.staff_user = Mock(is_authenticated=True, is_staff=True, pk=1)

    def _call(self, action_name, po, request, **url_kwargs):
        with mock.patch.object(PurchaseOrderViewSet, 'get_object', return_value=po), \
                mock.patch.object(PurchaseOrderViewSet, 'get_serializer', return_value=Mock(data={'id': po.pk})):
            force_authenticate(request, user=self.staff_user)
            return PurchaseOrderViewSet.as_view({'post': action_name})(request, pk=po.pk, **url_kwargs)

    def test_submit_success_returns_200(self):
        po = Mock(pk=1)
        request = self.factory.post('/api/purchase-orders/1/submit/')
        with mock.patch('apps.inventory.views.submit_purchase_order') as mock_submit:
            response = self._call('submit', po, request)
        mock_submit.assert_called_once_with(po)
        self.assertEqual(response.status_code, 200)

    def test_submit_invalid_state_returns_400(self):
        po = Mock(pk=1)
        request = self.factory.post('/api/purchase-orders/1/submit/')
        with mock.patch(
            'apps.inventory.views.submit_purchase_order',
            side_effect=InvalidPurchaseOrderStateError('not a draft'),
        ):
            response = self._call('submit', po, request)
        self.assertEqual(response.status_code, 400)

    def test_receive_missing_params_returns_400(self):
        po = Mock(pk=1)
        request = self.factory.post('/api/purchase-orders/1/receive/', {}, format='json')
        response = self._call('receive', po, request)
        self.assertEqual(response.status_code, 400)

    def test_receive_success_returns_200(self):
        po = Mock(pk=1)
        line = Mock(pk=5)
        po.lines.get.return_value = line
        request = self.factory.post('/api/purchase-orders/1/receive/', {'line': 5, 'quantity': 2}, format='json')
        with mock.patch('apps.inventory.views.receive_purchase_order_line') as mock_receive:
            response = self._call('receive', po, request)
        mock_receive.assert_called_once_with(line=line, quantity=2, created_by=self.staff_user)
        self.assertEqual(response.status_code, 200)

    def test_receive_unknown_line_returns_404(self):
        po = Mock(pk=1)
        po.lines.get.side_effect = PurchaseOrderLine.DoesNotExist
        request = self.factory.post('/api/purchase-orders/1/receive/', {'line': 999, 'quantity': 2}, format='json')
        response = self._call('receive', po, request)
        self.assertEqual(response.status_code, 404)

    def test_receive_over_quantity_returns_400(self):
        po = Mock(pk=1)
        line = Mock(pk=5)
        po.lines.get.return_value = line
        request = self.factory.post('/api/purchase-orders/1/receive/', {'line': 5, 'quantity': 999}, format='json')
        with mock.patch(
            'apps.inventory.views.receive_purchase_order_line', side_effect=ValueError('too much')
        ):
            response = self._call('receive', po, request)
        self.assertEqual(response.status_code, 400)


class PartsLookupActionTests(APITestCase):
    """Barcode/QR scan endpoint. Parts is unmanaged, so the model manager is mocked
    out rather than touching the real (test-DB-absent) parts table."""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = Mock(is_authenticated=True, is_staff=False)

    def _call(self, code=None):
        params = {'code': code} if code is not None else {}
        request = self.factory.get('/api/parts/lookup/', params)
        force_authenticate(request, user=self.user)
        return PartsViewSet.as_view({'get': 'lookup'})(request)

    def _patched_filter(self, MockParts, barcode_match=None, part_id_match=None, part_name_match=None):
        def side_effect(**kwargs):
            m = Mock()
            if 'barcode' in kwargs:
                m.first.return_value = barcode_match
            elif 'part_id' in kwargs:
                m.first.return_value = part_id_match
            elif 'part_name' in kwargs:
                m.first.return_value = part_name_match
            return m
        MockParts.objects.filter.side_effect = side_effect

    def test_missing_code_returns_400(self):
        response = self._call(code=None)
        self.assertEqual(response.status_code, 400)

    def test_barcode_match_takes_priority(self):
        part = Mock(part_id=1)
        with mock.patch('apps.inventory.views.Parts') as MockParts, \
                mock.patch.object(PartsViewSet, 'get_serializer', return_value=Mock(data={'part_id': 1})):
            self._patched_filter(MockParts, barcode_match=part)
            response = self._call(code='SCAN123')

        self.assertEqual(response.status_code, 200)

    def test_falls_back_to_part_id_when_code_is_numeric_and_no_barcode_match(self):
        part = Mock(part_id=7)
        with mock.patch('apps.inventory.views.Parts') as MockParts, \
                mock.patch.object(PartsViewSet, 'get_serializer', return_value=Mock(data={'part_id': 7})):
            self._patched_filter(MockParts, barcode_match=None, part_id_match=part)
            response = self._call(code='7')

        self.assertEqual(response.status_code, 200)

    def test_falls_back_to_part_name_when_code_is_not_numeric_and_no_barcode_match(self):
        part = Mock(part_id=3)
        with mock.patch('apps.inventory.views.Parts') as MockParts, \
                mock.patch.object(PartsViewSet, 'get_serializer', return_value=Mock(data={'part_id': 3})):
            self._patched_filter(MockParts, barcode_match=None, part_name_match=part)
            response = self._call(code='Brake Pad')

        self.assertEqual(response.status_code, 200)

    def test_no_match_anywhere_returns_404(self):
        with mock.patch('apps.inventory.views.Parts') as MockParts:
            self._patched_filter(MockParts)
            response = self._call(code='NOPE')

        self.assertEqual(response.status_code, 404)


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
