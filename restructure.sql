-- =====================================================================
-- inventory_db  —  schema restructure
-- Companion to REFACTOR.md.  MySQL 8.0.
--
-- HOW TO USE THIS FILE:
--   * DDL in MySQL auto-commits each statement — you CANNOT wrap the whole
--     script in one transaction and roll back. Run it PHASE BY PHASE.
--   * Before any phase marked "DATA-DEPENDENT", run its -- PREFLIGHT queries.
--     A preflight returning a non-zero count means data must be cleaned
--     BEFORE the ALTER, or the ALTER will fail / mislink rows.
--   * Take a backup first:
--         mysqldump -u root -p inventory_db > backup_before_refactor.sql
-- =====================================================================

-- ---------------------------------------------------------------------
-- PHASE 0 — pre-flight snapshot (read-only, safe to run anytime)
-- ---------------------------------------------------------------------
-- Row counts of the tables we will touch, so you can sanity-check after.
SELECT 'suppliers'              AS tbl, COUNT(*) AS rows FROM `suppliers`
UNION ALL SELECT 'parts',                COUNT(*) FROM `parts`
UNION ALL SELECT 'equipment_list',       COUNT(*) FROM `equipment_list`
UNION ALL SELECT 'inventory_transactions',COUNT(*) FROM `inventory_transactions`
UNION ALL SELECT 'build_sheets',          COUNT(*) FROM `build_sheets`
UNION ALL SELECT 'parts_has_equipment_list', COUNT(*) FROM `parts_has_equipment_list`
UNION ALL SELECT 'parts_suppliers',       COUNT(*) FROM `parts_suppliers`;


-- =====================================================================
-- PHASE 1 — TIER 1: fix broken / inverted foreign keys   (TURNKEY)
-- =====================================================================

-- 1a. suppliers: give it a real PK, remove the inverted FK into parts. -----
--     Currently: `id` AUTO_INCREMENT but NO primary key; instead
--     FOREIGN KEY (id) REFERENCES parts(`Supplier ID`).
ALTER TABLE `suppliers`
  DROP FOREIGN KEY `fk_suppliers_grid_view_parts1`;
--     Add the PK FIRST (keeps `id` indexed for the inbound FKs from
--     parts_suppliers / suppliers_logs / the grid-view), THEN drop the
--     now-redundant leftover index.
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`id`);
ALTER TABLE `suppliers`
  DROP INDEX `fk_suppliers_grid_view_parts1`;

--     OPTIONAL correct-direction link: parts.`Supplier ID` -> suppliers.id
--     PREFLIGHT (must return 0 before you add the FK):
--         SELECT COUNT(*) FROM `parts` p
--         LEFT JOIN `suppliers` s ON s.id = p.`Supplier ID`
--         WHERE p.`Supplier ID` IS NOT NULL AND s.id IS NULL;
-- ALTER TABLE `parts`
--   ADD CONSTRAINT `fk_parts_supplier`
--       FOREIGN KEY (`Supplier ID`) REFERENCES `suppliers` (`id`);


-- 1b. inventory_transactions: drop both bogus FKs, add a real part link. ---
ALTER TABLE `inventory_transactions`
  DROP FOREIGN KEY `fk_inventory_transactions_parts1`,   -- Signed Quantity -> parts.On Hand
  DROP FOREIGN KEY `fk_inventory_transactions_parts2`;   -- id -> parts.Part ID
ALTER TABLE `inventory_transactions`
  DROP INDEX `fk_inventory_transactions_parts1_idx`,     -- redundant indexes on Signed Quantity
  DROP INDEX `quantity`;
ALTER TABLE `inventory_transactions`
  ADD COLUMN `part_id` INT NULL AFTER `id`;

--     Seed the new column from the only signal the old schema carried:
--     the dropped FK forced transaction.id == parts.Part ID.
UPDATE `inventory_transactions` it
  JOIN `parts` p ON p.`Part ID` = it.id
  SET it.`part_id` = it.id;

