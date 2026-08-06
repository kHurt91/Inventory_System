-- Phase 6: Mobile access
-- Run only after backing up: mysqldump inventory_db > backup_before_phase6_<date>.sql

-- barcode is nullable: existing parts have not been physically re-labeled yet,
-- so the lookup endpoint falls back to part_id/part_name/supplier_part_code
-- until a part is actually barcoded.
ALTER TABLE parts
  ADD COLUMN barcode VARCHAR(64) NULL AFTER part_name,
  ADD UNIQUE INDEX parts_barcode_uniq (barcode);
