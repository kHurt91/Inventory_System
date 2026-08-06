-- Completes the remaining gaps of the restructure against the CURRENT schema
-- (2026-07-13). Every step here was preflighted: 0 orphans / 0 unparseable.
SET SQL_SAFE_UPDATES = 0;

-- 1) Money: double/float -> DECIMAL(12,2)
ALTER TABLE `purchase_order_history`
  MODIFY COLUMN `estimated_cost` DECIMAL(12,2) DEFAULT NULL,
  MODIFY COLUMN `actual_cost`    DECIMAL(12,2) DEFAULT NULL;
ALTER TABLE `sage_history`
  MODIFY COLUMN `total_cost` DECIMAL(12,2) DEFAULT NULL;
ALTER TABLE `parts_suppliers`
  MODIFY COLUMN `price` DECIMAL(12,2) DEFAULT NULL;

-- 2) Text dates -> DATE (normalize empties to NULL first)
UPDATE `purchase_order_history`
  SET `date_issued`   = STR_TO_DATE(NULLIF(`date_issued`,''),  '%Y-%m-%d'),
      `received_date` = STR_TO_DATE(NULLIF(`received_date`,''),'%Y-%m-%d');
ALTER TABLE `purchase_order_history`
  MODIFY COLUMN `date_issued`   DATE DEFAULT NULL,
  MODIFY COLUMN `received_date` DATE DEFAULT NULL;

UPDATE `repair_history`
  SET `date_needed`    = STR_TO_DATE(NULLIF(`date_needed`,''),   '%Y-%m-%d'),
      `date_issued`    = STR_TO_DATE(NULLIF(`date_issued`,''),   '%Y-%m-%d'),
      `date_completed` = STR_TO_DATE(NULLIF(`date_completed`,''),'%Y-%m-%d');
ALTER TABLE `repair_history`
  MODIFY COLUMN `date_needed`    DATE DEFAULT NULL,
  MODIFY COLUMN `date_issued`    DATE DEFAULT NULL,
  MODIFY COLUMN `date_completed` DATE DEFAULT NULL;

UPDATE `sage_history`
  SET `date` = STR_TO_DATE(NULLIF(`date`,''), '%Y-%m-%d');
ALTER TABLE `sage_history`
  MODIFY COLUMN `date` DATE DEFAULT NULL;

-- 3) purchase_order_history.part_id: text -> INT, then enforce FK -> parts
UPDATE `purchase_order_history` SET `part_id` = NULLIF(`part_id`,'');
ALTER TABLE `purchase_order_history`
  MODIFY COLUMN `part_id` INT DEFAULT NULL;
ALTER TABLE `purchase_order_history`
  ADD KEY `ix_poh_part` (`part_id`),
  ADD CONSTRAINT `fk_poh_part` FOREIGN KEY (`part_id`) REFERENCES `parts` (`part_id`);

-- 4) Add the missing foreign keys (indexes already exist)
ALTER TABLE `inventory_transactions`
  ADD CONSTRAINT `fk_inventory_transactions_parts`
      FOREIGN KEY (`part_id`) REFERENCES `parts` (`part_id`);
ALTER TABLE `parts`
  ADD CONSTRAINT `fk_parts_supplier`
      FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`);
ALTER TABLE `office_and_cleaning_supplies`
  ADD CONSTRAINT `fk_ocs_supplier`
      FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`);

-- 5) Drop the empty legacy leftover table
DROP TABLE IF EXISTS `purchase order history`;

SET SQL_SAFE_UPDATES = 1;