--     PREFLIGHT (must return 0 — every non-null part_id must exist in parts):
--         SELECT COUNT(*) FROM `inventory_transactions` it
--         LEFT JOIN `parts` p ON p.`Part ID` = it.part_id
--         WHERE it.part_id IS NOT NULL AND p.`Part ID` IS NULL;
ALTER TABLE `inventory_transactions`
  ADD KEY `ix_inventory_transactions_part` (`part_id`),
  ADD CONSTRAINT `fk_inventory_transactions_parts`
      FOREIGN KEY (`part_id`) REFERENCES `parts` (`Part ID`);
--     `Signed Quantity` stays a plain bigint amount (no longer a FK) — correct.


-- 1c. build_sheets: drop duplicate FKs and the needless composite PK. ------
ALTER TABLE `build_sheets`
  DROP FOREIGN KEY `fk_build_sheets_equipment_list1`,
  DROP FOREIGN KEY `fk_build_sheets_equipment_list2`;
ALTER TABLE `build_sheets`
  DROP PRIMARY KEY,
  ADD PRIMARY KEY (`id`);
--     The correct FK (equipment_id -> equipment_list.id) is added in PHASE 6,
--     because the current `Equipment ID` values point at equipment_list.`Build Sheet`
--     and must be remapped first.


-- 1d. parts_has_equipment_list: drop the mis-mapped composite FK. ----------
ALTER TABLE `parts_has_equipment_list`
  DROP FOREIGN KEY `fk_parts_has_equipment_list_equipment_list1`;  -- mapped part# to equipment.id
--     The good FK (parts_Part ID -> parts.Part ID) is retained.
--     equipment_list_id -> equipment_list.id is added in PHASE 6.


-- =====================================================================
-- PHASE 2 — TIER 6: drop legacy space-named tables         (DESTRUCTIVE)
--   Confirm no unique data lives ONLY in these before running.
--   NOTE: the two asset-mapping tables are intentionally NOT dropped here
--         (they need the manual merge in PHASE 6 / REFACTOR.md).
-- =====================================================================
DROP TABLE IF EXISTS `build sheets`;
DROP TABLE IF EXISTS `equipment list`;
DROP TABLE IF EXISTS `inventory transactions`;
DROP TABLE IF EXISTS `office & cleaning supplies`;
DROP TABLE IF EXISTS `office supply transactions`;
DROP TABLE IF EXISTS `parts diagrams`;
DROP TABLE IF EXISTS `purchase order history`;
DROP TABLE IF EXISTS `purchase order import staging`;
DROP TABLE IF EXISTS `purchase order upload intake`;
DROP TABLE IF EXISTS `repair history`;
DROP TABLE IF EXISTS `repair import staging`;
DROP TABLE IF EXISTS `repair upload intake`;
DROP TABLE IF EXISTS `sage history`;
DROP TABLE IF EXISTS `sage import staging`;
DROP TABLE IF EXISTS `sage upload intake`;
DROP TABLE IF EXISTS `supplier logs`;
DROP TABLE IF EXISTS `update equipment requests`;
DROP TABLE IF EXISTS `update part requests`;
DROP TABLE IF EXISTS `update supplier requests`;


-- =====================================================================
-- PHASE 3 — TIER 5: vestigial columns + illegal identifiers  (TURNKEY)
-- =====================================================================

-- 3a. parts_suppliers: drop the unused `id`, fix the LEADING-SPACE column
--     name and snake_case the key columns. Both FKs are dropped and
--     recreated so the constraint metadata tracks the renames.
ALTER TABLE `parts_suppliers`
  DROP FOREIGN KEY `fk_parts_suppliers_parts1`,
  DROP FOREIGN KEY `fk_parts_suppliers_suppliers_grid_view1`;
ALTER TABLE `parts_suppliers`
  DROP COLUMN `id`,
  CHANGE COLUMN `Part ID`      `part_id`     INT NOT NULL,
  CHANGE COLUMN ` Supplier ID` `supplier_id` INT NOT NULL,      -- note: leading space removed
  CHANGE COLUMN `Supplier Part Code` `supplier_part_code` TEXT,
  CHANGE COLUMN `Price`        `price`       DECIMAL(12,2) DEFAULT NULL;  -- money fix too
