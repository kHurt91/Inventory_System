from collections import defaultdict

from django.db import transaction
from django.utils import timezone

from .models import PartsSuppliers, PurchaseOrder, PurchaseOrderLine
from .services import TransactionType, record_transaction


class InvalidPurchaseOrderStateError(Exception):
    """Raised when a purchase order action is attempted from an invalid status."""


def draft_purchase_orders_from_reorder_alerts(parts, created_by=None):
    """
    Given an iterable of Parts flagged for reorder, group them by their assigned
    supplier and create one DRAFT PurchaseOrder per supplier with a line per part.
    Unit price is snapshotted from PartsSuppliers at draft time -- not looked up
    live later -- so a submitted/received PO reflects the price it was actually
    drafted against, even if supplier pricing changes afterward.

    Parts with no supplier assigned are skipped: there is nothing to draft against.
    Returns the list of created PurchaseOrder objects (empty if nothing to draft).
    """
    by_supplier = defaultdict(list)
    for part in parts:
        if part.supplier_id is not None:
            by_supplier[part.supplier_id].append(part)

    created_orders = []
    for supplier_id, supplier_parts in by_supplier.items():
        with transaction.atomic():
            po = PurchaseOrder.objects.create(
                supplier_id=supplier_id,
                status=PurchaseOrder.Status.DRAFT,
                auto_generated=True,
                created_by=created_by,
            )
            for part in supplier_parts:
                price = (
                    PartsSuppliers.objects.filter(part=part, supplier_id=supplier_id)
                    .values_list('price', flat=True)
                    .first()
                )
                PurchaseOrderLine.objects.create(
                    purchase_order=po,
                    part=part,
                    quantity_ordered=part.reorder_quantity or 1,
                    unit_price=price,
                )
            created_orders.append(po)
    return created_orders


def submit_purchase_order(purchase_order):
    """Move a DRAFT purchase order to SUBMITTED. Requires at least one line."""
    if purchase_order.status != PurchaseOrder.Status.DRAFT:
        raise InvalidPurchaseOrderStateError(
            f"Cannot submit PO #{purchase_order.pk}: status is '{purchase_order.status}', not 'Draft'."
        )
    if not purchase_order.lines.exists():
        raise InvalidPurchaseOrderStateError(f"Cannot submit PO #{purchase_order.pk}: it has no line items.")

    purchase_order.status = PurchaseOrder.Status.SUBMITTED
    purchase_order.submitted_at = timezone.now()
    purchase_order.save(update_fields=['status', 'submitted_at'])
    return purchase_order


def receive_purchase_order_line(*, line, quantity, created_by=None):
    """
    Receive `quantity` units against a single PurchaseOrderLine: posts a real
    InventoryTransactions row (via the existing record_transaction service, so
    Parts.on_hand/needs_reorder stay in sync the same way any other stock
    movement does), then updates the line's received count. Partial receiving
    across multiple deliveries is supported -- quantity_received accumulates.
    Once every line on the PO is fully received, the PO itself flips to RECEIVED.
    """
    purchase_order = line.purchase_order
    if purchase_order.status != PurchaseOrder.Status.SUBMITTED:
        raise InvalidPurchaseOrderStateError(
            f"Cannot receive against PO #{purchase_order.pk}: status is "
            f"'{purchase_order.status}', not 'Submitted'."
        )
    if quantity <= 0:
        raise ValueError("Received quantity must be positive.")

    remaining = line.quantity_ordered - line.quantity_received
    if quantity > remaining:
        raise ValueError(
            f"Cannot receive {quantity} against line {line.pk}: only {remaining} remain unreceived."
        )

    with transaction.atomic():
        record_transaction(
            part=line.part,
            transaction_type=TransactionType.RECEIVE_FROM_SUPPLIER,
            quantity=quantity,
            created_by=created_by,
            source_reference=f"PO-{purchase_order.pk}",
        )
        line.quantity_received += quantity
        line.save(update_fields=['quantity_received'])

        if all(l.quantity_received >= l.quantity_ordered for l in purchase_order.lines.all()):
            purchase_order.status = PurchaseOrder.Status.RECEIVED
            purchase_order.received_at = timezone.now()
            purchase_order.save(update_fields=['status', 'received_at'])

    return line
