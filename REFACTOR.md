# Database Restructure — Checklist & Plan

Target conventions:
- Every table has a single surrogate primary key named `id`.
- Foreign keys reference the **primary key** of the parent, never a "natural" business column.
- Money = `DECIMAL(12,2)`; dates = `DATE`/`DATETIME`; booleans = `tinyint(1)`.
- Column/table names are `snake_case`, no spaces or punctuation.

The companion script `restructure.sql` implements this in phases. **Run it phase by phase, not all at once**, and run the `-- PREFLIGHT` queries before any phase marked *DATA-DEPENDENT* — those phases fail or mislink data if the underlying values aren't clean.

> ⚠️ **Back up first.** `mysqldump inventory_db > backup_before_refactor.sql`. Most of this is irreversible (dropped FKs, dropped tables, type changes).

---

## Run order

| Phase | Scope | Risk | Turnkey? |
|-------|-------|------|----------|
| 0 | Backup + pre-checks | — | run the SELECTs |
| 1 | **Tier 1** — fix broken/inverted FKs | Medium | ✅ yes |
| 2 | **Tier 6** — drop legacy space-named tables | Low (destructive) | ✅ yes* |
| 3 | **Tier 5** — drop vestigial columns, fix illegal identifiers | Low | ✅ yes |
| 4 | **Tier 4** — money → DECIMAL | Low | ✅ yes |
| 5 | **Tier 4** — text dates → DATE, `Year` → SMALLINT | High | ⚠️ DATA-DEPENDENT |
| 6 | **Tier 2/3** — repoint FKs to `id`, add missing FKs | High | ⚠️ DATA-DEPENDENT |
| 7 | Full `snake_case` rename + `text`→`VARCHAR` sweep | Medium | ⚠️ mechanical, deferred |

\* Phase 2 keeps **both** asset-mapping tables — they need a manual merge (neither is complete). See "Asset mapping" below.

---

## Tier 1 — Broken / inverted foreign keys (Phase 1)

- **`suppliers`**: no PK; `id` is an inverted FK into `parts`. → drop the FK, add `PRIMARY KEY (id)`. Optionally add the correct-direction FK `parts.Supplier ID → suppliers.id`.
- **`inventory_transactions`**: FK `Signed Quantity → parts.On Hand` (a quantity, with `ON DELETE CASCADE`) and FK `id → parts.Part ID` (identity conflated with the part). → drop both, add a real `part_id` FK.
- **`build_sheets`**: duplicate FK, both pointing `Equipment ID → equipment_list.Build Sheet`; needless composite PK. → drop dupes, `PRIMARY KEY (id)`; re-add one clean FK in Phase 6.
- **`parts_has_equipment_list`**: composite FK matches `parts_Part ID` against `equipment_list.id`. → drop it; keep the correct FK to `parts`; add `equipment_list_id → equipment_list.id` in Phase 6.

## Tier 2 — FKs referencing non-unique columns (Phase 6)

FKs point at `equipment_list.Equipment ID` / `Build Sheet` / `Asset ID` and `suppliers.id`, none of which are unique/PK. Preferred fix: repoint children to the parent `id`. This is what removes every `to_field=` from the Django models.

## Tier 3 — Missing FKs (Phase 6)

`purchase_order_history.Part ID` (text), `repair_history.Asset ID` (text), `parts_diagrams.Component_Part ID`, and denormalized text (`Supplier Name`, `Manufacturer`, `Status`) should become enforced relationships.

## Tier 4 — Data types (Phases 4–5)

- Money as `double`/`float` → `DECIMAL(12,2)`: `purchase_order_history.Estimated/Actual Cost`, `sage_history.Total Cost`, `parts_suppliers.Price`.
- Text dates → `DATE`/`DATETIME` (many). Requires clean/parseable values.
- `equipment_list.Year` `double` → `SMALLINT`.
- `text` → `VARCHAR(n)` for short/key/lookup fields (Phase 7).

## Tier 5 — Naming (Phases 3 & 7)

- Illegal identifiers to fix now: leading space in `parts_suppliers.` `` Supplier ID``, plus `Active?`, `Serial Number!`, `Invoice #`, `Brand / Model`, etc.
- Vestigial columns to drop: `parts_suppliers.id`, Airtable rollups like `parts.Supplier Name (from Supplier Name)`, and (eventually) `airtable_id`.
- Full `snake_case` sweep of the remaining ~200 columns is Phase 7 (mechanical; do as its own reviewed batch).

## Tier 6 — Drop legacy tables (Phase 2)

All space-named Airtable dumps (`equipment list`, `parts diagrams`, `repair history`, …) — confirm no unique data first.

## Tier 7 — Indexes (folded into phases above)

- Make FK-referenced invisible indexes visible (`equipment_list.equipment_id`, `parts.signed_quantity`).
- Drop redundant indexes (two on `inventory_transactions.Signed Quantity`, the composite `parts_equipment_id`).

---

## Asset mapping (manual merge — do not auto-drop)

`asset ↔ equipment mapping` (legacy) has the real int FK to `equipment_list` but no PK.
`asset_equipment_mapping` (clean) has an `id` PK but stores `Asset ID` as text and has no FK.

Merge into a single `asset_equipment_mapping` with **both** an `id` PK and an integer `asset_id` FK → `equipment_list.id`. Because the clean table's `Asset ID` is text, you must verify those values map cleanly to equipment before adding the FK (see Phase 6 preflight). Only drop the legacy table once its relationships are migrated.

---

## After the restructure

1. `python manage.py inspectdb > apps/inventory/models_new.py` and diff against the current models — expect far fewer `db_column=`s, no duplicate classes, real `ForeignKey`s, and no `to_field`.
2. Fold the clean models in, then build `admin.py` on top (the original goal).