ALTER TABLE `parts_suppliers`
  ADD CONSTRAINT `fk_parts_suppliers_parts`
      FOREIGN KEY (`part_id`)     REFERENCES `parts` (`Part ID`),
  ADD CONSTRAINT `fk_parts_suppliers_suppliers`
      FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`);

-- 3b. Drop obvious Airtable rollup leftovers (add/remove to taste).
ALTER TABLE `parts`
  DROP COLUMN `Supplier Name (from Supplier Name)`;

-- 3c. Fix illegal identifiers on the core tables (`?`, `!`, `#`, `/`, spaces).
ALTER TABLE `equipment_list`
  CHANGE COLUMN `Serial Number!` `serial_number_alt` TEXT;
ALTER TABLE `suppliers_logs`
  CHANGE COLUMN `Supplier_ID` `supplier_id` INT DEFAULT NULL;   -- already FK'd; rename only
ALTER TABLE `purchase_order_history`
  CHANGE COLUMN `Invoice #`                  `invoice_number`      VARCHAR(64) DEFAULT NULL,
  CHANGE COLUMN `Shipper / Packing Slip #`   `shipper_packing_slip` TEXT;
--  (The remaining `?`/`#` columns live on staging tables — handled in PHASE 7.)


-- =====================================================================
-- PHASE 4 — TIER 4: money -> DECIMAL                          (TURNKEY)
--   double/float -> DECIMAL(12,2). Values are re-rounded to 2 dp.
-- =====================================================================
ALTER TABLE `purchase_order_history`
  MODIFY COLUMN `Estimated Cost` DECIMAL(12,2) DEFAULT NULL,
  MODIFY COLUMN `Actual Cost`    DECIMAL(12,2) DEFAULT NULL;
ALTER TABLE `sage_history`
  MODIFY COLUMN `Total Cost`     DECIMAL(12,2) DEFAULT NULL;
-- (parts_suppliers.price was already converted in 3a.)


-- =====================================================================
-- PHASE 5 — TIER 4: text dates -> DATE ; Year -> SMALLINT   (DATA-DEPENDENT)
--   Text dates only convert cleanly if every value parses. Verify first.
-- =====================================================================

-- 5a. Year: PREFLIGHT (must return 0 — every value must be a whole 4-digit year):
--         SELECT COUNT(*) FROM `equipment_list`
--         WHERE `Year` IS NOT NULL AND (`Year` <> FLOOR(`Year`) OR `Year` NOT BETWEEN 1900 AND 2100);
ALTER TABLE `equipment_list`
  MODIFY COLUMN `Year` SMALLINT DEFAULT NULL;

-- 5b. Dates: inspect the actual string format BEFORE converting.
--     PREFLIGHT — list any values MySQL cannot parse as a date:
--         SELECT `Date Issued` FROM `repair_history`
--         WHERE `Date Issued` IS NOT NULL AND STR_TO_DATE(`Date Issued`,'%Y-%m-%d') IS NULL
--         LIMIT 50;
--     If the format differs (e.g. m/d/Y), adjust the format string, then:
-- UPDATE `repair_history`
--   SET `Date Issued`    = STR_TO_DATE(`Date Issued`,    '%Y-%m-%d'),
--       `Date Needed`    = STR_TO_DATE(`Date Needed`,    '%Y-%m-%d'),
--       `Date Completed` = STR_TO_DATE(`Date Completed`, '%Y-%m-%d');
-- ALTER TABLE `repair_history`
--   MODIFY COLUMN `Date Issued`    DATE DEFAULT NULL,
--   MODIFY COLUMN `Date Needed`    DATE DEFAULT NULL,
--   MODIFY COLUMN `Date Completed` DATE DEFAULT NULL;
--     Repeat the same pattern for purchase_order_history / sage_history date columns
--     and the *_import_staging / *_upload_intake `Imported At` (use DATETIME) columns.


