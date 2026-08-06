from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from apps.inventory.models import Parts
from apps.inventory.purchasing_services import draft_purchase_orders_from_reorder_alerts
from apps.inventory.services import compute_needs_reorder


class Command(BaseCommand):
    help = (
        "Recompute needs_reorder for every Part -- using its reorder_point threshold "
        "if one is set, or falling back to 'out of stock' (on_hand <= 0) otherwise -- "
        "auto-draft purchase orders for newly-flagged parts, and email a digest."
    )

    def handle(self, *args, **options):
        parts = list(Parts.objects.all())

        newly_flagged = []
        for part in parts:
            was_flagged = bool(part.needs_reorder)
            is_flagged = compute_needs_reorder(part.on_hand, part.reorder_point)
            if is_flagged != was_flagged:
                Parts.objects.filter(pk=part.pk).update(needs_reorder=int(is_flagged))
            if is_flagged and not was_flagged:
                newly_flagged.append(part)

        self.stdout.write(
            f"Scanned {len(parts)} part(s); {len(newly_flagged)} newly flagged for reorder."
        )

        drafted_orders = []
        if newly_flagged:
            drafted_orders = draft_purchase_orders_from_reorder_alerts(newly_flagged)
            if drafted_orders:
                self.stdout.write(
                    f"Drafted {len(drafted_orders)} purchase order(s) for staff review: "
                    + ", ".join(f"#{po.pk} ({po.supplier.supplier_name})" for po in drafted_orders)
                )
            skipped = [p for p in newly_flagged if p.supplier_id is None]
            if skipped:
                self.stdout.write(
                    self.style.WARNING(
                        f"{len(skipped)} newly-flagged part(s) have no supplier assigned, "
                        "so no draft PO could be created for them: "
                        + ", ".join(str(p.part_id) for p in skipped)
                    )
                )

        if newly_flagged and settings.REORDER_ALERT_RECIPIENTS:
            lines = [
                f"- Part {p.part_id} ({p.part_description or 'no description'}): "
                f"on_hand={p.on_hand}, "
                + (
                    f"reorder_point={p.reorder_point}, reorder_quantity={p.reorder_quantity}"
                    if p.reorder_point is not None
                    else "out of stock (no reorder_point configured)"
                )
                for p in newly_flagged
            ]
            po_lines = [
                f"- Draft PO #{po.pk} created for supplier {po.supplier.supplier_name} "
                "(review and submit in the admin or API)"
                for po in drafted_orders
            ]
            message = "The following parts have dropped to or below their reorder point:\n\n" + "\n".join(lines)
            if po_lines:
                message += "\n\nDraft purchase orders were created automatically:\n\n" + "\n".join(po_lines)
            send_mail(
                subject=f"Low stock alert: {len(newly_flagged)} part(s) need reorder",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=settings.REORDER_ALERT_RECIPIENTS,
            )
            self.stdout.write(f"Sent low-stock digest to {', '.join(settings.REORDER_ALERT_RECIPIENTS)}.")
        elif newly_flagged:
            self.stdout.write(
                self.style.WARNING(
                    "Parts newly flagged for reorder, but REORDER_ALERT_RECIPIENTS is empty — no email sent."
                )
            )
