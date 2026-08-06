-- Phase 3: Transaction integrity
-- Run only after backing up: mysqldump inventory_db > backup_before_phase3_<date>.sql

-- PREFLIGHT: confirm current transaction_type distribution before altering
-- SELECT transaction_type, COUNT(*) FROM inventory_transactions GROUP BY transaction_type;

ALTER TABLE inventory_transactions
  ADD COLUMN created_by_id INT NULL AFTER part_id,
  ADD COLUMN source_reference VARCHAR(255) NULL AFTER created_by_id,
  ADD CONSTRAINT fk_inventory_transactions_created_by
    FOREIGN KEY (created_by_id) REFERENCES auth_user(id) ON DELETE SET NULL;

-- One-time data cleanup: normalize the 'Return to Suppler' typo to the canonical spelling
-- used by the new transaction_type choices enum.
UPDATE inventory_transactions
SET transaction_type = 'Return to Supplier'
WHERE transaction_type = 'Return to Suppler';