-- =====================================================================
-- PHASE 6 — TIER 2/3: repoint FKs onto primary keys + add missing FKs
--                                                          (DATA-DEPENDENT)
--   These convert "natural key" links (Equipment ID, Build Sheet, Asset ID)
--   into surrogate-key links against equipment_list.id. Each needs a mapping
--   step + preflight; do ONE table at a time and verify counts.
-- =====================================================================

-- 6a. Make the FK-referenced invisible index usable, and (optionally) enforce
--     uniqueness on the business key so repointing is unambiguous.
ALTER TABLE `equipment_list` ALTER INDEX `equipment_id` VISIBLE;
--     PREFLIGHT for uniqueness (must return 0 duplicates before adding UNIQUE):
--         SELECT `Equipment ID`, COUNT(*) c FROM `equipment_list`
--         WHERE `Equipment ID` IS NOT NULL GROUP BY `Equipment ID` HAVING c > 1;
-- ALTER TABLE `equipment_list` ADD UNIQUE KEY `uq_equipment_id` (`Equipment ID`);

-- 6b. Template — repoint a child from equipment_list.`Equipment ID` to .id.
--     Example: purchase_order_history.
--     Step 1: add the new surrogate FK column.
-- ALTER TABLE `purchase_order_history` ADD COLUMN `equipment_ref_id` INT NULL;
--     Step 2: map via the business key.
-- UPDATE `purchase_order_history` c
--   JOIN `equipment_list` e ON e.`Equipment ID` = c.`Equipment ID`
--   SET c.`equipment_ref_id` = e.`id`;
--     Step 3: PREFLIGHT — any child rows that failed to map?
--         SELECT COUNT(*) FROM `purchase_order_history`
--         WHERE `Equipment ID` IS NOT NULL AND `equipment_ref_id` IS NULL;
--     Step 4: drop old FK/col, swap in the new constraint.
-- ALTER TABLE `purchase_order_history`
--   DROP FOREIGN KEY `fk_purchase_order_history_equipment_list1`,
--   DROP COLUMN `Equipment ID`,
--   CHANGE COLUMN `equipment_ref_id` `equipment_id` INT NULL,
--   ADD CONSTRAINT `fk_poh_equipment`
--       FOREIGN KEY (`equipment_id`) REFERENCES `equipment_list` (`id`);
--
--     Apply the same 4-step pattern to:
--       parts_diagrams   (Equipment ID -> equipment_list.id)
--       repair_history   (Equipment ID -> equipment_list.id)
--       build_sheets     (Equipment ID -> equipment_list.id)   [FK re-added here]
--       parts_has_equipment_list (equipment_list_id -> equipment_list.id)

-- 6c. Missing FKs on text columns — convert then link. DATA-DEPENDENT.
--     purchase_order_history.`Part ID` is TEXT; verify all are numeric & exist:
--         SELECT COUNT(*) FROM `purchase_order_history` c
--         LEFT JOIN `parts` p ON p.`Part ID` = c.`Part ID`
--         WHERE c.`Part ID` IS NOT NULL AND (c.`Part ID` NOT REGEXP '^[0-9]+$' OR p.`Part ID` IS NULL);
-- ALTER TABLE `purchase_order_history` MODIFY COLUMN `Part ID` INT NULL;
-- ALTER TABLE `purchase_order_history`
--   ADD CONSTRAINT `fk_poh_part` FOREIGN KEY (`Part ID`) REFERENCES `parts` (`Part ID`);


-- =====================================================================
-- PHASE 7 — full snake_case + text->VARCHAR sweep            (DEFERRED)
--   ~200 columns, purely mechanical. Do as its own reviewed batch using
--   the CHANGE COLUMN pattern shown in PHASE 3. Recommended after 1-6 pass
--   and the app/models have been re-generated and tested.
--   Example pattern:
--     ALTER TABLE `equipment_list`
--       CHANGE COLUMN `Record ID`      `record_id`      VARCHAR(64),
--       CHANGE COLUMN `Make`           `make`           VARCHAR(100),
--       CHANGE COLUMN `Model`          `model`          VARCHAR(100),
--       CHANGE COLUMN `Asset Category` `asset_category` VARCHAR(100),
--       ...
-- =====================================================================
