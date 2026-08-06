-- Phase 4: Reorder management
-- Run only after backing up: mysqldump inventory_db > backup_before_phase4_<date>.sql

ALTER TABLE parts
  ADD COLUMN reorder_point INT NULL AFTER needs_reorder,
  ADD COLUMN reorder_quantity INT NULL AFTER reorder_point;
