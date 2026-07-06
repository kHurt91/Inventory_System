-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: inventory_db
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `asset ↔ equipment mapping`
--

DROP TABLE IF EXISTS `asset ↔ equipment mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asset ↔ equipment mapping` (
  `Last Updated` text,
  `Asset ID` int DEFAULT NULL,
  `Equipment ID` text,
  `Active?` tinyint(1) DEFAULT NULL,
  `airtable_id` text,
  `Equipment List 2` text,
  `Mapping Status` text,
  KEY `fk_asset ↔ equipment mapping_equipment_list1_idx` (`Asset ID`),
  CONSTRAINT `fk_asset ↔ equipment mapping_equipment_list1` FOREIGN KEY (`Asset ID`) REFERENCES `equipment_list` (`Asset ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `asset_equipment_mapping`
--

DROP TABLE IF EXISTS `asset_equipment_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asset_equipment_mapping` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Last Updated` text,
  `Asset ID` text,
  `Equipment ID` text,
  `Active?` tinyint(1) DEFAULT NULL,
  `airtable_id` text,
  `Equipment List 2` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=295 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `build sheets`
--

DROP TABLE IF EXISTS `build sheets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `build sheets` (
  `airtable_id` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `build_sheets`
--

DROP TABLE IF EXISTS `build_sheets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `build_sheets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Name` text,
  `Build Sheet` text,
  `Equipment ID` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`,`Equipment ID`),
  KEY `fk_build_sheets_equipment_list1_idx` (`Equipment ID`),
  CONSTRAINT `fk_build_sheets_equipment_list1` FOREIGN KEY (`Equipment ID`) REFERENCES `equipment_list` (`Build Sheet`),
  CONSTRAINT `fk_build_sheets_equipment_list2` FOREIGN KEY (`Equipment ID`) REFERENCES `equipment_list` (`Build Sheet`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `equipment list`
--

DROP TABLE IF EXISTS `equipment list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment list` (
  `Record ID` text,
  `Make` text,
  `Model` text,
  `Owned By` text,
  `Year` double DEFAULT NULL,
  `Asset Category` text,
  `Equipment ID` text,
  `airtable_id` text,
  `Serial Number` text,
  `Equipment Notes` text,
  `Part Compatibility` text,
  `Tires` text,
  `Manuals` text,
  `Status` text,
  `Serial Number!` text,
  `Notes` text,
  `Equipment Name` text,
  `Update Equipment Requests` text,
  `Asset ID (from Asset ↔ Equipment Mapping)` text,
  `Repair History 2` text,
  `Asset ID (From Equip Dbase)` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `equipment_list`
--

DROP TABLE IF EXISTS `equipment_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_list` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Record ID` text,
  `Make` text,
  `Model` text,
  `Owned By` text,
  `Year` double DEFAULT NULL,
  `Asset Category` text,
  `Equipment ID` int DEFAULT NULL,
  `airtable_id` text,
  `Serial Number` text,
  `Equipment Notes` text,
  `Part Compatibility` text,
  `Tires` text,
  `Manuals` text,
  `Status` text,
  `Build Sheet` int DEFAULT NULL,
  `Asset ID` int DEFAULT NULL,
  `ALT Asset ID` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Asset_id` (`Asset ID`),
  KEY `build_sheet` (`Build Sheet`),
  KEY `equipment_id` (`Equipment ID`) /*!80000 INVISIBLE */,
  KEY `parts_equipment_id` (`id`,`Equipment ID`)
) ENGINE=InnoDB AUTO_INCREMENT=294 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventory transactions`
--

DROP TABLE IF EXISTS `inventory transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory transactions` (
  `Signed Quantity` text,
  `Transaction Type` text,
  `Created Time` text,
  `Quantity` bigint DEFAULT NULL,
  `airtable_id` text,
  `Part ID` text,
  `Notes` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventory_transactions`
--

DROP TABLE IF EXISTS `inventory_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Signed Quantity` bigint DEFAULT NULL,
  `Transaction Type` text,
  `Created Time` text,
  `Quantity` bigint DEFAULT NULL,
  `airtable_id` text,
  `Notes` text,
  PRIMARY KEY (`id`),
  KEY `fk_inventory_transactions_parts1_idx` (`Signed Quantity`),
  KEY `quantity` (`Signed Quantity`),
  CONSTRAINT `fk_inventory_transactions_parts1` FOREIGN KEY (`Signed Quantity`) REFERENCES `parts` (`On Hand`) ON DELETE CASCADE,
  CONSTRAINT `fk_inventory_transactions_parts2` FOREIGN KEY (`id`) REFERENCES `parts` (`Part ID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `office & cleaning supplies`
--

DROP TABLE IF EXISTS `office & cleaning supplies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `office & cleaning supplies` (
  `Status` text,
  `Minimum Quantity` bigint DEFAULT NULL,
  `Category` text,
  `In-Stock Location` text,
  `Office Supply Transactions` text,
  `On Hand` bigint DEFAULT NULL,
  `Supply Name` text,
  `airtable_id` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `office supply transactions`
--

DROP TABLE IF EXISTS `office supply transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `office supply transactions` (
  `Supply Name` text,
  `Transaction Type` text,
  `airtable_id` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `office_and_cleaning_supplies`
--

DROP TABLE IF EXISTS `office_and_cleaning_supplies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `office_and_cleaning_supplies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Status` text,
  `Minimum Quantity` bigint DEFAULT NULL,
  `Category` text,
  `In-Stock Location` text,
  `Office Supply Transactions` text,
  `On Hand` bigint DEFAULT NULL,
  `Supply Name` text,
  `airtable_id` text,
  `Supplier Name` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `office_and_cleaning_supplies_has_suppliers_grid_view`
--

DROP TABLE IF EXISTS `office_and_cleaning_supplies_has_suppliers_grid_view`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `office_and_cleaning_supplies_has_suppliers_grid_view` (
  `office_and_cleaning_supplies_id` int NOT NULL,
  `suppliers_grid_view_id` int NOT NULL,
  PRIMARY KEY (`office_and_cleaning_supplies_id`,`suppliers_grid_view_id`),
  KEY `fk_office_and_cleaning_supplies_has_suppliers_grid_view_sup_idx` (`suppliers_grid_view_id`),
  KEY `fk_office_and_cleaning_supplies_has_suppliers_grid_view_off_idx` (`office_and_cleaning_supplies_id`),
  CONSTRAINT `fk_office_and_cleaning_supplies_has_suppliers_grid_view_offic1` FOREIGN KEY (`office_and_cleaning_supplies_id`) REFERENCES `office_and_cleaning_supplies` (`id`),
  CONSTRAINT `fk_office_and_cleaning_supplies_has_suppliers_grid_view_suppl1` FOREIGN KEY (`suppliers_grid_view_id`) REFERENCES `suppliers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `office_supply_transactions`
--

DROP TABLE IF EXISTS `office_supply_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `office_supply_transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Supply Name` text,
  `Transaction Type` text,
  `airtable_id` text,
  `office_supply_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_office_supply_transactions_office_and_cleaning_supplies1_idx` (`office_supply_id`),
  CONSTRAINT `fk_office_supply_transactions_office_and_cleaning_supplies1` FOREIGN KEY (`office_supply_id`) REFERENCES `office_and_cleaning_supplies` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parts`
--

DROP TABLE IF EXISTS `parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parts` (
  `Part Description` text,
  `In-Stock Location` text,
  `On Hand` bigint DEFAULT NULL,
  `Equipment Fitment` text,
  `Part ID` int NOT NULL AUTO_INCREMENT,
  `Record ID` int DEFAULT NULL,
  `Needs Reorder` tinyint DEFAULT NULL,
  `airtable_id` text,
  `Manufacturer` text,
  `Supplier ID` int DEFAULT NULL,
  `Alternate Supplier` text,
  `Supplier Name` text,
  `Cost Notes` text,
  `Brand / Model` text,
  `Part Name` text,
  `Update Part Requests` text,
  `Inventory Transactions` text,
  `Status` text,
  `Repair History` varchar(255) DEFAULT NULL,
  `Sage History` varchar(255) DEFAULT NULL,
  `Supplier Name (from Supplier Name)` text,
  PRIMARY KEY (`Part ID`),
  KEY `signed_quantity` (`On Hand`) /*!80000 INVISIBLE */,
  KEY `repair_history` (`Repair History`) /*!80000 INVISIBLE */,
  KEY `sage_history` (`Sage History`),
  KEY `supplier_id` (`Supplier ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1053 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parts diagrams`
--

DROP TABLE IF EXISTS `parts diagrams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parts diagrams` (
  `airtable_id` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parts_diagrams`
--

DROP TABLE IF EXISTS `parts_diagrams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parts_diagrams` (
  `id` int NOT NULL AUTO_INCREMENT,
  `airtable_id` text,
  `Notes` text,
  `Attachments` text,
  `Equipment ID` int DEFAULT NULL,
  `Diagram Description` text,
  `Component_Part ID` int DEFAULT NULL,
  `Date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_parts_diagram_equipment_list1_idx` (`Equipment ID`),
  CONSTRAINT `fk_parts_diagram_equipment_list1` FOREIGN KEY (`Equipment ID`) REFERENCES `equipment_list` (`Equipment ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parts_has_equipment_list`
--

DROP TABLE IF EXISTS `parts_has_equipment_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parts_has_equipment_list` (
  `parts_Part ID` int NOT NULL,
  `equipment_list_id` int NOT NULL,
  PRIMARY KEY (`parts_Part ID`,`equipment_list_id`),
  KEY `fk_parts_has_equipment_list_parts1_idx` (`parts_Part ID`),
  CONSTRAINT `fk_parts_has_equipment_list_equipment_list1` FOREIGN KEY (`parts_Part ID`, `equipment_list_id`) REFERENCES `equipment_list` (`id`, `Equipment ID`),
  CONSTRAINT `fk_parts_has_equipment_list_parts1` FOREIGN KEY (`parts_Part ID`) REFERENCES `parts` (`Part ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parts_suppliers`
--

DROP TABLE IF EXISTS `parts_suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parts_suppliers` (
  `id` int NOT NULL,
  `Part ID` int NOT NULL,
  ` Supplier ID` int NOT NULL,
  `Supplier Part Code` text,
  `Price` float DEFAULT NULL,
  PRIMARY KEY (`Part ID`,` Supplier ID`),
  KEY `fk_parts_suppliers_suppliers_grid_view1_idx` (` Supplier ID`),
  CONSTRAINT `fk_parts_suppliers_parts1` FOREIGN KEY (`Part ID`) REFERENCES `parts` (`Part ID`),
  CONSTRAINT `fk_parts_suppliers_suppliers_grid_view1` FOREIGN KEY (` Supplier ID`) REFERENCES `suppliers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `purchase order history`
--

DROP TABLE IF EXISTS `purchase order history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase order history` (
  `Part Description` text,
  `Part ID` text,
  `Date Issued` text,
  `Invoice #` decimal(22,1) DEFAULT NULL,
  `PO` text,
  `Estimated Cost` double DEFAULT NULL,
  `Company` text,
  `Supplier` text,
  `Actual Cost` double DEFAULT NULL,
  `Received Date` text,
  `Issued By` text,
  `airtable_id` text,
  `Shipper / Packing Slip #` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `purchase order import staging`
--

DROP TABLE IF EXISTS `purchase order import staging`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase order import staging` (
  `Mapped Actual Cost` double DEFAULT NULL,
  `Row Number` double DEFAULT NULL,
  `Name` text,
  `Notes` text,
  `Mapped Company` text,
  `Imported At` text,
  `Import Batch ID` text,
  `Raw JSON` text,
  `Mapping Status` text,
  `Error Message` text,
  `Attachment Summary` text,
  `Status` text,
  `Source Filename` text,
  `airtable_id` text,
  `Mapped Equipment ID` text,
  `Import Notes` text,
  `Mapped Issued By` text,
  `Mapped Estimated Cost` double DEFAULT NULL,
  `Mapped Invoice #` double DEFAULT NULL,
  `Promoted?` tinyint(1) DEFAULT NULL,
  `Duplicate?` tinyint(1) DEFAULT NULL,
  `Mapped Part ID` text,
  `Mapped Shipper / Packing Slip #` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `purchase order upload intake`
--

DROP TABLE IF EXISTS `purchase order upload intake`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase order upload intake` (
  `Rows Created` bigint DEFAULT NULL,
  `Main File` text,
  `Parse Status` text,
  `Import Batch ID` text,
  `Imported At` text,
  `airtable_id` text,
  `Import Notes` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `purchase_order_history`
--

DROP TABLE IF EXISTS `purchase_order_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_order_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Part Description` text,
  `Part ID` text,
  `Date Issued` text,
  `Invoice #` decimal(22,1) DEFAULT NULL,
  `PO` text,
  `Estimated Cost` double DEFAULT NULL,
  `Company` text,
  `Supplier` text,
  `Actual Cost` double DEFAULT NULL,
  `Received Date` text,
  `Issued By` text,
  `airtable_id` text,
  `Shipper / Packing Slip #` text,
  `Equipment ID` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_purchase_order_history_equipment_list1_idx` (`Equipment ID`),
  CONSTRAINT `fk_purchase_order_history_equipment_list1` FOREIGN KEY (`Equipment ID`) REFERENCES `equipment_list` (`Equipment ID`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `purchase_order_import_staging`
--

DROP TABLE IF EXISTS `purchase_order_import_staging`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_order_import_staging` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Mapped Actual Cost` double DEFAULT NULL,
  `Row Number` double DEFAULT NULL,
  `Name` text,
  `Notes` text,
  `Mapped Company` text,
  `Imported At` text,
  `Import Batch ID` text,
  `Raw JSON` text,
  `Mapping Status` text,
  `Error Message` text,
  `Attachment Summary` text,
  `Status` text,
  `Source Filename` text,
  `airtable_id` text,
  `Mapped Equipment ID` text,
  `Import Notes` text,
  `Mapped Issued By` text,
  `Mapped Estimated Cost` double DEFAULT NULL,
  `Mapped Invoice #` double DEFAULT NULL,
  `Promoted?` tinyint(1) DEFAULT NULL,
  `Duplicate?` tinyint(1) DEFAULT NULL,
  `Mapped Part ID` text,
  `Mapped Shipper / Packing Slip #` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `purchase_order_upload_intake`
--

DROP TABLE IF EXISTS `purchase_order_upload_intake`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_order_upload_intake` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Rows Created` bigint DEFAULT NULL,
  `Main File` text,
  `Parse Status` text,
  `Import Batch ID` text,
  `Imported At` text,
  `airtable_id` text,
  `Import Notes` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `repair history`
--

DROP TABLE IF EXISTS `repair history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair history` (
  `Date Needed` text,
  `Date Issued` text,
  `Svc Description` text,
  `Reported By` text,
  `Asset ID` text,
  `Work Order #` text,
  `airtable_id` text,
  `Completed By` text,
  `Mechanic Notes` text,
  `Hours-to-Complete` double DEFAULT NULL,
  `Date Completed` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `repair import staging`
--

DROP TABLE IF EXISTS `repair import staging`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair import staging` (
  `Attachment Summary` text,
  `airtable_id` text,
  `Raw JSON` text,
  `Mapped Date Issued` text,
  `Row Number` double DEFAULT NULL,
  `Error Message` text,
  `Import Batch ID` text,
  `Mapped Date Fixed` text,
  `Source Filename` text,
  `Imported At` text,
  `Mapping Status` text,
  `Mapped Equipment ID` text,
  `Mapped Asset ID` text,
  `Import Notes` text,
  `Recheck Mapping?` tinyint(1) DEFAULT NULL,
  `Mapped Part ID` text,
  `Auto-Promote Eligible?` tinyint(1) DEFAULT NULL,
  `Promote Error` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `repair upload intake`
--

DROP TABLE IF EXISTS `repair upload intake`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair upload intake` (
  `airtable_id` text,
  `Imported At` text,
  `Import Batch ID` text,
  `Parse Status` text,
  `Rows Created` double DEFAULT NULL,
  `Main File` text,
  `Import Notes` text,
  `Source Filename` text,
  `Core Upload` text,
  `Parse Eligible?` tinyint(1) DEFAULT NULL,
  `Imported By Email` text,
  `Parse Error` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `repair_history`
--

DROP TABLE IF EXISTS `repair_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Date Needed` text,
  `Date Issued` text,
  `Svc Description` text,
  `Reported By` text,
  `Asset ID` text,
  `Work Order #` text,
  `airtable_id` text,
  `Completed By` text,
  `Mechanic Notes` text,
  `Hours-to-Complete` double DEFAULT NULL,
  `Date Completed` text,
  `Part ID` int DEFAULT NULL,
  `Equipment ID` int DEFAULT NULL,
  `Repair Import Staging` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_repair_history_parts1_idx` (`Part ID`),
  KEY `fk_repair_history_repair_import_staging1_idx` (`Repair Import Staging`),
  KEY `fk_repair_history_equipment_list1_idx` (`Equipment ID`),
  CONSTRAINT `fk_repair_history_equipment_list1` FOREIGN KEY (`Equipment ID`) REFERENCES `equipment_list` (`Equipment ID`),
  CONSTRAINT `fk_repair_history_parts1` FOREIGN KEY (`Part ID`) REFERENCES `parts` (`Part ID`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_repair_history_repair_import_staging1` FOREIGN KEY (`Repair Import Staging`) REFERENCES `repair_import_staging` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1661 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `repair_import_staging`
--

DROP TABLE IF EXISTS `repair_import_staging`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair_import_staging` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Attachment Summary` text,
  `airtable_id` text,
  `Raw JSON` text,
  `Mapped Date Issued` text,
  `Row Number` double DEFAULT NULL,
  `Error Message` text,
  `Import Batch ID` text,
  `Mapped Date Fixed` text,
  `Source Filename` text,
  `Imported At` text,
  `Mapping Status` text,
  `Mapped Equipment ID` text,
  `Mapped Asset ID` text,
  `Import Notes` text,
  `Recheck Mapping?` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=989 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `repair_upload_intake`
--

DROP TABLE IF EXISTS `repair_upload_intake`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair_upload_intake` (
  `id` int NOT NULL AUTO_INCREMENT,
  `airtable_id` text,
  `Imported At` text,
  `Import Batch ID` text,
  `Parse Status` text,
  `Rows Created` double DEFAULT NULL,
  `Main File` text,
  `Import Notes` text,
  `Source Filename` text,
  `Core Upload` text,
  `Parse Eligible?` tinyint(1) DEFAULT NULL,
  `Imported By Email` text,
  `Parse Error` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sage history`
--

DROP TABLE IF EXISTS `sage history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sage history` (
  `airtable_id` text,
  `Unit Number (Extracted from GL Number)` text,
  `Sage Transaction Type` text,
  `Sage Description` text,
  `Date` text,
  `General Ledger Number` text,
  `Supplier Information` text,
  `Total Cost` double DEFAULT NULL,
  `Sage Equipment` text,
  `Data Source` text,
  `Import Batch ID` text,
  `Sage Import Staging` text,
  `Import Key` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sage import staging`
--

DROP TABLE IF EXISTS `sage import staging`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sage import staging` (
  `Status` text,
  `Mapped Description` text,
  `Mapping Status` text,
  `Notes` text,
  `Imported At` text,
  `Raw JSON` text,
  `Name` text,
  `Error Message` text,
  `Source Filename` text,
  `Attachment Summary` text,
  `Import Batch ID` text,
  `Mapped GL` text,
  `Row Number` double DEFAULT NULL,
  `airtable_id` text,
  `Promoted At` text,
  `Mapped Cost` double DEFAULT NULL,
  `Mapped Date` text,
  `Sage History Link` text,
  `Promoted?` tinyint(1) DEFAULT NULL,
  `Import Notes` text,
  `Promote Error` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sage upload intake`
--

DROP TABLE IF EXISTS `sage upload intake`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sage upload intake` (
  `Rows Created` bigint DEFAULT NULL,
  `Source Filename` text,
  `Import Notes` text,
  `Imported At` text,
  `Import Batch ID` text,
  `Main File` text,
  `Parse Status` text,
  `airtable_id` text,
  `Core upload` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sage_history`
--

DROP TABLE IF EXISTS `sage_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sage_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Part ID` int DEFAULT NULL,
  `Unit Number (Extracted from GL Number)` text,
  `Sage Transaction Type` text,
  `Sage Description` text,
  `Date` text,
  `General Ledger Number` text,
  `Supplier Information` text,
  `Total Cost` double DEFAULT NULL,
  `Sage Equipment` text,
  `Data Source` text,
  `Import Batch ID` text,
  `Sage Import Staging ID` int DEFAULT NULL,
  `Import Key` text,
  `Part Description` text,
  PRIMARY KEY (`id`),
  KEY `fk_sage_history_sage_import_staging1_idx` (`Sage Import Staging ID`),
  KEY `fk_sage_history_parts1_idx` (`Part ID`),
  CONSTRAINT `fk_sage_history_parts1` FOREIGN KEY (`Part ID`) REFERENCES `parts` (`Part ID`),
  CONSTRAINT `fk_sage_history_sage_import_staging1` FOREIGN KEY (`Sage Import Staging ID`) REFERENCES `sage_import_staging` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sage_import_staging`
--

DROP TABLE IF EXISTS `sage_import_staging`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sage_import_staging` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Status` text,
  `Mapped Description` text,
  `Mapping Status` text,
  `Notes` text,
  `Imported At` text,
  `Raw JSON` text,
  `Name` text,
  `Error Message` text,
  `Source Filename` text,
  `Attachment Summary` text,
  `Import Batch ID` text,
  `Mapped GL` text,
  `Row Number` double DEFAULT NULL,
  `airtable_id` text,
  `Promoted At` text,
  `Mapped Cost` double DEFAULT NULL,
  `Mapped Date` text,
  `Sage History Link` text,
  `Promoted?` tinyint(1) DEFAULT NULL,
  `Import Notes` text,
  `Promote Error` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sage_upload_intake`
--

DROP TABLE IF EXISTS `sage_upload_intake`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sage_upload_intake` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Rows Created` bigint DEFAULT NULL,
  `Source Filename` text,
  `Import Notes` text,
  `Imported At` text,
  `Import Batch ID` text,
  `Main File` text,
  `Parse Status` text,
  `airtable_id` text,
  `Core upload` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `supplier logs`
--

DROP TABLE IF EXISTS `supplier logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplier logs` (
  `Timestamp` text,
  `Log Entry` text,
  `Log Type` text,
  `User` text,
  `Supplier Name` text,
  `airtable_id` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Supplier Name` text,
  `Phone Number` text,
  `Contacts` text,
  `Supplier Specialty` text,
  `Supplier Location` text,
  `Supplier Experience Notes` text,
  `Purchasing Notes` text,
  `Supplier Type` text,
  `Website URL` text,
  `Account, Website, and Login Notes` text,
  `Credit Notes` text,
  `Email` text,
  `Attachments` text,
  `Parts` text,
  `Vendor Rating` text,
  `Contact Notes` text,
  `Account with Vendor` text,
  `Misc. Notes` text,
  `Fax Number` text,
  `Last Purchase Date` text,
  `Vendor Logs` text,
  `Parts 2` text,
  `Parts 3` text,
  `Address 1` text,
  `Address 2` text,
  `City` text,
  `Zip Code` text,
  `Status` text,
  `Purchase Order History` text,
  `Sage History` text,
  `Record ID` text,
  `Update Supplier Requests` text,
  `Office & Cleaning Supplies` text,
  KEY `fk_suppliers_grid_view_parts1` (`id`),
  CONSTRAINT `fk_suppliers_grid_view_parts1` FOREIGN KEY (`id`) REFERENCES `parts` (`Supplier ID`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `suppliers_logs`
--

DROP TABLE IF EXISTS `suppliers_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Timestamp` text,
  `Log Entry` text,
  `Log Type` text,
  `User` text,
  `Supplier Name` text,
  `airtable_id` text,
  `Supplier_ID` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_suppliers_logs_suppliers_grid_view1_idx` (`Supplier_ID`),
  CONSTRAINT `fk_suppliers_logs_suppliers_grid_view1` FOREIGN KEY (`Supplier_ID`) REFERENCES `suppliers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `update equipment requests`
--

DROP TABLE IF EXISTS `update equipment requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `update equipment requests` (
  `New Status` text,
  `Equipment (Link)` text,
  `Applied` tinyint(1) DEFAULT NULL,
  `Record ID (from Equipment)` text,
  `Submitted At` text,
  `Final Status` text,
  `Target Record ID Resolved` text,
  `airtable_id` text,
  `New Year` double DEFAULT NULL,
  `Final Year` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `update part requests`
--

DROP TABLE IF EXISTS `update part requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `update part requests` (
  `Final Part Description` text,
  `Part (Link)` text,
  `Target Record ID Resolved` text,
  `New Part Description` text,
  `Submitted At` text,
  `Record ID (from Part (Link))` text,
  `airtable_id` text,
  `New In-Stock Location` text,
  `Final In-Stock Location` text,
  `Final Status` text,
  `New Status` text,
  `New Supplier Name` text,
  `Final Supplier Name` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `update supplier requests`
--

DROP TABLE IF EXISTS `update supplier requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `update supplier requests` (
  `Supplier (Link)` text,
  `Submitted At` text,
  `Target Record ID Resolved` text,
  `Final Contact Name` text,
  `Applied` tinyint(1) DEFAULT NULL,
  `Record ID (from Supplier)` text,
  `New Contact Name` text,
  `airtable_id` text,
  `Final Supplier Name` text,
  `Final Contact Notes` text,
  `Final Phone` text,
  `New Email` text,
  `New Status` text,
  `New Phone` text,
  `New Misc Notes` text,
  `Final Status` text,
  `Final Supplier Notes` text,
  `Final Email` text,
  `New Contact Notes` text,
  `New Supplier Notes` text,
  `Final Misc Notes` text,
  `New Supplier Name` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `update_equipment_requests`
--

DROP TABLE IF EXISTS `update_equipment_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `update_equipment_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `New Status` text,
  `Equipment (Link)` text,
  `Applied` tinyint(1) DEFAULT NULL,
  `Record ID (from Equipment)` text,
  `Submitted At` text,
  `Final Status` text,
  `Target Record ID Resolved` text,
  `airtable_id` text,
  `New Year` double DEFAULT NULL,
  `Final Year` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `update_part_requests`
--

DROP TABLE IF EXISTS `update_part_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `update_part_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Final Part Description` text,
  `Part (Link)` text,
  `Target Record ID Resolved` text,
  `New Part Description` text,
  `Submitted At` text,
  `Record ID (from Part (Link))` text,
  `airtable_id` text,
  `New In-Stock Location` text,
  `Final In-Stock Location` text,
  `Final Status` text,
  `New Status` text,
  `New Supplier Name` text,
  `Final Supplier Name` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `update_supplier_requests`
--

DROP TABLE IF EXISTS `update_supplier_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `update_supplier_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Supplier (Link)` text,
  `Submitted At` text,
  `Target Record ID Resolved` text,
  `Final Contact Name` text,
  `Applied` tinyint(1) DEFAULT NULL,
  `Record ID (from Supplier)` text,
  `New Contact Name` text,
  `airtable_id` text,
  `Final Supplier Name` text,
  `Final Contact Notes` text,
  `Final Phone` text,
  `New Email` text,
  `New Status` text,
  `New Phone` text,
  `New Misc Notes` text,
  `Final Status` text,
  `Final Supplier Notes` text,
  `Final Email` text,
  `New Contact Notes` text,
  `New Supplier Notes` text,
  `Final Misc Notes` text,
  `New Supplier Name` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-06 14:50:29
