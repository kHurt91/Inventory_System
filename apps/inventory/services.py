from django.db import transaction
from django.db.models import F

from .models import InventoryTransactions, Parts

TransactionType = InventoryTransactions.TransactionType

_SIGN_BY_TRANSACTION_TYPE = {
    TransactionType.RECEIVE_FROM_SUPPLIER: 1,
    TransactionType.RETURN: 1,
    TransactionType.ISSUE: -1,
    TransactionType.RETURN_TO_SUPPLIER: -1,
}


class InsufficientStockError(Exception):
    """Raised when applying a transaction would drive Parts.on_hand below zero."""


def compute_signed_quantity(transaction_type, quantity):
    if quantity is None:
        return None
    sign = _SIGN_BY_TRANSACTION_TYPE.get(transaction_type)
    if sign is None:
        return None
    return sign * abs(quantity)


def compute_needs_reorder(on_hand, reorder_point):
    """
    Single source of truth for the needs_reorder derivation, shared by
    record_transaction(), the scan_reorder_alerts command, and PartsAdmin --
    every place Parts.on_hand or Parts.reorder_point can change. Threshold-based
    if a reorder_point is configured, otherwise falls back to "out of stock".
    """
    on_hand = on_hand or 0
    if reorder_point is not None:
        return on_hand <= reorder_point
    return on_hand <= 0


def record_transaction(*, part, transaction_type, quantity, created_by=None, source_reference=None):
    """
    Create an InventoryTransactions row and, if `part` is set, atomically apply
    its effect to Parts.on_hand. signed_quantity is always server-computed from
    transaction_type + quantity -- it is never accepted from the client, so
    there is exactly one source of truth for the sign.
    """
    signed_quantity = compute_signed_quantity(transaction_type, quantity)

    with transaction.atomic():
        if part is not None and signed_quantity is not None:
            locked_part = Parts.objects.select_for_update().get(pk=part.pk)
            new_on_hand = (locked_part.on_hand or 0) + signed_quantity
            if new_on_hand < 0:
                raise InsufficientStockError(
                    f"Applying this transaction would take Part {part.pk} on_hand "
                    f"from {locked_part.on_hand or 0} to {new_on_hand}."
                )
            update_fields = {
                'on_hand': F('on_hand') + signed_quantity,
                'needs_reorder': int(compute_needs_reorder(new_on_hand, locked_part.reorder_point)),
            }
            Parts.objects.filter(pk=part.pk).update(**update_fields)

        return InventoryTransactions.objects.create(
            part=part,
            transaction_type=transaction_type,
            quantity=quantity,
            signed_quantity=signed_quantity,
            created_by=created_by,
            source_reference=source_reference or None,
        )
