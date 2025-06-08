-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: ausales_db
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_groups`
--

DROP TABLE IF EXISTS `account_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_group_name` varchar(50) NOT NULL,
  `account_under` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `group_ledger_id` bigint NOT NULL,
  `group_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_groups_group_ledger_id_26fee411_fk_group_ledgers_id` (`group_ledger_id`),
  KEY `account_groups_group_type_id_f51b5c2e_fk_group_types_id` (`group_type_id`),
  KEY `account_groups_created_by_id_f8ef6c77_fk_users_id` (`created_by_id`),
  CONSTRAINT `account_groups_created_by_id_f8ef6c77_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `account_groups_group_ledger_id_26fee411_fk_group_ledgers_id` FOREIGN KEY (`group_ledger_id`) REFERENCES `group_ledgers` (`id`),
  CONSTRAINT `account_groups_group_type_id_f51b5c2e_fk_group_types_id` FOREIGN KEY (`group_type_id`) REFERENCES `group_types` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_groups`
--

LOCK TABLES `account_groups` WRITE;
/*!40000 ALTER TABLE `account_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_head`
--

DROP TABLE IF EXISTS `account_head`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_head` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_head_name` varchar(50) NOT NULL,
  `account_head_code` varchar(10) NOT NULL,
  `is_buyer` tinyint(1) NOT NULL,
  `is_diamond_dealer` tinyint(1) NOT NULL,
  `credit_balance_rupee` varchar(10) NOT NULL,
  `credit_balance_gm` varchar(10) NOT NULL,
  `debit_balance_rupee` varchar(10) NOT NULL,
  `debit_balance_gm` varchar(10) NOT NULL,
  `upi_id` varchar(150) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `account_type_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `customer_type_id` bigint NOT NULL,
  `group_name_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_head_account_type_id_54109cf6_fk_account_types_id` (`account_type_id`),
  KEY `account_head_created_by_id_b74f9204_fk_users_id` (`created_by_id`),
  KEY `account_head_customer_type_id_932c1b8b_fk_customer_types_id` (`customer_type_id`),
  KEY `account_head_group_name_id_1fe8962f_fk_account_groups_id` (`group_name_id`),
  CONSTRAINT `account_head_account_type_id_54109cf6_fk_account_types_id` FOREIGN KEY (`account_type_id`) REFERENCES `account_types` (`id`),
  CONSTRAINT `account_head_created_by_id_b74f9204_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `account_head_customer_type_id_932c1b8b_fk_customer_types_id` FOREIGN KEY (`customer_type_id`) REFERENCES `customer_types` (`id`),
  CONSTRAINT `account_head_group_name_id_1fe8962f_fk_account_groups_id` FOREIGN KEY (`group_name_id`) REFERENCES `account_groups` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_head`
--

LOCK TABLES `account_head` WRITE;
/*!40000 ALTER TABLE `account_head` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_head` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_head_address`
--

DROP TABLE IF EXISTS `account_head_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_head_address` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `door_no` varchar(10) NOT NULL,
  `street_name` varchar(100) NOT NULL,
  `area` varchar(50) NOT NULL,
  `taluk` varchar(50) NOT NULL,
  `postal` varchar(50) NOT NULL,
  `district` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  `pin_code` varchar(10) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `account_head_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_head_address_account_head_id_a3815517_fk_account_head_id` (`account_head_id`),
  KEY `account_head_address_created_by_id_d0547ece_fk_users_id` (`created_by_id`),
  CONSTRAINT `account_head_address_account_head_id_a3815517_fk_account_head_id` FOREIGN KEY (`account_head_id`) REFERENCES `account_head` (`id`),
  CONSTRAINT `account_head_address_created_by_id_d0547ece_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_head_address`
--

LOCK TABLES `account_head_address` WRITE;
/*!40000 ALTER TABLE `account_head_address` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_head_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_head_bank`
--

DROP TABLE IF EXISTS `account_head_bank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_head_bank` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `acc_holder_name` varchar(100) DEFAULT NULL,
  `account_no` varchar(100) DEFAULT NULL,
  `ifsc_code` varchar(100) DEFAULT NULL,
  `bank_name` varchar(100) DEFAULT NULL,
  `branch_name` varchar(100) DEFAULT NULL,
  `micr_code` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `account_head_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_head_bank_account_head_id_91f61bfe_fk_account_head_id` (`account_head_id`),
  KEY `account_head_bank_created_by_id_4c45bf95_fk_users_id` (`created_by_id`),
  CONSTRAINT `account_head_bank_account_head_id_91f61bfe_fk_account_head_id` FOREIGN KEY (`account_head_id`) REFERENCES `account_head` (`id`),
  CONSTRAINT `account_head_bank_created_by_id_4c45bf95_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_head_bank`
--

LOCK TABLES `account_head_bank` WRITE;
/*!40000 ALTER TABLE `account_head_bank` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_head_bank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_head_contact`
--

DROP TABLE IF EXISTS `account_head_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_head_contact` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mobile_number` varchar(10) NOT NULL,
  `email_id` varchar(100) NOT NULL,
  `website` varchar(100) NOT NULL,
  `std_code` varchar(10) NOT NULL,
  `landline_number` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `account_head_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_head_contact_account_head_id_a0d8e3ad_fk_account_head_id` (`account_head_id`),
  KEY `account_head_contact_created_by_id_112cd6de_fk_users_id` (`created_by_id`),
  CONSTRAINT `account_head_contact_account_head_id_a0d8e3ad_fk_account_head_id` FOREIGN KEY (`account_head_id`) REFERENCES `account_head` (`id`),
  CONSTRAINT `account_head_contact_created_by_id_112cd6de_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_head_contact`
--

LOCK TABLES `account_head_contact` WRITE;
/*!40000 ALTER TABLE `account_head_contact` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_head_contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_head_gst`
--

DROP TABLE IF EXISTS `account_head_gst`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_head_gst` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pan_no` varchar(50) DEFAULT NULL,
  `tin_no` varchar(50) DEFAULT NULL,
  `gst_no` varchar(100) DEFAULT NULL,
  `registered_name` varchar(100) DEFAULT NULL,
  `gst_status` varchar(50) DEFAULT NULL,
  `tax_payer_type` varchar(50) DEFAULT NULL,
  `bussiness_type` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `account_head_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_head_gst_account_head_id_6ba0b268_fk_account_head_id` (`account_head_id`),
  KEY `account_head_gst_created_by_id_2723fad6_fk_users_id` (`created_by_id`),
  CONSTRAINT `account_head_gst_account_head_id_6ba0b268_fk_account_head_id` FOREIGN KEY (`account_head_id`) REFERENCES `account_head` (`id`),
  CONSTRAINT `account_head_gst_created_by_id_2723fad6_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_head_gst`
--

LOCK TABLES `account_head_gst` WRITE;
/*!40000 ALTER TABLE `account_head_gst` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_head_gst` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_types`
--

DROP TABLE IF EXISTS `account_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_type_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_types`
--

LOCK TABLES `account_types` WRITE;
/*!40000 ALTER TABLE `account_types` DISABLE KEYS */;
INSERT INTO `account_types` VALUES (1,'Personal'),(2,'Nominal'),(3,'Real');
/*!40000 ALTER TABLE `account_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `advance_payment`
--

DROP TABLE IF EXISTS `advance_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `advance_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `advance_id` varchar(50) NOT NULL,
  `advance_amount` double DEFAULT NULL,
  `advance_weight` double DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `redeem_amount` double DEFAULT NULL,
  `redeem_weight` double DEFAULT NULL,
  `is_redeem` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `advance_purpose_id` bigint NOT NULL,
  `branch_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `customer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `advance_id` (`advance_id`),
  KEY `advance_payment_advance_purpose_id_f28cc79d_fk_advance_p` (`advance_purpose_id`),
  KEY `advance_payment_branch_id_0fda8c92_fk_branches_id` (`branch_id`),
  KEY `advance_payment_created_by_id_e4ef5b32_fk_users_id` (`created_by_id`),
  KEY `advance_payment_customer_id_5b696d5c_fk_customer_details_id` (`customer_id`),
  CONSTRAINT `advance_payment_advance_purpose_id_f28cc79d_fk_advance_p` FOREIGN KEY (`advance_purpose_id`) REFERENCES `advance_purpose` (`id`),
  CONSTRAINT `advance_payment_branch_id_0fda8c92_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `advance_payment_created_by_id_e4ef5b32_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `advance_payment_customer_id_5b696d5c_fk_customer_details_id` FOREIGN KEY (`customer_id`) REFERENCES `customer_details` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advance_payment`
--

LOCK TABLES `advance_payment` WRITE;
/*!40000 ALTER TABLE `advance_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `advance_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `advance_purpose`
--

DROP TABLE IF EXISTS `advance_purpose`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `advance_purpose` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `purpose_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `advance_purpose_created_by_id_a602f6f3_fk_users_id` (`created_by_id`),
  CONSTRAINT `advance_purpose_created_by_id_a602f6f3_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advance_purpose`
--

LOCK TABLES `advance_purpose` WRITE;
/*!40000 ALTER TABLE `advance_purpose` DISABLE KEYS */;
INSERT INTO `advance_purpose` VALUES (1,'Order',1,NULL,NULL,NULL,1),(2,'Repair',1,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `advance_purpose` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `approval_issue`
--

DROP TABLE IF EXISTS `approval_issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approval_issue` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `approval_issue_id` varchar(50) NOT NULL,
  `issue_date` date NOT NULL,
  `issued_by` varchar(150) NOT NULL,
  `receiver_name` varchar(150) NOT NULL,
  `notes` longtext,
  `issued_gross_weight` double NOT NULL,
  `issued_net_weight` double NOT NULL,
  `recieved_date` date DEFAULT NULL,
  `received_by` varchar(150) DEFAULT NULL,
  `received_gross_weight` double NOT NULL,
  `received_net_weight` double NOT NULL,
  `sold_gross_weight` double NOT NULL,
  `sold_net_weight` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `bill_type_id` bigint NOT NULL,
  `branch_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `estimation_details_id` bigint DEFAULT NULL,
  `shop_name_id` bigint NOT NULL,
  `status_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `approval_issue_id` (`approval_issue_id`),
  KEY `approval_issue_bill_type_id_5f6a84a7_fk_bill_type_id` (`bill_type_id`),
  KEY `approval_issue_branch_id_f0a633e2_fk_branches_id` (`branch_id`),
  KEY `approval_issue_created_by_id_c1df13a4_fk_users_id` (`created_by_id`),
  KEY `approval_issue_estimation_details_i_b5f26570_fk_estimatio` (`estimation_details_id`),
  KEY `approval_issue_shop_name_id_2e6fbcff_fk_customer_details_id` (`shop_name_id`),
  KEY `approval_issue_status_id_2f539023_fk_status_table_id` (`status_id`),
  CONSTRAINT `approval_issue_bill_type_id_5f6a84a7_fk_bill_type_id` FOREIGN KEY (`bill_type_id`) REFERENCES `bill_type` (`id`),
  CONSTRAINT `approval_issue_branch_id_f0a633e2_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `approval_issue_created_by_id_c1df13a4_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `approval_issue_estimation_details_i_b5f26570_fk_estimatio` FOREIGN KEY (`estimation_details_id`) REFERENCES `estimation_detail` (`id`),
  CONSTRAINT `approval_issue_shop_name_id_2e6fbcff_fk_customer_details_id` FOREIGN KEY (`shop_name_id`) REFERENCES `customer_details` (`id`),
  CONSTRAINT `approval_issue_status_id_2f539023_fk_status_table_id` FOREIGN KEY (`status_id`) REFERENCES `status_table` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `approval_issue`
--

LOCK TABLES `approval_issue` WRITE;
/*!40000 ALTER TABLE `approval_issue` DISABLE KEYS */;
/*!40000 ALTER TABLE `approval_issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `approval_issue_id`
--

DROP TABLE IF EXISTS `approval_issue_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approval_issue_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `approval_issue_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `approval_issue_id` (`approval_issue_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `approval_issue_id`
--

LOCK TABLES `approval_issue_id` WRITE;
/*!40000 ALTER TABLE `approval_issue_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `approval_issue_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `approval_issue_number`
--

DROP TABLE IF EXISTS `approval_issue_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approval_issue_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `approval_issue_number` varchar(50) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `approval_issue_number` (`approval_issue_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `approval_issue_number_user_id_a273b15b_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `approval_issue_number`
--

LOCK TABLES `approval_issue_number` WRITE;
/*!40000 ALTER TABLE `approval_issue_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `approval_issue_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `approval_issue_tag_item`
--

DROP TABLE IF EXISTS `approval_issue_tag_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approval_issue_tag_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_received` tinyint(1) NOT NULL,
  `is_sold` tinyint(1) NOT NULL,
  `approval_issue_details_id` bigint NOT NULL,
  `tag_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `approval_issue_tag_i_approval_issue_detai_17d4fccf_fk_approval_` (`approval_issue_details_id`),
  KEY `approval_issue_tag_i_tag_details_id_3a9bc185_fk_tagged_it` (`tag_details_id`),
  CONSTRAINT `approval_issue_tag_i_approval_issue_detai_17d4fccf_fk_approval_` FOREIGN KEY (`approval_issue_details_id`) REFERENCES `approval_issue` (`id`),
  CONSTRAINT `approval_issue_tag_i_tag_details_id_3a9bc185_fk_tagged_it` FOREIGN KEY (`tag_details_id`) REFERENCES `tagged_item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `approval_issue_tag_item`
--

LOCK TABLES `approval_issue_tag_item` WRITE;
/*!40000 ALTER TABLE `approval_issue_tag_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `approval_issue_tag_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `approval_rules`
--

DROP TABLE IF EXISTS `approval_rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approval_rules` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `approval_type_id` bigint NOT NULL,
  `approved_by_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `modified_by_id` bigint NOT NULL,
  `user_role_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `approval_rules_approval_type_id_e18e9bac_fk_approval_types_id` (`approval_type_id`),
  KEY `approval_rules_approved_by_id_7feaa687_fk_users_id` (`approved_by_id`),
  KEY `approval_rules_created_by_id_1043c083_fk_users_id` (`created_by_id`),
  KEY `approval_rules_modified_by_id_a0ac5c23_fk_users_id` (`modified_by_id`),
  KEY `approval_rules_user_role_id_90bc7b7c_fk_user_roles_id` (`user_role_id`),
  CONSTRAINT `approval_rules_approval_type_id_e18e9bac_fk_approval_types_id` FOREIGN KEY (`approval_type_id`) REFERENCES `approval_types` (`id`),
  CONSTRAINT `approval_rules_approved_by_id_7feaa687_fk_users_id` FOREIGN KEY (`approved_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `approval_rules_created_by_id_1043c083_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `approval_rules_modified_by_id_a0ac5c23_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `approval_rules_user_role_id_90bc7b7c_fk_user_roles_id` FOREIGN KEY (`user_role_id`) REFERENCES `user_roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `approval_rules`
--

LOCK TABLES `approval_rules` WRITE;
/*!40000 ALTER TABLE `approval_rules` DISABLE KEYS */;
/*!40000 ALTER TABLE `approval_rules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `approval_types`
--

DROP TABLE IF EXISTS `approval_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approval_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `approval_type` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `modified_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `approval_type` (`approval_type`),
  KEY `approval_types_created_by_id_f602ad66_fk_users_id` (`created_by_id`),
  KEY `approval_types_modified_by_id_2f9fe87f_fk_users_id` (`modified_by_id`),
  CONSTRAINT `approval_types_created_by_id_f602ad66_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `approval_types_modified_by_id_2f9fe87f_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `approval_types`
--

LOCK TABLES `approval_types` WRITE;
/*!40000 ALTER TABLE `approval_types` DISABLE KEYS */;
INSERT INTO `approval_types` VALUES (1,'Estimation Approval',1,NULL,NULL,1,1);
/*!40000 ALTER TABLE `approval_types` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=825 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Token',6,'add_token'),(22,'Can change Token',6,'change_token'),(23,'Can delete Token',6,'delete_token'),(24,'Can view Token',6,'view_token'),(25,'Can add token',7,'add_tokenproxy'),(26,'Can change token',7,'change_tokenproxy'),(27,'Can delete token',7,'delete_tokenproxy'),(28,'Can view token',7,'view_tokenproxy'),(29,'Can add main_menu_group',8,'add_mainmenugroup'),(30,'Can change main_menu_group',8,'change_mainmenugroup'),(31,'Can delete main_menu_group',8,'delete_mainmenugroup'),(32,'Can view main_menu_group',8,'view_mainmenugroup'),(33,'Can add menu',9,'add_menu'),(34,'Can change menu',9,'change_menu'),(35,'Can delete menu',9,'delete_menu'),(36,'Can view menu',9,'view_menu'),(37,'Can add payment_mode',10,'add_paymentmode'),(38,'Can change payment_mode',10,'change_paymentmode'),(39,'Can delete payment_mode',10,'delete_paymentmode'),(40,'Can view payment_mode',10,'view_paymentmode'),(41,'Can add payment_status',11,'add_paymentstatus'),(42,'Can change payment_status',11,'change_paymentstatus'),(43,'Can delete payment_status',11,'delete_paymentstatus'),(44,'Can view payment_status',11,'view_paymentstatus'),(45,'Can add status_table',12,'add_statustable'),(46,'Can change status_table',12,'change_statustable'),(47,'Can delete status_table',12,'delete_statustable'),(48,'Can view status_table',12,'view_statustable'),(49,'Can add sale_return_policy',13,'add_salereturnpolicy'),(50,'Can change sale_return_policy',13,'change_salereturnpolicy'),(51,'Can delete sale_return_policy',13,'delete_salereturnpolicy'),(52,'Can view sale_return_policy',13,'view_salereturnpolicy'),(53,'Can add print_module',14,'add_printmodule'),(54,'Can change print_module',14,'change_printmodule'),(55,'Can delete print_module',14,'delete_printmodule'),(56,'Can view print_module',14,'view_printmodule'),(57,'Can add menu_permission',15,'add_menupermission'),(58,'Can change menu_permission',15,'change_menupermission'),(59,'Can delete menu_permission',15,'delete_menupermission'),(60,'Can view menu_permission',15,'view_menupermission'),(61,'Can add menu_group',16,'add_menugroup'),(62,'Can change menu_group',16,'change_menugroup'),(63,'Can delete menu_group',16,'delete_menugroup'),(64,'Can view menu_group',16,'view_menugroup'),(65,'Can add incentive_types',17,'add_incentivetype'),(66,'Can change incentive_types',17,'change_incentivetype'),(67,'Can delete incentive_types',17,'delete_incentivetype'),(68,'Can view incentive_types',17,'view_incentivetype'),(69,'Can add incentive_percents',18,'add_incentivepercent'),(70,'Can change incentive_percents',18,'change_incentivepercent'),(71,'Can delete incentive_percents',18,'delete_incentivepercent'),(72,'Can view incentive_percents',18,'view_incentivepercent'),(73,'Can add settings_gender',19,'add_gender'),(74,'Can change settings_gender',19,'change_gender'),(75,'Can delete settings_gender',19,'delete_gender'),(76,'Can view settings_gender',19,'view_gender'),(77,'Can add location',20,'add_location'),(78,'Can change location',20,'change_location'),(79,'Can delete location',20,'delete_location'),(80,'Can view location',20,'view_location'),(81,'Can add user_role',21,'add_userrole'),(82,'Can change user_role',21,'change_userrole'),(83,'Can delete user_role',21,'delete_userrole'),(84,'Can view user_role',21,'view_userrole'),(85,'Can add branch',22,'add_branch'),(86,'Can change branch',22,'change_branch'),(87,'Can delete branch',22,'delete_branch'),(88,'Can view branch',22,'view_branch'),(89,'Can add user',23,'add_user'),(90,'Can change user',23,'change_user'),(91,'Can delete user',23,'delete_user'),(92,'Can view user',23,'view_user'),(93,'Can add department',24,'add_department'),(94,'Can change department',24,'change_department'),(95,'Can delete department',24,'delete_department'),(96,'Can view department',24,'view_department'),(97,'Can add designation',25,'add_designation'),(98,'Can change designation',25,'change_designation'),(99,'Can delete designation',25,'delete_designation'),(100,'Can view designation',25,'view_designation'),(101,'Can add staff',26,'add_staff'),(102,'Can change staff',26,'change_staff'),(103,'Can delete staff',26,'delete_staff'),(104,'Can view staff',26,'view_staff'),(105,'Can add counter',27,'add_counter'),(106,'Can change counter',27,'change_counter'),(107,'Can delete counter',27,'delete_counter'),(108,'Can view counter',27,'view_counter'),(109,'Can add floor',28,'add_floor'),(110,'Can change floor',28,'change_floor'),(111,'Can delete floor',28,'delete_floor'),(112,'Can view floor',28,'view_floor'),(113,'Can add counter_target',29,'add_countertarget'),(114,'Can change counter_target',29,'change_countertarget'),(115,'Can delete counter_target',29,'delete_countertarget'),(116,'Can view counter_target',29,'view_countertarget'),(117,'Can add metal',30,'add_metal'),(118,'Can change metal',30,'change_metal'),(119,'Can delete metal',30,'delete_metal'),(120,'Can view metal',30,'view_metal'),(121,'Can add tax_detail',31,'add_taxdetails'),(122,'Can change tax_detail',31,'change_taxdetails'),(123,'Can delete tax_detail',31,'delete_taxdetails'),(124,'Can view tax_detail',31,'view_taxdetails'),(125,'Can add voucher_type',32,'add_vouchertype'),(126,'Can change voucher_type',32,'change_vouchertype'),(127,'Can delete voucher_type',32,'delete_vouchertype'),(128,'Can view voucher_type',32,'view_vouchertype'),(129,'Can add tax_details_audit',33,'add_taxdetailsaudit'),(130,'Can change tax_details_audit',33,'change_taxdetailsaudit'),(131,'Can delete tax_details_audit',33,'delete_taxdetailsaudit'),(132,'Can view tax_details_audit',33,'view_taxdetailsaudit'),(133,'Can add tag_type',34,'add_tagtypes'),(134,'Can change tag_type',34,'change_tagtypes'),(135,'Can delete tag_type',34,'delete_tagtypes'),(136,'Can view tag_type',34,'view_tagtypes'),(137,'Can add stone_detail',35,'add_stonedetails'),(138,'Can change stone_detail',35,'change_stonedetails'),(139,'Can delete stone_detail',35,'delete_stonedetails'),(140,'Can view stone_detail',35,'view_stonedetails'),(141,'Can add shape_detail',36,'add_shapedetails'),(142,'Can change shape_detail',36,'change_shapedetails'),(143,'Can delete shape_detail',36,'delete_shapedetails'),(144,'Can view shape_detail',36,'view_shapedetails'),(145,'Can add sales_tax_detail',37,'add_salestaxdetails'),(146,'Can change sales_tax_detail',37,'change_salestaxdetails'),(147,'Can delete sales_tax_detail',37,'delete_salestaxdetails'),(148,'Can view sales_tax_detail',37,'view_salestaxdetails'),(149,'Can add repair_type',38,'add_repairtype'),(150,'Can change repair_type',38,'change_repairtype'),(151,'Can delete repair_type',38,'delete_repairtype'),(152,'Can view repair_type',38,'view_repairtype'),(153,'Can add purity',39,'add_purity'),(154,'Can change purity',39,'change_purity'),(155,'Can delete purity',39,'delete_purity'),(156,'Can view purity',39,'view_purity'),(157,'Can add purchase_tax_detail',40,'add_purchasetaxdetails'),(158,'Can change purchase_tax_detail',40,'change_purchasetaxdetails'),(159,'Can delete purchase_tax_detail',40,'delete_purchasetaxdetails'),(160,'Can view purchase_tax_detail',40,'view_purchasetaxdetails'),(161,'Can add metal_rate',41,'add_metalrate'),(162,'Can change metal_rate',41,'change_metalrate'),(163,'Can delete metal_rate',41,'delete_metalrate'),(164,'Can view metal_rate',41,'view_metalrate'),(165,'Can add metal_old_rate',42,'add_metaloldrate'),(166,'Can change metal_old_rate',42,'change_metaloldrate'),(167,'Can delete metal_old_rate',42,'delete_metaloldrate'),(168,'Can view metal_old_rate',42,'view_metaloldrate'),(169,'Can add gst_type',43,'add_gsttype'),(170,'Can change gst_type',43,'change_gsttype'),(171,'Can delete gst_type',43,'delete_gsttype'),(172,'Can view gst_type',43,'view_gsttype'),(173,'Can add gift_voucher',44,'add_giftvoucher'),(174,'Can change gift_voucher',44,'change_giftvoucher'),(175,'Can delete gift_voucher',44,'delete_giftvoucher'),(176,'Can view gift_voucher',44,'view_giftvoucher'),(177,'Can add cut_detail',45,'add_cutdetails'),(178,'Can change cut_detail',45,'change_cutdetails'),(179,'Can delete cut_detail',45,'delete_cutdetails'),(180,'Can view cut_detail',45,'view_cutdetails'),(181,'Can add color_detail',46,'add_colordetails'),(182,'Can change color_detail',46,'change_colordetails'),(183,'Can delete color_detail',46,'delete_colordetails'),(184,'Can view color_detail',46,'view_colordetails'),(185,'Can add clarity_detail',47,'add_claritydetails'),(186,'Can change clarity_detail',47,'change_claritydetails'),(187,'Can delete clarity_detail',47,'delete_claritydetails'),(188,'Can view clarity_detail',47,'view_claritydetails'),(189,'Can add centgroup_detail',48,'add_centgroup'),(190,'Can change centgroup_detail',48,'change_centgroup'),(191,'Can delete centgroup_detail',48,'delete_centgroup'),(192,'Can view centgroup_detail',48,'view_centgroup'),(193,'Can add card_type',49,'add_cardtype'),(194,'Can change card_type',49,'change_cardtype'),(195,'Can delete card_type',49,'delete_cardtype'),(196,'Can view card_type',49,'view_cardtype'),(197,'Can add carat_rate_detail',50,'add_caratrate'),(198,'Can change carat_rate_detail',50,'change_caratrate'),(199,'Can delete carat_rate_detail',50,'delete_caratrate'),(200,'Can view carat_rate_detail',50,'view_caratrate'),(201,'Can add account_group',51,'add_accountgroup'),(202,'Can change account_group',51,'change_accountgroup'),(203,'Can delete account_group',51,'delete_accountgroup'),(204,'Can view account_group',51,'view_accountgroup'),(205,'Can add account_head',52,'add_accountheaddetails'),(206,'Can change account_head',52,'change_accountheaddetails'),(207,'Can delete account_head',52,'delete_accountheaddetails'),(208,'Can view account_head',52,'view_accountheaddetails'),(209,'Can add account_type',53,'add_accounttype'),(210,'Can change account_type',53,'change_accounttype'),(211,'Can delete account_type',53,'delete_accounttype'),(212,'Can view account_type',53,'view_accounttype'),(213,'Can add company_detail',54,'add_companydetails'),(214,'Can change company_detail',54,'change_companydetails'),(215,'Can delete company_detail',54,'delete_companydetails'),(216,'Can view company_detail',54,'view_companydetails'),(217,'Can add customer_type',55,'add_customertype'),(218,'Can change customer_type',55,'change_customertype'),(219,'Can delete customer_type',55,'delete_customertype'),(220,'Can view customer_type',55,'view_customertype'),(221,'Can add group_ledger',56,'add_groupledger'),(222,'Can change group_ledger',56,'change_groupledger'),(223,'Can delete group_ledger',56,'delete_groupledger'),(224,'Can view group_ledger',56,'view_groupledger'),(225,'Can add group_type',57,'add_grouptype'),(226,'Can change group_type',57,'change_grouptype'),(227,'Can delete group_type',57,'delete_grouptype'),(228,'Can view group_type',57,'view_grouptype'),(229,'Can add company_gst_detail',58,'add_companygstdetails'),(230,'Can change company_gst_detail',58,'change_companygstdetails'),(231,'Can delete company_gst_detail',58,'delete_companygstdetails'),(232,'Can view company_gst_detail',58,'view_companygstdetails'),(233,'Can add company_bank_detail',59,'add_companybankdetails'),(234,'Can change company_bank_detail',59,'change_companybankdetails'),(235,'Can delete company_bank_detail',59,'delete_companybankdetails'),(236,'Can view company_bank_detail',59,'view_companybankdetails'),(237,'Can add company_address_detail',60,'add_companyaddressdetails'),(238,'Can change company_address_detail',60,'change_companyaddressdetails'),(239,'Can delete company_address_detail',60,'delete_companyaddressdetails'),(240,'Can view company_address_detail',60,'view_companyaddressdetails'),(241,'Can add account_head_gst',61,'add_accountheadgstdetails'),(242,'Can change account_head_gst',61,'change_accountheadgstdetails'),(243,'Can delete account_head_gst',61,'delete_accountheadgstdetails'),(244,'Can view account_head_gst',61,'view_accountheadgstdetails'),(245,'Can add account_head_contact',62,'add_accountheadcontact'),(246,'Can change account_head_contact',62,'change_accountheadcontact'),(247,'Can delete account_head_contact',62,'delete_accountheadcontact'),(248,'Can view account_head_contact',62,'view_accountheadcontact'),(249,'Can add account_head_bank',63,'add_accountheadbankdetails'),(250,'Can change account_head_bank',63,'change_accountheadbankdetails'),(251,'Can delete account_head_bank',63,'delete_accountheadbankdetails'),(252,'Can view account_head_bank',63,'view_accountheadbankdetails'),(253,'Can add account_head_address',64,'add_accountheadaddress'),(254,'Can change account_head_address',64,'change_accountheadaddress'),(255,'Can delete account_head_address',64,'delete_accountheadaddress'),(256,'Can view account_head_address',64,'view_accountheadaddress'),(257,'Can add calculation_type',65,'add_calculationtype'),(258,'Can change calculation_type',65,'change_calculationtype'),(259,'Can delete calculation_type',65,'delete_calculationtype'),(260,'Can view calculation_type',65,'view_calculationtype'),(261,'Can add item_detail',66,'add_item'),(262,'Can change item_detail',66,'change_item'),(263,'Can delete item_detail',66,'delete_item'),(264,'Can view item_detail',66,'view_item'),(265,'Can add item_id',67,'add_itemid'),(266,'Can change item_id',67,'change_itemid'),(267,'Can delete item_id',67,'delete_itemid'),(268,'Can view item_id',67,'view_itemid'),(269,'Can add measurement_type',68,'add_measurementtype'),(270,'Can change measurement_type',68,'change_measurementtype'),(271,'Can delete measurement_type',68,'delete_measurementtype'),(272,'Can view measurement_type',68,'view_measurementtype'),(273,'Can add stock_type',69,'add_stocktype'),(274,'Can change stock_type',69,'change_stocktype'),(275,'Can delete stock_type',69,'delete_stocktype'),(276,'Can view stock_type',69,'view_stocktype'),(277,'Can add sub_item_detail',70,'add_subitem'),(278,'Can change sub_item_detail',70,'change_subitem'),(279,'Can delete sub_item_detail',70,'delete_subitem'),(280,'Can view sub_item_detail',70,'view_subitem'),(281,'Can add sub_item_id',71,'add_subitemid'),(282,'Can change sub_item_id',71,'change_subitemid'),(283,'Can delete sub_item_id',71,'delete_subitemid'),(284,'Can view sub_item_id',71,'view_subitemid'),(285,'Can add weight_type',72,'add_weighttype'),(286,'Can change weight_type',72,'change_weighttype'),(287,'Can delete weight_type',72,'delete_weighttype'),(288,'Can view weight_type',72,'view_weighttype'),(289,'Can add weight_calculation',73,'add_weightcalculation'),(290,'Can change weight_calculation',73,'change_weightcalculation'),(291,'Can delete weight_calculation',73,'delete_weightcalculation'),(292,'Can view weight_calculation',73,'view_weightcalculation'),(293,'Can add subitem_weight_calculation',74,'add_subitemweightcalculation'),(294,'Can change subitem_weight_calculation',74,'change_subitemweightcalculation'),(295,'Can delete subitem_weight_calculation',74,'delete_subitemweightcalculation'),(296,'Can view subitem_weight_calculation',74,'view_subitemweightcalculation'),(297,'Can add sub_per_gram_rate',75,'add_subitempergramrate'),(298,'Can change sub_per_gram_rate',75,'change_subitempergramrate'),(299,'Can delete sub_per_gram_rate',75,'delete_subitempergramrate'),(300,'Can view sub_per_gram_rate',75,'view_subitempergramrate'),(301,'Can add subitem_fixed_rate',76,'add_subitemfixedrate'),(302,'Can change subitem_fixed_rate',76,'change_subitemfixedrate'),(303,'Can delete subitem_fixed_rate',76,'delete_subitemfixedrate'),(304,'Can view subitem_fixed_rate',76,'view_subitemfixedrate'),(305,'Can add range_stock',77,'add_rangestock'),(306,'Can change range_stock',77,'change_rangestock'),(307,'Can delete range_stock',77,'delete_rangestock'),(308,'Can view range_stock',77,'view_rangestock'),(309,'Can add per_gram_rate',78,'add_pergramrate'),(310,'Can change per_gram_rate',78,'change_pergramrate'),(311,'Can delete per_gram_rate',78,'delete_pergramrate'),(312,'Can view per_gram_rate',78,'view_pergramrate'),(313,'Can add measurement_detail',79,'add_measurement'),(314,'Can change measurement_detail',79,'change_measurement'),(315,'Can delete measurement_detail',79,'delete_measurement'),(316,'Can view measurement_detail',79,'view_measurement'),(317,'Can add fixed_rate',80,'add_fixedrate'),(318,'Can change fixed_rate',80,'change_fixedrate'),(319,'Can delete fixed_rate',80,'delete_fixedrate'),(320,'Can view fixed_rate',80,'view_fixedrate'),(321,'Can add entry_type',81,'add_entrytype'),(322,'Can change entry_type',81,'change_entrytype'),(323,'Can delete entry_type',81,'delete_entrytype'),(324,'Can view entry_type',81,'view_entrytype'),(325,'Can add lot',82,'add_lot'),(326,'Can change lot',82,'change_lot'),(327,'Can delete lot',82,'delete_lot'),(328,'Can view lot',82,'view_lot'),(329,'Can add lot_id',83,'add_lotid'),(330,'Can change lot_id',83,'change_lotid'),(331,'Can delete lot_id',83,'delete_lotid'),(332,'Can view lot_id',83,'view_lotid'),(333,'Can add lot_item',84,'add_lotitem'),(334,'Can change lot_item',84,'change_lotitem'),(335,'Can delete lot_item',84,'delete_lotitem'),(336,'Can view lot_item',84,'view_lotitem'),(337,'Can add lot_item_diamond',85,'add_lotitemdiamond'),(338,'Can change lot_item_diamond',85,'change_lotitemdiamond'),(339,'Can delete lot_item_diamond',85,'delete_lotitemdiamond'),(340,'Can view lot_item_diamond',85,'view_lotitemdiamond'),(341,'Can add lot_item_stone',86,'add_lotitemstone'),(342,'Can change lot_item_stone',86,'change_lotitemstone'),(343,'Can delete lot_item_stone',86,'delete_lotitemstone'),(344,'Can view lot_item_stone',86,'view_lotitemstone'),(345,'Can add rate_type',87,'add_ratetype'),(346,'Can change rate_type',87,'change_ratetype'),(347,'Can delete rate_type',87,'delete_ratetype'),(348,'Can view rate_type',87,'view_ratetype'),(349,'Can add stone_weight_type',88,'add_stoneweighttype'),(350,'Can change stone_weight_type',88,'change_stoneweighttype'),(351,'Can delete stone_weight_type',88,'delete_stoneweighttype'),(352,'Can view stone_weight_type',88,'view_stoneweighttype'),(353,'Can add tag_entry',89,'add_tagentry'),(354,'Can change tag_entry',89,'change_tagentry'),(355,'Can delete tag_entry',89,'delete_tagentry'),(356,'Can view tag_entry',89,'view_tagentry'),(357,'Can add tagged_item',90,'add_taggeditems'),(358,'Can change tagged_item',90,'change_taggeditems'),(359,'Can delete tagged_item',90,'delete_taggeditems'),(360,'Can view tagged_item',90,'view_taggeditems'),(361,'Can add tag_number',91,'add_tagnumber'),(362,'Can change tag_number',91,'change_tagnumber'),(363,'Can delete tag_number',91,'delete_tagnumber'),(364,'Can view tag_number',91,'view_tagnumber'),(365,'Can add tagged_item_stone',92,'add_taggeditemstone'),(366,'Can change tagged_item_stone',92,'change_taggeditemstone'),(367,'Can delete tagged_item_stone',92,'delete_taggeditemstone'),(368,'Can view tagged_item_stone',92,'view_taggeditemstone'),(369,'Can add tagged_item_diamond',93,'add_taggeditemdiamond'),(370,'Can change tagged_item_diamond',93,'change_taggeditemdiamond'),(371,'Can delete tagged_item_diamond',93,'delete_taggeditemdiamond'),(372,'Can view tagged_item_diamond',93,'view_taggeditemdiamond'),(373,'Can add duplicate_tag',94,'add_duplicatetag'),(374,'Can change duplicate_tag',94,'change_duplicatetag'),(375,'Can delete duplicate_tag',94,'delete_duplicatetag'),(376,'Can view duplicate_tag',94,'view_duplicatetag'),(377,'Can add bill_id',95,'add_billid'),(378,'Can change bill_id',95,'change_billid'),(379,'Can delete bill_id',95,'delete_billid'),(380,'Can view bill_id',95,'view_billid'),(381,'Can add billing_detail',96,'add_billingdetails'),(382,'Can change billing_detail',96,'change_billingdetails'),(383,'Can delete billing_detail',96,'delete_billingdetails'),(384,'Can view billing_detail',96,'view_billingdetails'),(385,'Can add billing_tag_value',97,'add_billingtagitems'),(386,'Can change billing_tag_value',97,'change_billingtagitems'),(387,'Can delete billing_tag_value',97,'delete_billingtagitems'),(388,'Can view billing_tag_value',97,'view_billingtagitems'),(389,'Can add bill_type',98,'add_billingtype'),(390,'Can change bill_type',98,'change_billingtype'),(391,'Can delete bill_type',98,'delete_billingtype'),(392,'Can view bill_type',98,'view_billingtype'),(393,'Can add estimation_detail',99,'add_estimatedetails'),(394,'Can change estimation_detail',99,'change_estimatedetails'),(395,'Can delete estimation_detail',99,'delete_estimatedetails'),(396,'Can view estimation_detail',99,'view_estimatedetails'),(397,'Can add gold_estimation_id',100,'add_goldestimationid'),(398,'Can change gold_estimation_id',100,'change_goldestimationid'),(399,'Can delete gold_estimation_id',100,'delete_goldestimationid'),(400,'Can view gold_estimation_id',100,'view_goldestimationid'),(401,'Can add billing_misc_issue_detail',101,'add_miscissuedetails'),(402,'Can change billing_misc_issue_detail',101,'change_miscissuedetails'),(403,'Can delete billing_misc_issue_detail',101,'delete_miscissuedetails'),(404,'Can view billing_misc_issue_detail',101,'view_miscissuedetails'),(405,'Can add billing_misc_issue_id',102,'add_miscissueid'),(406,'Can change billing_misc_issue_id',102,'change_miscissueid'),(407,'Can delete billing_misc_issue_id',102,'delete_miscissueid'),(408,'Can view billing_misc_issue_id',102,'view_miscissueid'),(409,'Can add silver_bill_id',103,'add_silverbillid'),(410,'Can change silver_bill_id',103,'change_silverbillid'),(411,'Can delete silver_bill_id',103,'delete_silverbillid'),(412,'Can view silver_bill_id',103,'view_silverbillid'),(413,'Can add silver_estimation_id',104,'add_silverestimationid'),(414,'Can change silver_estimation_id',104,'change_silverestimationid'),(415,'Can delete silver_estimation_id',104,'delete_silverestimationid'),(416,'Can view silver_estimation_id',104,'view_silverestimationid'),(417,'Can add silver_estimation_number',105,'add_silverestimationnumber'),(418,'Can change silver_estimation_number',105,'change_silverestimationnumber'),(419,'Can delete silver_estimation_number',105,'delete_silverestimationnumber'),(420,'Can view silver_estimation_number',105,'view_silverestimationnumber'),(421,'Can add silver_bill_number',106,'add_silverbillnumber'),(422,'Can change silver_bill_number',106,'change_silverbillnumber'),(423,'Can delete silver_bill_number',106,'delete_silverbillnumber'),(424,'Can view silver_bill_number',106,'view_silverbillnumber'),(425,'Can add billing_session_misc_issue_id',107,'add_sessionmiscissueid'),(426,'Can change billing_session_misc_issue_id',107,'change_sessionmiscissueid'),(427,'Can delete billing_session_misc_issue_id',107,'delete_sessionmiscissueid'),(428,'Can view billing_session_misc_issue_id',107,'view_sessionmiscissueid'),(429,'Can add billing_misc_particular',108,'add_miscparticulars'),(430,'Can change billing_misc_particular',108,'change_miscparticulars'),(431,'Can delete billing_misc_particular',108,'delete_miscparticulars'),(432,'Can view billing_misc_particular',108,'view_miscparticulars'),(433,'Can add gold_estimation_number',109,'add_goldestimationnumber'),(434,'Can change gold_estimation_number',109,'change_goldestimationnumber'),(435,'Can delete gold_estimation_number',109,'delete_goldestimationnumber'),(436,'Can view gold_estimation_number',109,'view_goldestimationnumber'),(437,'Can add estimation_tag_value',110,'add_estimationtagitems'),(438,'Can change estimation_tag_value',110,'change_estimationtagitems'),(439,'Can delete estimation_tag_value',110,'delete_estimationtagitems'),(440,'Can view estimation_tag_value',110,'view_estimationtagitems'),(441,'Can add estimation_item_stone',111,'add_estimationstonedetails'),(442,'Can change estimation_item_stone',111,'change_estimationstonedetails'),(443,'Can delete estimation_item_stone',111,'delete_estimationstonedetails'),(444,'Can view estimation_item_stone',111,'view_estimationstonedetails'),(445,'Can add estimation_sale_return',112,'add_estimationsalereturnitems'),(446,'Can change estimation_sale_return',112,'change_estimationsalereturnitems'),(447,'Can delete estimation_sale_return',112,'delete_estimationsalereturnitems'),(448,'Can view estimation_sale_return',112,'view_estimationsalereturnitems'),(449,'Can add estimation_return_stone',113,'add_estimationreturnstonedetails'),(450,'Can change estimation_return_stone',113,'change_estimationreturnstonedetails'),(451,'Can delete estimation_return_stone',113,'delete_estimationreturnstonedetails'),(452,'Can view estimation_return_stone',113,'view_estimationreturnstonedetails'),(453,'Can add estimation_return_diamond',114,'add_estimationreturndiamonddetails'),(454,'Can change estimation_return_diamond',114,'change_estimationreturndiamonddetails'),(455,'Can delete estimation_return_diamond',114,'delete_estimationreturndiamonddetails'),(456,'Can view estimation_return_diamond',114,'view_estimationreturndiamonddetails'),(457,'Can add estimation_old_gold_value',115,'add_estimationoldgold'),(458,'Can change estimation_old_gold_value',115,'change_estimationoldgold'),(459,'Can delete estimation_old_gold_value',115,'delete_estimationoldgold'),(460,'Can view estimation_old_gold_value',115,'view_estimationoldgold'),(461,'Can add estimation_item_diamond',116,'add_estimationdiamonddetails'),(462,'Can change estimation_item_diamond',116,'change_estimationdiamonddetails'),(463,'Can delete estimation_item_diamond',116,'delete_estimationdiamonddetails'),(464,'Can view estimation_item_diamond',116,'view_estimationdiamonddetails'),(465,'Can add estimation_approval',117,'add_estimationapproval'),(466,'Can change estimation_approval',117,'change_estimationapproval'),(467,'Can delete estimation_approval',117,'delete_estimationapproval'),(468,'Can view estimation_approval',117,'view_estimationapproval'),(469,'Can add bill_number',118,'add_billnumber'),(470,'Can change bill_number',118,'change_billnumber'),(471,'Can delete bill_number',118,'delete_billnumber'),(472,'Can view bill_number',118,'view_billnumber'),(473,'Can add billing_item_stone',119,'add_billingstonedetails'),(474,'Can change billing_item_stone',119,'change_billingstonedetails'),(475,'Can delete billing_item_stone',119,'delete_billingstonedetails'),(476,'Can view billing_item_stone',119,'view_billingstonedetails'),(477,'Can add billing_sale_return',120,'add_billingsalereturnitems'),(478,'Can change billing_sale_return',120,'change_billingsalereturnitems'),(479,'Can delete billing_sale_return',120,'delete_billingsalereturnitems'),(480,'Can view billing_sale_return',120,'view_billingsalereturnitems'),(481,'Can add billing_return_stone',121,'add_billingreturnstonedetails'),(482,'Can change billing_return_stone',121,'change_billingreturnstonedetails'),(483,'Can delete billing_return_stone',121,'delete_billingreturnstonedetails'),(484,'Can view billing_return_stone',121,'view_billingreturnstonedetails'),(485,'Can add billing_return_diamond',122,'add_billingreturndiamonddetails'),(486,'Can change billing_return_diamond',122,'change_billingreturndiamonddetails'),(487,'Can delete billing_return_diamond',122,'delete_billingreturndiamonddetails'),(488,'Can view billing_return_diamond',122,'view_billingreturndiamonddetails'),(489,'Can add billing_old_gold_value',123,'add_billingoldgold'),(490,'Can change billing_old_gold_value',123,'change_billingoldgold'),(491,'Can delete billing_old_gold_value',123,'delete_billingoldgold'),(492,'Can view billing_old_gold_value',123,'view_billingoldgold'),(493,'Can add billing_item_diamond',124,'add_billingdiamonddetails'),(494,'Can change billing_item_diamond',124,'change_billingdiamonddetails'),(495,'Can delete billing_item_diamond',124,'delete_billingdiamonddetails'),(496,'Can view billing_item_diamond',124,'view_billingdiamonddetails'),(497,'Can add value_addition_designer',125,'add_valueadditiondesigner'),(498,'Can change value_addition_designer',125,'change_valueadditiondesigner'),(499,'Can delete value_addition_designer',125,'delete_valueadditiondesigner'),(500,'Can view value_addition_designer',125,'view_valueadditiondesigner'),(501,'Can add value_addition_customer',126,'add_valueadditioncustomer'),(502,'Can change value_addition_customer',126,'change_valueadditioncustomer'),(503,'Can delete value_addition_customer',126,'delete_valueadditioncustomer'),(504,'Can view value_addition_customer',126,'view_valueadditioncustomer'),(505,'Can add customer_group',127,'add_customergroup'),(506,'Can change customer_group',127,'change_customergroup'),(507,'Can delete customer_group',127,'delete_customergroup'),(508,'Can view customer_group',127,'view_customergroup'),(509,'Can add customer_detail',128,'add_customer'),(510,'Can change customer_detail',128,'change_customer'),(511,'Can delete customer_detail',128,'delete_customer'),(512,'Can view customer_detail',128,'view_customer'),(513,'Can add advance_purpose',129,'add_advancepurpose'),(514,'Can change advance_purpose',129,'change_advancepurpose'),(515,'Can delete advance_purpose',129,'delete_advancepurpose'),(516,'Can view advance_purpose',129,'view_advancepurpose'),(517,'Can add advance_payment',130,'add_advancepayment'),(518,'Can change advance_payment',130,'change_advancepayment'),(519,'Can delete advance_payment',130,'delete_advancepayment'),(520,'Can view advance_payment',130,'view_advancepayment'),(521,'Can add order_management_order_id',131,'add_orderid'),(522,'Can change order_management_order_id',131,'change_orderid'),(523,'Can delete order_management_order_id',131,'delete_orderid'),(524,'Can view order_management_order_id',131,'view_orderid'),(525,'Can add order_management_order_item_attachement',132,'add_orderitemattachments'),(526,'Can change order_management_order_item_attachement',132,'change_orderitemattachments'),(527,'Can delete order_management_order_item_attachement',132,'delete_orderitemattachments'),(528,'Can view order_management_order_item_attachement',132,'view_orderitemattachments'),(529,'Can add order_management_session_order_id',133,'add_sessionorderid'),(530,'Can change order_management_session_order_id',133,'change_sessionorderid'),(531,'Can delete order_management_session_order_id',133,'delete_sessionorderid'),(532,'Can view order_management_session_order_id',133,'view_sessionorderid'),(533,'Can add order_management_priority',134,'add_priority'),(534,'Can change order_management_priority',134,'change_priority'),(535,'Can delete order_management_priority',134,'delete_priority'),(536,'Can view order_management_priority',134,'view_priority'),(537,'Can add order_management_order_item',135,'add_orderitemdetails'),(538,'Can change order_management_order_item',135,'change_orderitemdetails'),(539,'Can delete order_management_order_item',135,'delete_orderitemdetails'),(540,'Can view order_management_order_item',135,'view_orderitemdetails'),(541,'Can add order_management_order_issue',136,'add_orderissue'),(542,'Can change order_management_order_issue',136,'change_orderissue'),(543,'Can delete order_management_order_issue',136,'delete_orderissue'),(544,'Can view order_management_order_issue',136,'view_orderissue'),(545,'Can add order_management_order_for',137,'add_orderfor'),(546,'Can change order_management_order_for',137,'change_orderfor'),(547,'Can delete order_management_order_for',137,'delete_orderfor'),(548,'Can view order_management_order_for',137,'view_orderfor'),(549,'Can add order_management_order_detail',138,'add_orderdetails'),(550,'Can change order_management_order_detail',138,'change_orderdetails'),(551,'Can delete order_management_order_detail',138,'delete_orderdetails'),(552,'Can view order_management_order_detail',138,'view_orderdetails'),(553,'Can add approval_type',139,'add_approvaltype'),(554,'Can change approval_type',139,'change_approvaltype'),(555,'Can delete approval_type',139,'delete_approvaltype'),(556,'Can view approval_type',139,'view_approvaltype'),(557,'Can add approval_rule',140,'add_approvalrule'),(558,'Can change approval_rule',140,'change_approvalrule'),(559,'Can delete approval_rule',140,'delete_approvalrule'),(560,'Can view approval_rule',140,'view_approvalrule'),(561,'Can add approval_issue',141,'add_approvalissue'),(562,'Can change approval_issue',141,'change_approvalissue'),(563,'Can delete approval_issue',141,'delete_approvalissue'),(564,'Can view approval_issue',141,'view_approvalissue'),(565,'Can add approval_issue_id',142,'add_approvalissueid'),(566,'Can change approval_issue_id',142,'change_approvalissueid'),(567,'Can delete approval_issue_id',142,'delete_approvalissueid'),(568,'Can view approval_issue_id',142,'view_approvalissueid'),(569,'Can add received_item',143,'add_receiveditem'),(570,'Can change received_item',143,'change_receiveditem'),(571,'Can delete received_item',143,'delete_receiveditem'),(572,'Can view received_item',143,'view_receiveditem'),(573,'Can add return_item',144,'add_returnitem'),(574,'Can change return_item',144,'change_returnitem'),(575,'Can delete return_item',144,'delete_returnitem'),(576,'Can view return_item',144,'view_returnitem'),(577,'Can add transerfer_item',145,'add_transferitem'),(578,'Can change transerfer_item',145,'change_transferitem'),(579,'Can delete transerfer_item',145,'delete_transferitem'),(580,'Can view transerfer_item',145,'view_transferitem'),(581,'Can add transfer_type',146,'add_transfertype'),(582,'Can change transfer_type',146,'change_transfertype'),(583,'Can delete transfer_type',146,'delete_transfertype'),(584,'Can view transfer_type',146,'view_transfertype'),(585,'Can add transferstatus',147,'add_transferstatus'),(586,'Can change transferstatus',147,'change_transferstatus'),(587,'Can delete transferstatus',147,'delete_transferstatus'),(588,'Can view transferstatus',147,'view_transferstatus'),(589,'Can add transferitem_detail',148,'add_transferitemdetails'),(590,'Can change transferitem_detail',148,'change_transferitemdetails'),(591,'Can delete transferitem_detail',148,'delete_transferitemdetails'),(592,'Can view transferitem_detail',148,'view_transferitemdetails'),(593,'Can add returnitem_detail',149,'add_returnitemdetails'),(594,'Can change returnitem_detail',149,'change_returnitemdetails'),(595,'Can delete returnitem_detail',149,'delete_returnitemdetails'),(596,'Can view returnitem_detail',149,'view_returnitemdetails'),(597,'Can add receiveditem_detail',150,'add_receiveditemdetails'),(598,'Can change receiveditem_detail',150,'change_receiveditemdetails'),(599,'Can delete receiveditem_detail',150,'delete_receiveditemdetails'),(600,'Can view receiveditem_detail',150,'view_receiveditemdetails'),(601,'Can add approval_issue_tag_item',151,'add_approvalissuetagitems'),(602,'Can change approval_issue_tag_item',151,'change_approvalissuetagitems'),(603,'Can delete approval_issue_tag_item',151,'delete_approvalissuetagitems'),(604,'Can view approval_issue_tag_item',151,'view_approvalissuetagitems'),(605,'Can add approval_issue_number',152,'add_approvalissuenumber'),(606,'Can change approval_issue_number',152,'change_approvalissuenumber'),(607,'Can delete approval_issue_number',152,'delete_approvalissuenumber'),(608,'Can view approval_issue_number',152,'view_approvalissuenumber'),(609,'Can add newpurchase',153,'add_newpurchase'),(610,'Can change newpurchase',153,'change_newpurchase'),(611,'Can delete newpurchase',153,'delete_newpurchase'),(612,'Can view newpurchase',153,'view_newpurchase'),(613,'Can add newpurchase_item_detail',154,'add_newpurchaseitemdetail'),(614,'Can change newpurchase_item_detail',154,'change_newpurchaseitemdetail'),(615,'Can delete newpurchase_item_detail',154,'delete_newpurchaseitemdetail'),(616,'Can view newpurchase_item_detail',154,'view_newpurchaseitemdetail'),(617,'Can add purchase_entry',155,'add_purchaseentry'),(618,'Can change purchase_entry',155,'change_purchaseentry'),(619,'Can delete purchase_entry',155,'delete_purchaseentry'),(620,'Can view purchase_entry',155,'view_purchaseentry'),(621,'Can add purchase_item_detail',156,'add_purchaseitemdetail'),(622,'Can change purchase_item_detail',156,'change_purchaseitemdetail'),(623,'Can delete purchase_item_detail',156,'delete_purchaseitemdetail'),(624,'Can view purchase_item_detail',156,'view_purchaseitemdetail'),(625,'Can add purchase_type',157,'add_purchasetype'),(626,'Can change purchase_type',157,'change_purchasetype'),(627,'Can delete purchase_type',157,'delete_purchasetype'),(628,'Can view purchase_type',157,'view_purchasetype'),(629,'Can add purchase_item_stone',158,'add_purchasestonedetails'),(630,'Can change purchase_item_stone',158,'change_purchasestonedetails'),(631,'Can delete purchase_item_stone',158,'delete_purchasestonedetails'),(632,'Can view purchase_item_stone',158,'view_purchasestonedetails'),(633,'Can add purchase_person_type',159,'add_purchasepersontype'),(634,'Can change purchase_person_type',159,'change_purchasepersontype'),(635,'Can delete purchase_person_type',159,'delete_purchasepersontype'),(636,'Can view purchase_person_type',159,'view_purchasepersontype'),(637,'Can add purchase_payment',160,'add_purchasepayment'),(638,'Can change purchase_payment',160,'change_purchasepayment'),(639,'Can delete purchase_payment',160,'delete_purchasepayment'),(640,'Can view purchase_payment',160,'view_purchasepayment'),(641,'Can add purchase_item_diamond',161,'add_purchasediamonddetails'),(642,'Can change purchase_item_diamond',161,'change_purchasediamonddetails'),(643,'Can delete purchase_item_diamond',161,'delete_purchasediamonddetails'),(644,'Can view purchase_item_diamond',161,'view_purchasediamonddetails'),(645,'Can add newpurchase_item_stone',162,'add_newpurchasestonedetails'),(646,'Can change newpurchase_item_stone',162,'change_newpurchasestonedetails'),(647,'Can delete newpurchase_item_stone',162,'delete_newpurchasestonedetails'),(648,'Can view newpurchase_item_stone',162,'view_newpurchasestonedetails'),(649,'Can add newpurchase_item_diamond',163,'add_newpurchasediamonddetails'),(650,'Can change newpurchase_item_diamond',163,'change_newpurchasediamonddetails'),(651,'Can delete newpurchase_item_diamond',163,'delete_newpurchasediamonddetails'),(652,'Can view newpurchase_item_diamond',163,'view_newpurchasediamonddetails'),(653,'Can add vendormetal_rate_cut',164,'add_metalratecut'),(654,'Can change vendormetal_rate_cut',164,'change_metalratecut'),(655,'Can delete vendormetal_rate_cut',164,'delete_metalratecut'),(656,'Can view vendormetal_rate_cut',164,'view_metalratecut'),(657,'Can add vendorcash_rate_cut',165,'add_cashratecut'),(658,'Can change vendorcash_rate_cut',165,'change_cashratecut'),(659,'Can delete vendorcash_rate_cut',165,'delete_cashratecut'),(660,'Can view vendorcash_rate_cut',165,'view_cashratecut'),(661,'Can add vendor_amountsettle',166,'add_amountsettle'),(662,'Can change vendor_amountsettle',166,'change_amountsettle'),(663,'Can delete vendor_amountsettle',166,'delete_amountsettle'),(664,'Can view vendor_amountsettle',166,'view_amountsettle'),(665,'Can add repair_detail',167,'add_repairdetails'),(666,'Can change repair_detail',167,'change_repairdetails'),(667,'Can delete repair_detail',167,'delete_repairdetails'),(668,'Can view repair_detail',167,'view_repairdetails'),(669,'Can add repair_order_oldgold',168,'add_repairorderoldgold'),(670,'Can change repair_order_oldgold',168,'change_repairorderoldgold'),(671,'Can delete repair_order_oldgold',168,'delete_repairorderoldgold'),(672,'Can view repair_order_oldgold',168,'view_repairorderoldgold'),(673,'Can add repair_number',169,'add_repairordernumber'),(674,'Can change repair_number',169,'change_repairordernumber'),(675,'Can delete repair_number',169,'delete_repairordernumber'),(676,'Can view repair_number',169,'view_repairordernumber'),(677,'Can add repair_order_issued',170,'add_repairorderissued'),(678,'Can change repair_order_issued',170,'change_repairorderissued'),(679,'Can delete repair_order_issued',170,'delete_repairorderissued'),(680,'Can view repair_order_issued',170,'view_repairorderissued'),(681,'Can add repair_item_detail',171,'add_repairitemdetails'),(682,'Can change repair_item_detail',171,'change_repairitemdetails'),(683,'Can delete repair_item_detail',171,'delete_repairitemdetails'),(684,'Can view repair_item_detail',171,'view_repairitemdetails'),(685,'Can add repair_for',172,'add_repairfor'),(686,'Can change repair_for',172,'change_repairfor'),(687,'Can delete repair_for',172,'delete_repairfor'),(688,'Can view repair_for',172,'view_repairfor'),(689,'Can add delivery_bill',173,'add_deliverybill'),(690,'Can change delivery_bill',173,'change_deliverybill'),(691,'Can delete delivery_bill',173,'delete_deliverybill'),(692,'Can view delivery_bill',173,'view_deliverybill'),(693,'Can add backup_bill_id',174,'add_backupbillid'),(694,'Can change backup_bill_id',174,'change_backupbillid'),(695,'Can delete backup_bill_id',174,'delete_backupbillid'),(696,'Can view backup_bill_id',174,'view_backupbillid'),(697,'Can add backup_bill_silver_id',175,'add_backupbillsilverbillid'),(698,'Can change backup_bill_silver_id',175,'change_backupbillsilverbillid'),(699,'Can delete backup_bill_silver_id',175,'delete_backupbillsilverbillid'),(700,'Can view backup_bill_silver_id',175,'view_backupbillsilverbillid'),(701,'Can add billing_backup_detail',176,'add_billingbackupdetails'),(702,'Can change billing_backup_detail',176,'change_billingbackupdetails'),(703,'Can delete billing_backup_detail',176,'delete_billingbackupdetails'),(704,'Can view billing_backup_detail',176,'view_billingbackupdetails'),(705,'Can add billing_backup_tagitem',177,'add_billingbackuptagitems'),(706,'Can change billing_backup_tagitem',177,'change_billingbackuptagitems'),(707,'Can delete billing_backup_tagitem',177,'delete_billingbackuptagitems'),(708,'Can view billing_backup_tagitem',177,'view_billingbackuptagitems'),(709,'Can add billing_backup_stone_detail',178,'add_billingbackupstonedetails'),(710,'Can change billing_backup_stone_detail',178,'change_billingbackupstonedetails'),(711,'Can delete billing_backup_stone_detail',178,'delete_billingbackupstonedetails'),(712,'Can view billing_backup_stone_detail',178,'view_billingbackupstonedetails'),(713,'Can add billing_backup_oldgold_detail',179,'add_billingbackupoldgold'),(714,'Can change billing_backup_oldgold_detail',179,'change_billingbackupoldgold'),(715,'Can delete billing_backup_oldgold_detail',179,'delete_billingbackupoldgold'),(716,'Can view billing_backup_oldgold_detail',179,'view_billingbackupoldgold'),(717,'Can add billing_backup_diamond_detail',180,'add_billingbackupdiamonddetails'),(718,'Can change billing_backup_diamond_detail',180,'change_billingbackupdiamonddetails'),(719,'Can delete billing_backup_diamond_detail',180,'delete_billingbackupdiamonddetails'),(720,'Can view billing_backup_diamond_detail',180,'view_billingbackupdiamonddetails'),(721,'Can add backup_bill_silver_number',181,'add_backupbillsilvernumber'),(722,'Can change backup_bill_silver_number',181,'change_backupbillsilvernumber'),(723,'Can delete backup_bill_silver_number',181,'delete_backupbillsilvernumber'),(724,'Can view backup_bill_silver_number',181,'view_backupbillsilvernumber'),(725,'Can add backup_bill_number',182,'add_backupbillnumber'),(726,'Can change backup_bill_number',182,'change_backupbillnumber'),(727,'Can delete backup_bill_number',182,'delete_backupbillnumber'),(728,'Can view backup_bill_number',182,'view_backupbillnumber'),(729,'Can add bag_id',183,'add_bagid'),(730,'Can change bag_id',183,'change_bagid'),(731,'Can delete bag_id',183,'delete_bagid'),(732,'Can view bag_id',183,'view_bagid'),(733,'Can add melting_issue',184,'add_meltingissue'),(734,'Can change melting_issue',184,'change_meltingissue'),(735,'Can delete melting_issue',184,'delete_meltingissue'),(736,'Can view melting_issue',184,'view_meltingissue'),(737,'Can add melting_issue_id',185,'add_meltingissueid'),(738,'Can change melting_issue_id',185,'change_meltingissueid'),(739,'Can delete melting_issue_id',185,'delete_meltingissueid'),(740,'Can view melting_issue_id',185,'view_meltingissueid'),(741,'Can add melting_recipt',186,'add_meltingrecipt'),(742,'Can change melting_recipt',186,'change_meltingrecipt'),(743,'Can delete melting_recipt',186,'delete_meltingrecipt'),(744,'Can view melting_recipt',186,'view_meltingrecipt'),(745,'Can add melting_recipt_id',187,'add_meltingreciptid'),(746,'Can change melting_recipt_id',187,'change_meltingreciptid'),(747,'Can delete melting_recipt_id',187,'delete_meltingreciptid'),(748,'Can view melting_recipt_id',187,'view_meltingreciptid'),(749,'Can add old_gold_type',188,'add_oldgoldtype'),(750,'Can change old_gold_type',188,'change_oldgoldtype'),(751,'Can delete old_gold_type',188,'delete_oldgoldtype'),(752,'Can view old_gold_type',188,'view_oldgoldtype'),(753,'Can add old_metal_category',189,'add_oldmetalcategory'),(754,'Can change old_metal_category',189,'change_oldmetalcategory'),(755,'Can delete old_metal_category',189,'delete_oldmetalcategory'),(756,'Can view old_metal_category',189,'view_oldmetalcategory'),(757,'Can add purification_issue',190,'add_purificationissue'),(758,'Can change purification_issue',190,'change_purificationissue'),(759,'Can delete purification_issue',190,'delete_purificationissue'),(760,'Can view purification_issue',190,'view_purificationissue'),(761,'Can add purification_issue_id',191,'add_purificationissueid'),(762,'Can change purification_issue_id',191,'change_purificationissueid'),(763,'Can delete purification_issue_id',191,'delete_purificationissueid'),(764,'Can view purification_issue_id',191,'view_purificationissueid'),(765,'Can add purification_recipt_id',192,'add_purificationreciptid'),(766,'Can change purification_recipt_id',192,'change_purificationreciptid'),(767,'Can delete purification_recipt_id',192,'delete_purificationreciptid'),(768,'Can view purification_recipt_id',192,'view_purificationreciptid'),(769,'Can add transfer_creation',193,'add_transfercreation'),(770,'Can change transfer_creation',193,'change_transfercreation'),(771,'Can delete transfer_creation',193,'delete_transfercreation'),(772,'Can view transfer_creation',193,'view_transfercreation'),(773,'Can add transfer_creation_type',194,'add_transfercreationtype'),(774,'Can change transfer_creation_type',194,'change_transfercreationtype'),(775,'Can delete transfer_creation_type',194,'delete_transfercreationtype'),(776,'Can view transfer_creation_type',194,'view_transfercreationtype'),(777,'Can add transfer_creation_item',195,'add_transfercreationitems'),(778,'Can change transfer_creation_item',195,'change_transfercreationitems'),(779,'Can delete transfer_creation_item',195,'delete_transfercreationitems'),(780,'Can view transfer_creation_item',195,'view_transfercreationitems'),(781,'Can add purification_recipt_number',196,'add_purificationreciptnumber'),(782,'Can change purification_recipt_number',196,'change_purificationreciptnumber'),(783,'Can delete purification_recipt_number',196,'delete_purificationreciptnumber'),(784,'Can view purification_recipt_number',196,'view_purificationreciptnumber'),(785,'Can add purification_recipt',197,'add_purificationrecipt'),(786,'Can change purification_recipt',197,'change_purificationrecipt'),(787,'Can delete purification_recipt',197,'delete_purificationrecipt'),(788,'Can view purification_recipt',197,'view_purificationrecipt'),(789,'Can add purification_issue_number',198,'add_purificationissuenumber'),(790,'Can change purification_issue_number',198,'change_purificationissuenumber'),(791,'Can delete purification_issue_number',198,'delete_purificationissuenumber'),(792,'Can view purification_issue_number',198,'view_purificationissuenumber'),(793,'Can add melting_recipt_number',199,'add_meltingreciptnumber'),(794,'Can change melting_recipt_number',199,'change_meltingreciptnumber'),(795,'Can delete melting_recipt_number',199,'delete_meltingreciptnumber'),(796,'Can view melting_recipt_number',199,'view_meltingreciptnumber'),(797,'Can add melting_issue_number',200,'add_meltingissuenumber'),(798,'Can change melting_issue_number',200,'change_meltingissuenumber'),(799,'Can delete melting_issue_number',200,'delete_meltingissuenumber'),(800,'Can view melting_issue_number',200,'view_meltingissuenumber'),(801,'Can add bag_number',201,'add_bagnumber'),(802,'Can change bag_number',201,'change_bagnumber'),(803,'Can delete bag_number',201,'delete_bagnumber'),(804,'Can view bag_number',201,'view_bagnumber'),(805,'Can add payment_method',202,'add_paymentmenthod'),(806,'Can change payment_method',202,'change_paymentmenthod'),(807,'Can delete payment_method',202,'delete_paymentmenthod'),(808,'Can view payment_method',202,'view_paymentmenthod'),(809,'Can add payment_module',203,'add_paymentmodule'),(810,'Can change payment_module',203,'change_paymentmodule'),(811,'Can delete payment_module',203,'delete_paymentmodule'),(812,'Can view payment_module',203,'view_paymentmodule'),(813,'Can add payment_provider',204,'add_paymentproviders'),(814,'Can change payment_provider',204,'change_paymentproviders'),(815,'Can delete payment_provider',204,'delete_paymentproviders'),(816,'Can view payment_provider',204,'view_paymentproviders'),(817,'Can add payment_table',205,'add_customerpaymenttabel'),(818,'Can change payment_table',205,'change_customerpaymenttabel'),(819,'Can delete payment_table',205,'delete_customerpaymenttabel'),(820,'Can view payment_table',205,'view_customerpaymenttabel'),(821,'Can add common_payment',206,'add_commonpaymentdetails'),(822,'Can change common_payment',206,'change_commonpaymentdetails'),(823,'Can delete common_payment',206,'delete_commonpaymentdetails'),(824,'Can view common_payment',206,'view_commonpaymentdetails');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('3f481aae6463edace17a1c702c9fd0d5043bac88','2024-07-03 06:21:57.021320',3),('7c9c1471884b778f025f0bf86bd411b0a978c634','2024-07-03 06:21:07.758414',2);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backup_bill_id`
--

DROP TABLE IF EXISTS `backup_bill_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backup_bill_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `backupbill_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `backupbill_id` (`backupbill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_bill_id`
--

LOCK TABLES `backup_bill_id` WRITE;
/*!40000 ALTER TABLE `backup_bill_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `backup_bill_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backup_bill_number`
--

DROP TABLE IF EXISTS `backup_bill_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backup_bill_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `backupbill_number` varchar(50) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `backupbill_number` (`backupbill_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `backup_bill_number_user_id_30270549_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_bill_number`
--

LOCK TABLES `backup_bill_number` WRITE;
/*!40000 ALTER TABLE `backup_bill_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `backup_bill_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backup_bill_silver_id`
--

DROP TABLE IF EXISTS `backup_bill_silver_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backup_bill_silver_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `backupbill_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `backupbill_id` (`backupbill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_bill_silver_id`
--

LOCK TABLES `backup_bill_silver_id` WRITE;
/*!40000 ALTER TABLE `backup_bill_silver_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `backup_bill_silver_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backup_bill_silver_number`
--

DROP TABLE IF EXISTS `backup_bill_silver_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backup_bill_silver_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `backupbill_number` varchar(50) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `backupbill_number` (`backupbill_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `backup_bill_silver_number_user_id_4c7cbf98_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_bill_silver_number`
--

LOCK TABLES `backup_bill_silver_number` WRITE;
/*!40000 ALTER TABLE `backup_bill_silver_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `backup_bill_silver_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bag_id`
--

DROP TABLE IF EXISTS `bag_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bag_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bag_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bag_id` (`bag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bag_id`
--

LOCK TABLES `bag_id` WRITE;
/*!40000 ALTER TABLE `bag_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `bag_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bag_number`
--

DROP TABLE IF EXISTS `bag_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bag_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bag_number` varchar(50) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bag_number` (`bag_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `bag_number_user_id_992d7776_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bag_number`
--

LOCK TABLES `bag_number` WRITE;
/*!40000 ALTER TABLE `bag_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `bag_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bill_id`
--

DROP TABLE IF EXISTS `bill_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bill_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bill_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bill_id` (`bill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill_id`
--

LOCK TABLES `bill_id` WRITE;
/*!40000 ALTER TABLE `bill_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `bill_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bill_number`
--

DROP TABLE IF EXISTS `bill_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bill_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bill_number` varchar(10) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bill_number` (`bill_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `bill_number_user_id_d5f8aaaa_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill_number`
--

LOCK TABLES `bill_number` WRITE;
/*!40000 ALTER TABLE `bill_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `bill_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bill_type`
--

DROP TABLE IF EXISTS `bill_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bill_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bill_type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bill_type` (`bill_type`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill_type`
--

LOCK TABLES `bill_type` WRITE;
/*!40000 ALTER TABLE `bill_type` DISABLE KEYS */;
INSERT INTO `bill_type` VALUES (1,'gold'),(2,'silver');
/*!40000 ALTER TABLE `bill_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_backup_detail`
--

DROP TABLE IF EXISTS `billing_backup_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_backup_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bill_no` varchar(20) DEFAULT NULL,
  `bill_date` datetime(6) DEFAULT NULL,
  `customer_mobile` varchar(10) DEFAULT NULL,
  `total_amount` double NOT NULL,
  `gst_amount` double NOT NULL,
  `advance_amount` double NOT NULL,
  `discount_amount` double NOT NULL,
  `exchange_amount` double NOT NULL,
  `chit_amount` double NOT NULL,
  `payable_amount` double NOT NULL,
  `cash_amount` double NOT NULL,
  `card_amount` double NOT NULL,
  `account_transfer_amount` double NOT NULL,
  `upi_amount` double NOT NULL,
  `paid_amount` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `bill_type_id` bigint DEFAULT NULL,
  `branch_id` bigint DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `customer_details_id` bigint NOT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bill_no` (`bill_no`),
  KEY `billing_backup_detail_bill_type_id_0375af7c_fk_bill_type_id` (`bill_type_id`),
  KEY `billing_backup_detail_branch_id_ab655dc4_fk_branches_id` (`branch_id`),
  KEY `billing_backup_detail_created_by_id_212b9c0a_fk_users_id` (`created_by_id`),
  KEY `billing_backup_detai_customer_details_id_d6932b24_fk_customer_` (`customer_details_id`),
  KEY `billing_backup_detail_modified_by_id_9a2f173a_fk_users_id` (`modified_by_id`),
  CONSTRAINT `billing_backup_detai_customer_details_id_d6932b24_fk_customer_` FOREIGN KEY (`customer_details_id`) REFERENCES `customer_details` (`id`),
  CONSTRAINT `billing_backup_detail_bill_type_id_0375af7c_fk_bill_type_id` FOREIGN KEY (`bill_type_id`) REFERENCES `bill_type` (`id`),
  CONSTRAINT `billing_backup_detail_branch_id_ab655dc4_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `billing_backup_detail_created_by_id_212b9c0a_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `billing_backup_detail_modified_by_id_9a2f173a_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_backup_detail`
--

LOCK TABLES `billing_backup_detail` WRITE;
/*!40000 ALTER TABLE `billing_backup_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_backup_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_backup_diamond_detail`
--

DROP TABLE IF EXISTS `billing_backup_diamond_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_backup_diamond_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `diamond_pieces` int DEFAULT NULL,
  `diamond_weight` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `include_diamond_weight` tinyint(1) NOT NULL,
  `total_diamond_value` double DEFAULT NULL,
  `billing_details_id` bigint NOT NULL,
  `billing_item_details_id` bigint NOT NULL,
  `diamond_name_id` bigint NOT NULL,
  `diamond_rate_type_id` bigint NOT NULL,
  `diamond_weight_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `billing_backup_diamo_billing_details_id_b89585b3_fk_billing_b` (`billing_details_id`),
  KEY `billing_backup_diamo_billing_item_details_c3cc8a97_fk_billing_b` (`billing_item_details_id`),
  KEY `billing_backup_diamo_diamond_name_id_94d7e966_fk_stone_det` (`diamond_name_id`),
  KEY `billing_backup_diamo_diamond_rate_type_id_d19d8421_fk_rate_type` (`diamond_rate_type_id`),
  KEY `billing_backup_diamo_diamond_weight_type__8904cd29_fk_stone_wei` (`diamond_weight_type_id`),
  CONSTRAINT `billing_backup_diamo_billing_details_id_b89585b3_fk_billing_b` FOREIGN KEY (`billing_details_id`) REFERENCES `billing_backup_detail` (`id`),
  CONSTRAINT `billing_backup_diamo_billing_item_details_c3cc8a97_fk_billing_b` FOREIGN KEY (`billing_item_details_id`) REFERENCES `billing_backup_tagitem` (`id`),
  CONSTRAINT `billing_backup_diamo_diamond_name_id_94d7e966_fk_stone_det` FOREIGN KEY (`diamond_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `billing_backup_diamo_diamond_rate_type_id_d19d8421_fk_rate_type` FOREIGN KEY (`diamond_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `billing_backup_diamo_diamond_weight_type__8904cd29_fk_stone_wei` FOREIGN KEY (`diamond_weight_type_id`) REFERENCES `stone_weight_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_backup_diamond_detail`
--

LOCK TABLES `billing_backup_diamond_detail` WRITE;
/*!40000 ALTER TABLE `billing_backup_diamond_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_backup_diamond_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_backup_oldgold_detail`
--

DROP TABLE IF EXISTS `billing_backup_oldgold_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_backup_oldgold_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_name` varchar(150) DEFAULT NULL,
  `old_gold_no` varchar(100) DEFAULT NULL,
  `metal_rate` double DEFAULT NULL,
  `today_metal_rate` double DEFAULT NULL,
  `old_gross_weight` double DEFAULT NULL,
  `old_net_weight` double DEFAULT NULL,
  `dust_weight` double DEFAULT NULL,
  `old_metal_rate` double DEFAULT NULL,
  `total_old_gold_value` double DEFAULT NULL,
  `billing_details_id` bigint NOT NULL,
  `old_metal_id` bigint NOT NULL,
  `purity_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `billing_backup_oldgo_billing_details_id_b16962ec_fk_billing_b` (`billing_details_id`),
  KEY `billing_backup_oldgold_detail_old_metal_id_c6b8b8d1_fk_metals_id` (`old_metal_id`),
  KEY `billing_backup_oldgold_detail_purity_id_41c68de2_fk_purities_id` (`purity_id`),
  CONSTRAINT `billing_backup_oldgo_billing_details_id_b16962ec_fk_billing_b` FOREIGN KEY (`billing_details_id`) REFERENCES `billing_backup_detail` (`id`),
  CONSTRAINT `billing_backup_oldgold_detail_old_metal_id_c6b8b8d1_fk_metals_id` FOREIGN KEY (`old_metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `billing_backup_oldgold_detail_purity_id_41c68de2_fk_purities_id` FOREIGN KEY (`purity_id`) REFERENCES `purities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_backup_oldgold_detail`
--

LOCK TABLES `billing_backup_oldgold_detail` WRITE;
/*!40000 ALTER TABLE `billing_backup_oldgold_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_backup_oldgold_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_backup_stone_detail`
--

DROP TABLE IF EXISTS `billing_backup_stone_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_backup_stone_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stone_pieces` int DEFAULT NULL,
  `stone_weight` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `include_stone_weight` tinyint(1) NOT NULL,
  `total_stone_value` double DEFAULT NULL,
  `billing_details_id` bigint NOT NULL,
  `billing_item_details_id` bigint NOT NULL,
  `stone_name_id` bigint NOT NULL,
  `stone_rate_type_id` bigint NOT NULL,
  `stone_weight_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `billing_backup_stone_billing_details_id_4d7e29f4_fk_billing_b` (`billing_details_id`),
  KEY `billing_backup_stone_billing_item_details_7097528a_fk_billing_b` (`billing_item_details_id`),
  KEY `billing_backup_stone_stone_name_id_6860b28e_fk_stone_det` (`stone_name_id`),
  KEY `billing_backup_stone_stone_rate_type_id_c0b70c19_fk_rate_type` (`stone_rate_type_id`),
  KEY `billing_backup_stone_stone_weight_type_id_daae403f_fk_stone_wei` (`stone_weight_type_id`),
  CONSTRAINT `billing_backup_stone_billing_details_id_4d7e29f4_fk_billing_b` FOREIGN KEY (`billing_details_id`) REFERENCES `billing_backup_detail` (`id`),
  CONSTRAINT `billing_backup_stone_billing_item_details_7097528a_fk_billing_b` FOREIGN KEY (`billing_item_details_id`) REFERENCES `billing_backup_tagitem` (`id`),
  CONSTRAINT `billing_backup_stone_stone_name_id_6860b28e_fk_stone_det` FOREIGN KEY (`stone_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `billing_backup_stone_stone_rate_type_id_c0b70c19_fk_rate_type` FOREIGN KEY (`stone_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `billing_backup_stone_stone_weight_type_id_daae403f_fk_stone_wei` FOREIGN KEY (`stone_weight_type_id`) REFERENCES `stone_weight_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_backup_stone_detail`
--

LOCK TABLES `billing_backup_stone_detail` WRITE;
/*!40000 ALTER TABLE `billing_backup_stone_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_backup_stone_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_backup_tagitem`
--

DROP TABLE IF EXISTS `billing_backup_tagitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_backup_tagitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_number` int DEFAULT NULL,
  `net_weight` double DEFAULT NULL,
  `gross_weight` double DEFAULT NULL,
  `tag_weight` double DEFAULT NULL,
  `cover_weight` double DEFAULT NULL,
  `loop_weight` double DEFAULT NULL,
  `other_weight` double DEFAULT NULL,
  `pieces` int DEFAULT NULL,
  `total_pieces` int DEFAULT NULL,
  `rate` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `wastage_percentage` double DEFAULT NULL,
  `flat_wastage` double DEFAULT NULL,
  `making_charge` double DEFAULT NULL,
  `huid_rate` double DEFAULT NULL,
  `flat_making_charge` double DEFAULT NULL,
  `tax_percent` double DEFAULT NULL,
  `additional_charges` double DEFAULT NULL,
  `total_stone_weight` double DEFAULT NULL,
  `total_diamond_weight` double DEFAULT NULL,
  `gst` double DEFAULT NULL,
  `total_rate` double DEFAULT NULL,
  `without_gst_rate` double DEFAULT NULL,
  `billing_details_id` bigint NOT NULL,
  `billing_tag_item_id` bigint NOT NULL,
  `calculation_type_id` bigint NOT NULL,
  `item_details_id` bigint NOT NULL,
  `making_charge_calculation_type_id` bigint DEFAULT NULL,
  `metal_id` bigint NOT NULL,
  `per_gram_weight_type_id` bigint DEFAULT NULL,
  `stock_type_id` bigint NOT NULL,
  `sub_item_details_id` bigint NOT NULL,
  `wastage_calculation_type_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `billing_backup_tagit_billing_details_id_03cf5c24_fk_billing_b` (`billing_details_id`),
  KEY `billing_backup_tagit_billing_tag_item_id_dc2d87b7_fk_tagged_it` (`billing_tag_item_id`),
  KEY `billing_backup_tagit_calculation_type_id_0117c131_fk_calculati` (`calculation_type_id`),
  KEY `billing_backup_tagit_item_details_id_5639892e_fk_item_deta` (`item_details_id`),
  KEY `billing_backup_tagit_making_charge_calcul_75cde2a6_fk_weight_ty` (`making_charge_calculation_type_id`),
  KEY `billing_backup_tagitem_metal_id_e5403fae_fk_metals_id` (`metal_id`),
  KEY `billing_backup_tagit_per_gram_weight_type_19d3064a_fk_weight_ty` (`per_gram_weight_type_id`),
  KEY `billing_backup_tagitem_stock_type_id_94d87ac5_fk_stock_type_id` (`stock_type_id`),
  KEY `billing_backup_tagit_sub_item_details_id_be1dda46_fk_sub_item_` (`sub_item_details_id`),
  KEY `billing_backup_tagit_wastage_calculation__7dd04848_fk_weight_ty` (`wastage_calculation_type_id`),
  CONSTRAINT `billing_backup_tagit_billing_details_id_03cf5c24_fk_billing_b` FOREIGN KEY (`billing_details_id`) REFERENCES `billing_backup_detail` (`id`),
  CONSTRAINT `billing_backup_tagit_billing_tag_item_id_dc2d87b7_fk_tagged_it` FOREIGN KEY (`billing_tag_item_id`) REFERENCES `tagged_item` (`id`),
  CONSTRAINT `billing_backup_tagit_calculation_type_id_0117c131_fk_calculati` FOREIGN KEY (`calculation_type_id`) REFERENCES `calculation_type` (`id`),
  CONSTRAINT `billing_backup_tagit_item_details_id_5639892e_fk_item_deta` FOREIGN KEY (`item_details_id`) REFERENCES `item_detail` (`id`),
  CONSTRAINT `billing_backup_tagit_making_charge_calcul_75cde2a6_fk_weight_ty` FOREIGN KEY (`making_charge_calculation_type_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `billing_backup_tagit_per_gram_weight_type_19d3064a_fk_weight_ty` FOREIGN KEY (`per_gram_weight_type_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `billing_backup_tagit_sub_item_details_id_be1dda46_fk_sub_item_` FOREIGN KEY (`sub_item_details_id`) REFERENCES `sub_item_detail` (`id`),
  CONSTRAINT `billing_backup_tagit_wastage_calculation__7dd04848_fk_weight_ty` FOREIGN KEY (`wastage_calculation_type_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `billing_backup_tagitem_metal_id_e5403fae_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `billing_backup_tagitem_stock_type_id_94d87ac5_fk_stock_type_id` FOREIGN KEY (`stock_type_id`) REFERENCES `stock_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_backup_tagitem`
--

LOCK TABLES `billing_backup_tagitem` WRITE;
/*!40000 ALTER TABLE `billing_backup_tagitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_backup_tagitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_detail`
--

DROP TABLE IF EXISTS `billing_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bill_no` varchar(20) DEFAULT NULL,
  `bill_date` datetime(6) DEFAULT NULL,
  `customer_mobile` varchar(10) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `bill_type_id` bigint DEFAULT NULL,
  `branch_id` bigint DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `customer_details_id` bigint NOT NULL,
  `estimation_details_id` bigint DEFAULT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  `payment_status_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bill_no` (`bill_no`),
  KEY `billing_detail_bill_type_id_7e066b8b_fk_bill_type_id` (`bill_type_id`),
  KEY `billing_detail_branch_id_7bc67cd7_fk_branches_id` (`branch_id`),
  KEY `billing_detail_created_by_id_c9d8eee4_fk_users_id` (`created_by_id`),
  KEY `billing_detail_customer_details_id_2462d11a_fk_customer_` (`customer_details_id`),
  KEY `billing_detail_estimation_details_i_4aba0ace_fk_estimatio` (`estimation_details_id`),
  KEY `billing_detail_modified_by_id_8ce809da_fk_users_id` (`modified_by_id`),
  KEY `billing_detail_payment_status_id_cc6a3325_fk_payment_status_id` (`payment_status_id`),
  CONSTRAINT `billing_detail_bill_type_id_7e066b8b_fk_bill_type_id` FOREIGN KEY (`bill_type_id`) REFERENCES `bill_type` (`id`),
  CONSTRAINT `billing_detail_branch_id_7bc67cd7_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `billing_detail_created_by_id_c9d8eee4_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `billing_detail_customer_details_id_2462d11a_fk_customer_` FOREIGN KEY (`customer_details_id`) REFERENCES `customer_details` (`id`),
  CONSTRAINT `billing_detail_estimation_details_i_4aba0ace_fk_estimatio` FOREIGN KEY (`estimation_details_id`) REFERENCES `estimation_detail` (`id`),
  CONSTRAINT `billing_detail_modified_by_id_8ce809da_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `billing_detail_payment_status_id_cc6a3325_fk_payment_status_id` FOREIGN KEY (`payment_status_id`) REFERENCES `payment_status` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_detail`
--

LOCK TABLES `billing_detail` WRITE;
/*!40000 ALTER TABLE `billing_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_item_diamond`
--

DROP TABLE IF EXISTS `billing_item_diamond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_item_diamond` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `diamond_pieces` int DEFAULT NULL,
  `diamond_weight` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `include_diamond_weight` tinyint(1) NOT NULL,
  `total_diamond_value` double DEFAULT NULL,
  `billing_details_id` bigint NOT NULL,
  `billing_item_details_id` bigint NOT NULL,
  `diamond_name_id` bigint NOT NULL,
  `diamond_rate_type_id` bigint NOT NULL,
  `diamond_weight_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `billing_item_diamond_billing_details_id_6c542882_fk_billing_d` (`billing_details_id`),
  KEY `billing_item_diamond_billing_item_details_f5f3f1b4_fk_billing_t` (`billing_item_details_id`),
  KEY `billing_item_diamond_diamond_name_id_96cd8e2f_fk_stone_detail_id` (`diamond_name_id`),
  KEY `billing_item_diamond_diamond_rate_type_id_119a9b82_fk_rate_type` (`diamond_rate_type_id`),
  KEY `billing_item_diamond_diamond_weight_type__59c76a53_fk_stone_wei` (`diamond_weight_type_id`),
  CONSTRAINT `billing_item_diamond_billing_details_id_6c542882_fk_billing_d` FOREIGN KEY (`billing_details_id`) REFERENCES `billing_detail` (`id`),
  CONSTRAINT `billing_item_diamond_billing_item_details_f5f3f1b4_fk_billing_t` FOREIGN KEY (`billing_item_details_id`) REFERENCES `billing_tag_value` (`id`),
  CONSTRAINT `billing_item_diamond_diamond_name_id_96cd8e2f_fk_stone_detail_id` FOREIGN KEY (`diamond_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `billing_item_diamond_diamond_rate_type_id_119a9b82_fk_rate_type` FOREIGN KEY (`diamond_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `billing_item_diamond_diamond_weight_type__59c76a53_fk_stone_wei` FOREIGN KEY (`diamond_weight_type_id`) REFERENCES `stone_weight_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_item_diamond`
--

LOCK TABLES `billing_item_diamond` WRITE;
/*!40000 ALTER TABLE `billing_item_diamond` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_item_diamond` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_item_stone`
--

DROP TABLE IF EXISTS `billing_item_stone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_item_stone` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stone_pieces` int DEFAULT NULL,
  `stone_weight` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `include_stone_weight` tinyint(1) NOT NULL,
  `total_stone_value` double DEFAULT NULL,
  `billing_details_id` bigint NOT NULL,
  `billing_item_details_id` bigint NOT NULL,
  `stone_name_id` bigint NOT NULL,
  `stone_rate_type_id` bigint NOT NULL,
  `stone_weight_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `billing_item_stone_billing_details_id_171cc69f_fk_billing_d` (`billing_details_id`),
  KEY `billing_item_stone_billing_item_details_fd69e34a_fk_billing_t` (`billing_item_details_id`),
  KEY `billing_item_stone_stone_name_id_9eda8886_fk_stone_detail_id` (`stone_name_id`),
  KEY `billing_item_stone_stone_rate_type_id_edc08144_fk_rate_type_id` (`stone_rate_type_id`),
  KEY `billing_item_stone_stone_weight_type_id_569f2a2d_fk_stone_wei` (`stone_weight_type_id`),
  CONSTRAINT `billing_item_stone_billing_details_id_171cc69f_fk_billing_d` FOREIGN KEY (`billing_details_id`) REFERENCES `billing_detail` (`id`),
  CONSTRAINT `billing_item_stone_billing_item_details_fd69e34a_fk_billing_t` FOREIGN KEY (`billing_item_details_id`) REFERENCES `billing_tag_value` (`id`),
  CONSTRAINT `billing_item_stone_stone_name_id_9eda8886_fk_stone_detail_id` FOREIGN KEY (`stone_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `billing_item_stone_stone_rate_type_id_edc08144_fk_rate_type_id` FOREIGN KEY (`stone_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `billing_item_stone_stone_weight_type_id_569f2a2d_fk_stone_wei` FOREIGN KEY (`stone_weight_type_id`) REFERENCES `stone_weight_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_item_stone`
--

LOCK TABLES `billing_item_stone` WRITE;
/*!40000 ALTER TABLE `billing_item_stone` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_item_stone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_misc_issue_detail`
--

DROP TABLE IF EXISTS `billing_misc_issue_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_misc_issue_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `issue_date` date NOT NULL,
  `giver_name` varchar(100) DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `total_gross_weight` double NOT NULL,
  `total_net_weight` double NOT NULL,
  `total_pieces` int NOT NULL,
  `total_amount` double NOT NULL,
  `bill_amount` double NOT NULL,
  `net_amount` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `branch_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `customer_id` bigint NOT NULL,
  `misc_issue_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `misc_issue_id_id` (`misc_issue_id_id`),
  KEY `billing_misc_issue_detail_branch_id_33157143_fk_branches_id` (`branch_id`),
  KEY `billing_misc_issue_detail_created_by_id_7dfc537e_fk_users_id` (`created_by_id`),
  KEY `billing_misc_issue_d_customer_id_ab4cba10_fk_customer_` (`customer_id`),
  CONSTRAINT `billing_misc_issue_d_customer_id_ab4cba10_fk_customer_` FOREIGN KEY (`customer_id`) REFERENCES `customer_details` (`id`),
  CONSTRAINT `billing_misc_issue_d_misc_issue_id_id_573d11eb_fk_billing_m` FOREIGN KEY (`misc_issue_id_id`) REFERENCES `billing_misc_issue_id` (`id`),
  CONSTRAINT `billing_misc_issue_detail_branch_id_33157143_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `billing_misc_issue_detail_created_by_id_7dfc537e_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_misc_issue_detail`
--

LOCK TABLES `billing_misc_issue_detail` WRITE;
/*!40000 ALTER TABLE `billing_misc_issue_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_misc_issue_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_misc_issue_id`
--

DROP TABLE IF EXISTS `billing_misc_issue_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_misc_issue_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `misc_issue_id` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `misc_issue_id` (`misc_issue_id`),
  KEY `billing_misc_issue_id_created_by_id_ab6fcd90_fk_users_id` (`created_by_id`),
  CONSTRAINT `billing_misc_issue_id_created_by_id_ab6fcd90_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_misc_issue_id`
--

LOCK TABLES `billing_misc_issue_id` WRITE;
/*!40000 ALTER TABLE `billing_misc_issue_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_misc_issue_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_misc_particular`
--

DROP TABLE IF EXISTS `billing_misc_particular`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_misc_particular` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pieces` int NOT NULL,
  `metal_rate` double NOT NULL,
  `amount` double NOT NULL,
  `misc_issue_details_id` bigint NOT NULL,
  `tag_number_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `billing_misc_particu_misc_issue_details_i_1f72bd5b_fk_billing_m` (`misc_issue_details_id`),
  KEY `billing_misc_particular_tag_number_id_2a9637a4_fk_tagged_item_id` (`tag_number_id`),
  CONSTRAINT `billing_misc_particu_misc_issue_details_i_1f72bd5b_fk_billing_m` FOREIGN KEY (`misc_issue_details_id`) REFERENCES `billing_misc_issue_detail` (`id`),
  CONSTRAINT `billing_misc_particular_tag_number_id_2a9637a4_fk_tagged_item_id` FOREIGN KEY (`tag_number_id`) REFERENCES `tagged_item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_misc_particular`
--

LOCK TABLES `billing_misc_particular` WRITE;
/*!40000 ALTER TABLE `billing_misc_particular` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_misc_particular` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_old_gold_value`
--

DROP TABLE IF EXISTS `billing_old_gold_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_old_gold_value` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_name` varchar(150) DEFAULT NULL,
  `old_gold_no` varchar(100) NOT NULL,
  `metal_rate` double DEFAULT NULL,
  `today_metal_rate` double DEFAULT NULL,
  `old_gross_weight` double DEFAULT NULL,
  `old_net_weight` double DEFAULT NULL,
  `dust_weight` double DEFAULT NULL,
  `old_metal_rate` double DEFAULT NULL,
  `total_old_gold_value` double DEFAULT NULL,
  `is_transfered` tinyint(1) NOT NULL,
  `billing_details_id` bigint NOT NULL,
  `old_metal_id` bigint NOT NULL,
  `purity_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `billing_old_gold_val_billing_details_id_e7af3059_fk_billing_d` (`billing_details_id`),
  KEY `billing_old_gold_value_old_metal_id_03e4e6a3_fk_metals_id` (`old_metal_id`),
  KEY `billing_old_gold_value_purity_id_1f8f6b60_fk_purities_id` (`purity_id`),
  CONSTRAINT `billing_old_gold_val_billing_details_id_e7af3059_fk_billing_d` FOREIGN KEY (`billing_details_id`) REFERENCES `billing_detail` (`id`),
  CONSTRAINT `billing_old_gold_value_old_metal_id_03e4e6a3_fk_metals_id` FOREIGN KEY (`old_metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `billing_old_gold_value_purity_id_1f8f6b60_fk_purities_id` FOREIGN KEY (`purity_id`) REFERENCES `purities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_old_gold_value`
--

LOCK TABLES `billing_old_gold_value` WRITE;
/*!40000 ALTER TABLE `billing_old_gold_value` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_old_gold_value` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_return_diamond`
--

DROP TABLE IF EXISTS `billing_return_diamond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_return_diamond` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `diamond_pieces` int DEFAULT NULL,
  `diamond_weight` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `include_diamond_weight` tinyint(1) NOT NULL,
  `total_diamond_value` double DEFAULT NULL,
  `billing_details_id` bigint NOT NULL,
  `billing_return_item_id` bigint NOT NULL,
  `diamond_name_id` bigint NOT NULL,
  `diamond_rate_type_id` bigint NOT NULL,
  `diamond_weight_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `billing_return_diamo_billing_details_id_03172a2d_fk_billing_d` (`billing_details_id`),
  KEY `billing_return_diamo_billing_return_item__30ea4d77_fk_billing_s` (`billing_return_item_id`),
  KEY `billing_return_diamo_diamond_name_id_5120fa07_fk_stone_det` (`diamond_name_id`),
  KEY `billing_return_diamo_diamond_rate_type_id_f411b89a_fk_rate_type` (`diamond_rate_type_id`),
  KEY `billing_return_diamo_diamond_weight_type__903bf24d_fk_stone_wei` (`diamond_weight_type_id`),
  CONSTRAINT `billing_return_diamo_billing_details_id_03172a2d_fk_billing_d` FOREIGN KEY (`billing_details_id`) REFERENCES `billing_detail` (`id`),
  CONSTRAINT `billing_return_diamo_billing_return_item__30ea4d77_fk_billing_s` FOREIGN KEY (`billing_return_item_id`) REFERENCES `billing_sale_return` (`id`),
  CONSTRAINT `billing_return_diamo_diamond_name_id_5120fa07_fk_stone_det` FOREIGN KEY (`diamond_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `billing_return_diamo_diamond_rate_type_id_f411b89a_fk_rate_type` FOREIGN KEY (`diamond_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `billing_return_diamo_diamond_weight_type__903bf24d_fk_stone_wei` FOREIGN KEY (`diamond_weight_type_id`) REFERENCES `stone_weight_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_return_diamond`
--

LOCK TABLES `billing_return_diamond` WRITE;
/*!40000 ALTER TABLE `billing_return_diamond` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_return_diamond` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_return_stone`
--

DROP TABLE IF EXISTS `billing_return_stone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_return_stone` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stone_pieces` int DEFAULT NULL,
  `stone_weight` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `include_stone_weight` tinyint(1) NOT NULL,
  `total_stone_value` double DEFAULT NULL,
  `billing_details_id` bigint NOT NULL,
  `billing_return_item_id` bigint NOT NULL,
  `stone_name_id` bigint NOT NULL,
  `stone_rate_type_id` bigint NOT NULL,
  `stone_weight_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `billing_return_stone_billing_details_id_cd99c6ec_fk_billing_d` (`billing_details_id`),
  KEY `billing_return_stone_billing_return_item__fb32a730_fk_billing_s` (`billing_return_item_id`),
  KEY `billing_return_stone_stone_name_id_0f6e39f6_fk_stone_detail_id` (`stone_name_id`),
  KEY `billing_return_stone_stone_rate_type_id_483ac1db_fk_rate_type_id` (`stone_rate_type_id`),
  KEY `billing_return_stone_stone_weight_type_id_4ab4d65f_fk_stone_wei` (`stone_weight_type_id`),
  CONSTRAINT `billing_return_stone_billing_details_id_cd99c6ec_fk_billing_d` FOREIGN KEY (`billing_details_id`) REFERENCES `billing_detail` (`id`),
  CONSTRAINT `billing_return_stone_billing_return_item__fb32a730_fk_billing_s` FOREIGN KEY (`billing_return_item_id`) REFERENCES `billing_sale_return` (`id`),
  CONSTRAINT `billing_return_stone_stone_name_id_0f6e39f6_fk_stone_detail_id` FOREIGN KEY (`stone_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `billing_return_stone_stone_rate_type_id_483ac1db_fk_rate_type_id` FOREIGN KEY (`stone_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `billing_return_stone_stone_weight_type_id_4ab4d65f_fk_stone_wei` FOREIGN KEY (`stone_weight_type_id`) REFERENCES `stone_weight_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_return_stone`
--

LOCK TABLES `billing_return_stone` WRITE;
/*!40000 ALTER TABLE `billing_return_stone` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_return_stone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_sale_return`
--

DROP TABLE IF EXISTS `billing_sale_return`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_sale_return` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_number` int DEFAULT NULL,
  `net_weight` double DEFAULT NULL,
  `gross_weight` double DEFAULT NULL,
  `tag_weight` double DEFAULT NULL,
  `cover_weight` double DEFAULT NULL,
  `loop_weight` double DEFAULT NULL,
  `other_weight` double DEFAULT NULL,
  `pieces` int DEFAULT NULL,
  `total_pieces` int DEFAULT NULL,
  `rate` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `wastage_percentage` double DEFAULT NULL,
  `flat_wastage` double DEFAULT NULL,
  `making_charge` double DEFAULT NULL,
  `flat_making_charge` double DEFAULT NULL,
  `tax_percent` double DEFAULT NULL,
  `additional_charges` double DEFAULT NULL,
  `total_stone_weight` double DEFAULT NULL,
  `total_diamond_weight` double DEFAULT NULL,
  `gst` double DEFAULT NULL,
  `total_rate` double DEFAULT NULL,
  `without_gst_rate` double DEFAULT NULL,
  `huid_rate` double DEFAULT NULL,
  `billing_details_id` bigint NOT NULL,
  `calculation_type_id` bigint NOT NULL,
  `item_details_id` bigint NOT NULL,
  `making_charge_calculation_type_id` bigint DEFAULT NULL,
  `metal_id` bigint NOT NULL,
  `per_gram_weight_type_id` bigint DEFAULT NULL,
  `return_bill_details_id` bigint NOT NULL,
  `return_items_id` bigint NOT NULL,
  `stock_type_id` bigint NOT NULL,
  `sub_item_details_id` bigint NOT NULL,
  `wastage_calculation_type_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `billing_sale_return_billing_details_id_bd320c15_fk_billing_d` (`billing_details_id`),
  KEY `billing_sale_return_calculation_type_id_972c109d_fk_calculati` (`calculation_type_id`),
  KEY `billing_sale_return_item_details_id_1ec296bf_fk_item_detail_id` (`item_details_id`),
  KEY `billing_sale_return_making_charge_calcul_29b13ada_fk_weight_ty` (`making_charge_calculation_type_id`),
  KEY `billing_sale_return_metal_id_a4101a7a_fk_metals_id` (`metal_id`),
  KEY `billing_sale_return_per_gram_weight_type_eb15c29c_fk_weight_ty` (`per_gram_weight_type_id`),
  KEY `billing_sale_return_return_bill_details__e8f6c651_fk_billing_d` (`return_bill_details_id`),
  KEY `billing_sale_return_return_items_id_3d51563b_fk_billing_t` (`return_items_id`),
  KEY `billing_sale_return_stock_type_id_d68c7ab4_fk_stock_type_id` (`stock_type_id`),
  KEY `billing_sale_return_sub_item_details_id_19e95296_fk_sub_item_` (`sub_item_details_id`),
  KEY `billing_sale_return_wastage_calculation__860f7046_fk_weight_ty` (`wastage_calculation_type_id`),
  CONSTRAINT `billing_sale_return_billing_details_id_bd320c15_fk_billing_d` FOREIGN KEY (`billing_details_id`) REFERENCES `billing_detail` (`id`),
  CONSTRAINT `billing_sale_return_calculation_type_id_972c109d_fk_calculati` FOREIGN KEY (`calculation_type_id`) REFERENCES `calculation_type` (`id`),
  CONSTRAINT `billing_sale_return_item_details_id_1ec296bf_fk_item_detail_id` FOREIGN KEY (`item_details_id`) REFERENCES `item_detail` (`id`),
  CONSTRAINT `billing_sale_return_making_charge_calcul_29b13ada_fk_weight_ty` FOREIGN KEY (`making_charge_calculation_type_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `billing_sale_return_metal_id_a4101a7a_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `billing_sale_return_per_gram_weight_type_eb15c29c_fk_weight_ty` FOREIGN KEY (`per_gram_weight_type_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `billing_sale_return_return_bill_details__e8f6c651_fk_billing_d` FOREIGN KEY (`return_bill_details_id`) REFERENCES `billing_detail` (`id`),
  CONSTRAINT `billing_sale_return_return_items_id_3d51563b_fk_billing_t` FOREIGN KEY (`return_items_id`) REFERENCES `billing_tag_value` (`id`),
  CONSTRAINT `billing_sale_return_stock_type_id_d68c7ab4_fk_stock_type_id` FOREIGN KEY (`stock_type_id`) REFERENCES `stock_type` (`id`),
  CONSTRAINT `billing_sale_return_sub_item_details_id_19e95296_fk_sub_item_` FOREIGN KEY (`sub_item_details_id`) REFERENCES `sub_item_detail` (`id`),
  CONSTRAINT `billing_sale_return_wastage_calculation__860f7046_fk_weight_ty` FOREIGN KEY (`wastage_calculation_type_id`) REFERENCES `weight_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_sale_return`
--

LOCK TABLES `billing_sale_return` WRITE;
/*!40000 ALTER TABLE `billing_sale_return` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_sale_return` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_session_misc_issue_id`
--

DROP TABLE IF EXISTS `billing_session_misc_issue_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_session_misc_issue_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ses_misc_issue_id_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ses_misc_issue_id_id` (`ses_misc_issue_id_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `billing_session_misc_issue_id_user_id_74ce8413_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `billing_session_misc_ses_misc_issue_id_id_74d8a557_fk_billing_m` FOREIGN KEY (`ses_misc_issue_id_id`) REFERENCES `billing_misc_issue_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_session_misc_issue_id`
--

LOCK TABLES `billing_session_misc_issue_id` WRITE;
/*!40000 ALTER TABLE `billing_session_misc_issue_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_session_misc_issue_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_tag_value`
--

DROP TABLE IF EXISTS `billing_tag_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_tag_value` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_number` int DEFAULT NULL,
  `net_weight` double DEFAULT NULL,
  `gross_weight` double DEFAULT NULL,
  `tag_weight` double DEFAULT NULL,
  `cover_weight` double DEFAULT NULL,
  `loop_weight` double DEFAULT NULL,
  `other_weight` double DEFAULT NULL,
  `pieces` int DEFAULT NULL,
  `total_pieces` int DEFAULT NULL,
  `rate` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `huid_rate` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `wastage_percentage` double DEFAULT NULL,
  `flat_wastage` double DEFAULT NULL,
  `making_charge` double DEFAULT NULL,
  `flat_making_charge` double DEFAULT NULL,
  `tax_percent` double DEFAULT NULL,
  `additional_charges` double DEFAULT NULL,
  `total_stone_weight` double DEFAULT NULL,
  `total_diamond_weight` double DEFAULT NULL,
  `gst` double DEFAULT NULL,
  `total_rate` double DEFAULT NULL,
  `without_gst_rate` double DEFAULT NULL,
  `is_returned` tinyint(1) NOT NULL,
  `billing_details_id` bigint NOT NULL,
  `billing_tag_item_id` bigint NOT NULL,
  `calculation_type_id` bigint NOT NULL,
  `item_details_id` bigint NOT NULL,
  `making_charge_calculation_type_id` bigint DEFAULT NULL,
  `metal_id` bigint NOT NULL,
  `per_gram_weight_type_id` bigint DEFAULT NULL,
  `stock_type_id` bigint NOT NULL,
  `sub_item_details_id` bigint NOT NULL,
  `wastage_calculation_type_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `billing_tag_value_billing_details_id_ff67706e_fk_billing_d` (`billing_details_id`),
  KEY `billing_tag_value_billing_tag_item_id_51f03f8e_fk_tagged_item_id` (`billing_tag_item_id`),
  KEY `billing_tag_value_calculation_type_id_41342fd5_fk_calculati` (`calculation_type_id`),
  KEY `billing_tag_value_item_details_id_4f7f7425_fk_item_detail_id` (`item_details_id`),
  KEY `billing_tag_value_making_charge_calcul_8f25a33a_fk_weight_ty` (`making_charge_calculation_type_id`),
  KEY `billing_tag_value_metal_id_161e79c4_fk_metals_id` (`metal_id`),
  KEY `billing_tag_value_per_gram_weight_type_7813056c_fk_weight_ty` (`per_gram_weight_type_id`),
  KEY `billing_tag_value_stock_type_id_f101b953_fk_stock_type_id` (`stock_type_id`),
  KEY `billing_tag_value_sub_item_details_id_553f67c5_fk_sub_item_` (`sub_item_details_id`),
  KEY `billing_tag_value_wastage_calculation__6759eda6_fk_weight_ty` (`wastage_calculation_type_id`),
  CONSTRAINT `billing_tag_value_billing_details_id_ff67706e_fk_billing_d` FOREIGN KEY (`billing_details_id`) REFERENCES `billing_detail` (`id`),
  CONSTRAINT `billing_tag_value_billing_tag_item_id_51f03f8e_fk_tagged_item_id` FOREIGN KEY (`billing_tag_item_id`) REFERENCES `tagged_item` (`id`),
  CONSTRAINT `billing_tag_value_calculation_type_id_41342fd5_fk_calculati` FOREIGN KEY (`calculation_type_id`) REFERENCES `calculation_type` (`id`),
  CONSTRAINT `billing_tag_value_item_details_id_4f7f7425_fk_item_detail_id` FOREIGN KEY (`item_details_id`) REFERENCES `item_detail` (`id`),
  CONSTRAINT `billing_tag_value_making_charge_calcul_8f25a33a_fk_weight_ty` FOREIGN KEY (`making_charge_calculation_type_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `billing_tag_value_metal_id_161e79c4_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `billing_tag_value_per_gram_weight_type_7813056c_fk_weight_ty` FOREIGN KEY (`per_gram_weight_type_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `billing_tag_value_stock_type_id_f101b953_fk_stock_type_id` FOREIGN KEY (`stock_type_id`) REFERENCES `stock_type` (`id`),
  CONSTRAINT `billing_tag_value_sub_item_details_id_553f67c5_fk_sub_item_` FOREIGN KEY (`sub_item_details_id`) REFERENCES `sub_item_detail` (`id`),
  CONSTRAINT `billing_tag_value_wastage_calculation__6759eda6_fk_weight_ty` FOREIGN KEY (`wastage_calculation_type_id`) REFERENCES `weight_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_tag_value`
--

LOCK TABLES `billing_tag_value` WRITE;
/*!40000 ALTER TABLE `billing_tag_value` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_tag_value` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branches`
--

DROP TABLE IF EXISTS `branches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `branches` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `branch_name` varchar(100) NOT NULL,
  `branch_shortcode` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `created_by` varchar(50) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `location_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `branch_name` (`branch_name`),
  KEY `branches_location_id_1835a128_fk_locations_id` (`location_id`),
  CONSTRAINT `branches_location_id_1835a128_fk_locations_id` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branches`
--

LOCK TABLES `branches` WRITE;
/*!40000 ALTER TABLE `branches` DISABLE KEYS */;
INSERT INTO `branches` VALUES (1,'Coimbatore','CBE',1,NULL,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `branches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calculation_type`
--

DROP TABLE IF EXISTS `calculation_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calculation_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `calculation_name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `calculation_name` (`calculation_name`),
  KEY `calculation_type_created_by_id_2d9b2009_fk_users_id` (`created_by_id`),
  CONSTRAINT `calculation_type_created_by_id_2d9b2009_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calculation_type`
--

LOCK TABLES `calculation_type` WRITE;
/*!40000 ALTER TABLE `calculation_type` DISABLE KEYS */;
INSERT INTO `calculation_type` VALUES (1,'Fixed Rate',1,NULL,NULL,NULL,NULL),(2,'Weight Calculation',1,NULL,NULL,NULL,NULL),(3,'Per Gram Rate',1,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `calculation_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carat_rate_detail`
--

DROP TABLE IF EXISTS `carat_rate_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carat_rate_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `purchase_rate` double NOT NULL,
  `selling_rate` double NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `cent_group_id` bigint NOT NULL,
  `clarity_id` bigint NOT NULL,
  `color_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `cut_id` bigint NOT NULL,
  `designer_id` bigint NOT NULL,
  `shape_id` bigint NOT NULL,
  `stone_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `carat_rate_detail_cent_group_id_181c1a5a_fk_centgroup_detail_id` (`cent_group_id`),
  KEY `carat_rate_detail_clarity_id_01174196_fk_clarity_detail_id` (`clarity_id`),
  KEY `carat_rate_detail_color_id_083d1a0f_fk_color_detail_id` (`color_id`),
  KEY `carat_rate_detail_created_by_id_d1ea75af_fk_users_id` (`created_by_id`),
  KEY `carat_rate_detail_cut_id_9f8ff66b_fk_cut_detail_id` (`cut_id`),
  KEY `carat_rate_detail_designer_id_7b85ef33_fk_account_head_id` (`designer_id`),
  KEY `carat_rate_detail_shape_id_3b1825ee_fk_shape_detail_id` (`shape_id`),
  KEY `carat_rate_detail_stone_id_5ebfbe28_fk_stone_detail_id` (`stone_id`),
  CONSTRAINT `carat_rate_detail_cent_group_id_181c1a5a_fk_centgroup_detail_id` FOREIGN KEY (`cent_group_id`) REFERENCES `centgroup_detail` (`id`),
  CONSTRAINT `carat_rate_detail_clarity_id_01174196_fk_clarity_detail_id` FOREIGN KEY (`clarity_id`) REFERENCES `clarity_detail` (`id`),
  CONSTRAINT `carat_rate_detail_color_id_083d1a0f_fk_color_detail_id` FOREIGN KEY (`color_id`) REFERENCES `color_detail` (`id`),
  CONSTRAINT `carat_rate_detail_created_by_id_d1ea75af_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `carat_rate_detail_cut_id_9f8ff66b_fk_cut_detail_id` FOREIGN KEY (`cut_id`) REFERENCES `cut_detail` (`id`),
  CONSTRAINT `carat_rate_detail_designer_id_7b85ef33_fk_account_head_id` FOREIGN KEY (`designer_id`) REFERENCES `account_head` (`id`),
  CONSTRAINT `carat_rate_detail_shape_id_3b1825ee_fk_shape_detail_id` FOREIGN KEY (`shape_id`) REFERENCES `shape_detail` (`id`),
  CONSTRAINT `carat_rate_detail_stone_id_5ebfbe28_fk_stone_detail_id` FOREIGN KEY (`stone_id`) REFERENCES `stone_detail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carat_rate_detail`
--

LOCK TABLES `carat_rate_detail` WRITE;
/*!40000 ALTER TABLE `carat_rate_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `carat_rate_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `card_type`
--

DROP TABLE IF EXISTS `card_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `card_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `card_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `card_name` (`card_name`),
  KEY `card_type_created_by_id_ac9393d5_fk_users_id` (`created_by_id`),
  CONSTRAINT `card_type_created_by_id_ac9393d5_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `card_type`
--

LOCK TABLES `card_type` WRITE;
/*!40000 ALTER TABLE `card_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `card_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `centgroup_detail`
--

DROP TABLE IF EXISTS `centgroup_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `centgroup_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `centgroup_name` varchar(30) NOT NULL,
  `from_weight` double NOT NULL,
  `to_weight` double NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `centgroup_name` (`centgroup_name`),
  KEY `centgroup_detail_created_by_id_467c033b_fk_users_id` (`created_by_id`),
  CONSTRAINT `centgroup_detail_created_by_id_467c033b_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `centgroup_detail`
--

LOCK TABLES `centgroup_detail` WRITE;
/*!40000 ALTER TABLE `centgroup_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `centgroup_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clarity_detail`
--

DROP TABLE IF EXISTS `clarity_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clarity_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `clarity_name` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `clarity_name` (`clarity_name`),
  KEY `clarity_detail_created_by_id_44e5f65b_fk_users_id` (`created_by_id`),
  CONSTRAINT `clarity_detail_created_by_id_44e5f65b_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clarity_detail`
--

LOCK TABLES `clarity_detail` WRITE;
/*!40000 ALTER TABLE `clarity_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `clarity_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `color_detail`
--

DROP TABLE IF EXISTS `color_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `color_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `color_name` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `color_name` (`color_name`),
  KEY `color_detail_created_by_id_b519d30d_fk_users_id` (`created_by_id`),
  CONSTRAINT `color_detail_created_by_id_b519d30d_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `color_detail`
--

LOCK TABLES `color_detail` WRITE;
/*!40000 ALTER TABLE `color_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `color_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `common_payment`
--

DROP TABLE IF EXISTS `common_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `common_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `refference_number` varchar(100) NOT NULL,
  `total_amount` double DEFAULT NULL,
  `discount_percentage` double DEFAULT NULL,
  `discount_amount` double DEFAULT NULL,
  `igst_percentage` double DEFAULT NULL,
  `igst_amount` double DEFAULT NULL,
  `sgst_percentage` double DEFAULT NULL,
  `sgst_amount` double DEFAULT NULL,
  `cgst_percentage` double DEFAULT NULL,
  `cgst_amount` double DEFAULT NULL,
  `others` double DEFAULT NULL,
  `hall_mark_charges` double DEFAULT NULL,
  `making_charge_per_gram` double DEFAULT NULL,
  `flat_making_charge` double DEFAULT NULL,
  `stone_amount` double DEFAULT NULL,
  `diamond_amount` double DEFAULT NULL,
  `payable_amount` double DEFAULT NULL,
  `salereturn_amount` double NOT NULL,
  `exchange_amount` double NOT NULL,
  `advance_amount` double DEFAULT NULL,
  `balance_amount` double DEFAULT NULL,
  `amount_received` double DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `gst_type_id` bigint NOT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `refference_number` (`refference_number`),
  KEY `common_payment_created_by_id_5392d0e6_fk_users_id` (`created_by_id`),
  KEY `common_payment_gst_type_id_b691f7ba_fk_gst_type_id` (`gst_type_id`),
  KEY `common_payment_modified_by_id_3648e7d9_fk_users_id` (`modified_by_id`),
  CONSTRAINT `common_payment_created_by_id_5392d0e6_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `common_payment_gst_type_id_b691f7ba_fk_gst_type_id` FOREIGN KEY (`gst_type_id`) REFERENCES `gst_type` (`id`),
  CONSTRAINT `common_payment_modified_by_id_3648e7d9_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `common_payment`
--

LOCK TABLES `common_payment` WRITE;
/*!40000 ALTER TABLE `common_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `common_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company_address_details`
--

DROP TABLE IF EXISTS `company_address_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_address_details` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `door_no` varchar(10) DEFAULT NULL,
  `street_name` varchar(50) DEFAULT NULL,
  `area` varchar(100) DEFAULT NULL,
  `taluk` varchar(100) DEFAULT NULL,
  `postal` varchar(100) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `pincode` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `company_details_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `company_address_deta_company_details_id_45ca9f33_fk_company_d` (`company_details_id`),
  KEY `company_address_details_created_by_id_aa1bb71b_fk_users_id` (`created_by_id`),
  CONSTRAINT `company_address_deta_company_details_id_45ca9f33_fk_company_d` FOREIGN KEY (`company_details_id`) REFERENCES `company_details` (`id`),
  CONSTRAINT `company_address_details_created_by_id_aa1bb71b_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_address_details`
--

LOCK TABLES `company_address_details` WRITE;
/*!40000 ALTER TABLE `company_address_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `company_address_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company_bank_details`
--

DROP TABLE IF EXISTS `company_bank_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_bank_details` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `acc_holder_name` varchar(100) DEFAULT NULL,
  `account_no` varchar(100) DEFAULT NULL,
  `ifsc_code` varchar(100) DEFAULT NULL,
  `bank_name` varchar(100) DEFAULT NULL,
  `branch_name` varchar(100) DEFAULT NULL,
  `micr_code` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `company_details_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `company_bank_details_company_details_id_4ee994c4_fk_company_d` (`company_details_id`),
  KEY `company_bank_details_created_by_id_9e0336ac_fk_users_id` (`created_by_id`),
  CONSTRAINT `company_bank_details_company_details_id_4ee994c4_fk_company_d` FOREIGN KEY (`company_details_id`) REFERENCES `company_details` (`id`),
  CONSTRAINT `company_bank_details_created_by_id_9e0336ac_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_bank_details`
--

LOCK TABLES `company_bank_details` WRITE;
/*!40000 ALTER TABLE `company_bank_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `company_bank_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company_details`
--

DROP TABLE IF EXISTS `company_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_details` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_name` varchar(100) NOT NULL,
  `mobile_no` varchar(10) NOT NULL,
  `email_id` varchar(100) NOT NULL,
  `website` varchar(100) DEFAULT NULL,
  `std_code` varchar(10) DEFAULT NULL,
  `landline_no` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `company_details_created_by_id_ffe6d3bd_fk_users_id` (`created_by_id`),
  CONSTRAINT `company_details_created_by_id_ffe6d3bd_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_details`
--

LOCK TABLES `company_details` WRITE;
/*!40000 ALTER TABLE `company_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `company_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company_gst_details`
--

DROP TABLE IF EXISTS `company_gst_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_gst_details` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pan_no` varchar(50) DEFAULT NULL,
  `gst_no` varchar(100) DEFAULT NULL,
  `registered_name` varchar(100) DEFAULT NULL,
  `gst_status` varchar(100) DEFAULT NULL,
  `tax_payer_type` varchar(100) DEFAULT NULL,
  `bussiness_type` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `company_details_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `company_gst_details_company_details_id_edc981dc_fk_company_d` (`company_details_id`),
  KEY `company_gst_details_created_by_id_b93852ec_fk_users_id` (`created_by_id`),
  CONSTRAINT `company_gst_details_company_details_id_edc981dc_fk_company_d` FOREIGN KEY (`company_details_id`) REFERENCES `company_details` (`id`),
  CONSTRAINT `company_gst_details_created_by_id_b93852ec_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_gst_details`
--

LOCK TABLES `company_gst_details` WRITE;
/*!40000 ALTER TABLE `company_gst_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `company_gst_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `counter_target`
--

DROP TABLE IF EXISTS `counter_target`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `counter_target` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `target_from_date` date DEFAULT NULL,
  `target_to_date` date DEFAULT NULL,
  `target_pieces` int NOT NULL,
  `target_weight` double NOT NULL,
  `target_amount` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `branch_id` bigint DEFAULT NULL,
  `counter_details_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `counter_target_branch_id_9e5f88ac_fk_branches_id` (`branch_id`),
  KEY `counter_target_counter_details_id_587a975c_fk_counters_id` (`counter_details_id`),
  KEY `counter_target_created_by_id_07466db0_fk_users_id` (`created_by_id`),
  CONSTRAINT `counter_target_branch_id_9e5f88ac_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `counter_target_counter_details_id_587a975c_fk_counters_id` FOREIGN KEY (`counter_details_id`) REFERENCES `counters` (`id`),
  CONSTRAINT `counter_target_created_by_id_07466db0_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `counter_target`
--

LOCK TABLES `counter_target` WRITE;
/*!40000 ALTER TABLE `counter_target` DISABLE KEYS */;
/*!40000 ALTER TABLE `counter_target` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `counters`
--

DROP TABLE IF EXISTS `counters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `counters` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `counter_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `branch_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `floor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `counters_floor_id_b867ab2f_fk_floors_id` (`floor_id`),
  KEY `counters_branch_id_2c943d79_fk_branches_id` (`branch_id`),
  KEY `counters_created_by_id_588a1d7a_fk_users_id` (`created_by_id`),
  CONSTRAINT `counters_branch_id_2c943d79_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `counters_created_by_id_588a1d7a_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `counters_floor_id_b867ab2f_fk_floors_id` FOREIGN KEY (`floor_id`) REFERENCES `floors` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `counters`
--

LOCK TABLES `counters` WRITE;
/*!40000 ALTER TABLE `counters` DISABLE KEYS */;
/*!40000 ALTER TABLE `counters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_details`
--

DROP TABLE IF EXISTS `customer_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_details` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(100) NOT NULL,
  `email` varchar(60) DEFAULT NULL,
  `phone` varchar(10) NOT NULL,
  `door_no` varchar(10) DEFAULT NULL,
  `street_name` varchar(50) DEFAULT NULL,
  `area` varchar(100) DEFAULT NULL,
  `taluk` varchar(100) DEFAULT NULL,
  `postal` varchar(100) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `pincode` varchar(50) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `aadhar_card` varchar(500) DEFAULT NULL,
  `pan_card` varchar(500) DEFAULT NULL,
  `gst_no` varchar(500) DEFAULT NULL,
  `is_married` tinyint(1) NOT NULL,
  `marriage_date` date DEFAULT NULL,
  `upi_id` varchar(150) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `branch_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `customer_group_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`),
  KEY `customer_details_branch_id_5fc33f4b_fk_branches_id` (`branch_id`),
  KEY `customer_details_created_by_id_e4a983ca_fk_users_id` (`created_by_id`),
  KEY `customer_details_customer_group_id_3c69b279_fk_customer_` (`customer_group_id`),
  CONSTRAINT `customer_details_branch_id_5fc33f4b_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `customer_details_created_by_id_e4a983ca_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `customer_details_customer_group_id_3c69b279_fk_customer_` FOREIGN KEY (`customer_group_id`) REFERENCES `customer_groups` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_details`
--

LOCK TABLES `customer_details` WRITE;
/*!40000 ALTER TABLE `customer_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_groups`
--

DROP TABLE IF EXISTS `customer_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customer_group_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customer_group_name` (`customer_group_name`),
  KEY `customer_groups_created_by_id_895da475_fk_users_id` (`created_by_id`),
  CONSTRAINT `customer_groups_created_by_id_895da475_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_groups`
--

LOCK TABLES `customer_groups` WRITE;
/*!40000 ALTER TABLE `customer_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_types`
--

DROP TABLE IF EXISTS `customer_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customer_type_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_types`
--

LOCK TABLES `customer_types` WRITE;
/*!40000 ALTER TABLE `customer_types` DISABLE KEYS */;
INSERT INTO `customer_types` VALUES (1,'Customer'),(2,'Retailer'),(3,'Smith'),(4,'Designer'),(5,'Vip Customer'),(6,'Vip Retailer');
/*!40000 ALTER TABLE `customer_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cut_detail`
--

DROP TABLE IF EXISTS `cut_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cut_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cut_name` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cut_name` (`cut_name`),
  KEY `cut_detail_created_by_id_c6ea79a4_fk_users_id` (`created_by_id`),
  CONSTRAINT `cut_detail_created_by_id_c6ea79a4_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cut_detail`
--

LOCK TABLES `cut_detail` WRITE;
/*!40000 ALTER TABLE `cut_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `cut_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `delivery_bill`
--

DROP TABLE IF EXISTS `delivery_bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delivery_bill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `delivery_note_id` varchar(50) NOT NULL,
  `customer_mobile` varchar(10) DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `total_stone_rate` double DEFAULT NULL,
  `total_diamond_rate` double DEFAULT NULL,
  `estimate_repair_charge` double DEFAULT NULL,
  `working_charge` double DEFAULT NULL,
  `added_weight_amount` double DEFAULT NULL,
  `less_weight_amount` double DEFAULT NULL,
  `advance_amount` double DEFAULT NULL,
  `grand_total` double DEFAULT NULL,
  `balance_amount` double DEFAULT NULL,
  `cash` double DEFAULT NULL,
  `upi` double DEFAULT NULL,
  `debit_card_amount` double DEFAULT NULL,
  `credit_card_amount` double DEFAULT NULL,
  `account_transfer` double DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `customer_details_id` bigint NOT NULL,
  `repair_details_id_id` bigint NOT NULL,
  `status_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `delivery_note_id` (`delivery_note_id`),
  KEY `delivery_bill_created_by_id_7373246f_fk_users_id` (`created_by_id`),
  KEY `delivery_bill_customer_details_id_f6c53c5c_fk_customer_` (`customer_details_id`),
  KEY `delivery_bill_repair_details_id_id_be02c1ad_fk_repair_detail_id` (`repair_details_id_id`),
  KEY `delivery_bill_status_id_62adbe08_fk_status_table_id` (`status_id`),
  CONSTRAINT `delivery_bill_created_by_id_7373246f_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `delivery_bill_customer_details_id_f6c53c5c_fk_customer_` FOREIGN KEY (`customer_details_id`) REFERENCES `customer_details` (`id`),
  CONSTRAINT `delivery_bill_repair_details_id_id_be02c1ad_fk_repair_detail_id` FOREIGN KEY (`repair_details_id_id`) REFERENCES `repair_detail` (`id`),
  CONSTRAINT `delivery_bill_status_id_62adbe08_fk_status_table_id` FOREIGN KEY (`status_id`) REFERENCES `status_table` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delivery_bill`
--

LOCK TABLES `delivery_bill` WRITE;
/*!40000 ALTER TABLE `delivery_bill` DISABLE KEYS */;
/*!40000 ALTER TABLE `delivery_bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `department_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `department_name` (`department_name`),
  KEY `departments_created_by_id_86cf2aef_fk_users_id` (`created_by_id`),
  CONSTRAINT `departments_created_by_id_86cf2aef_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'Sales',1,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `designations`
--

DROP TABLE IF EXISTS `designations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `designations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `designation_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `designation_name` (`designation_name`),
  KEY `designations_created_by_id_499de0c4_fk_users_id` (`created_by_id`),
  CONSTRAINT `designations_created_by_id_499de0c4_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `designations`
--

LOCK TABLES `designations` WRITE;
/*!40000 ALTER TABLE `designations` DISABLE KEYS */;
INSERT INTO `designations` VALUES (1,'Sales manager',1,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `designations` ENABLE KEYS */;
UNLOCK TABLES;

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
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-07-03 05:48:48.068014','1','Super Admin',1,'[{\"added\": {}}]',21,1),(2,'2024-07-03 05:49:26.495437','1','802c09f1698fe051381693f33dc6bfdac35c4ede',1,'[{\"added\": {}}]',7,1),(3,'2024-07-03 05:49:49.522640','1','admin@atts.in',2,'[{\"changed\": {\"fields\": [\"Created at\", \"Created By\", \"User Role\", \"User Branch\"]}}]',23,1),(4,'2024-07-03 06:14:08.831797','1','menu permission',1,'[{\"added\": {}}]',15,1),(5,'2024-07-03 06:14:13.562554','1','menu permission',2,'[{\"changed\": {\"fields\": [\"Add\", \"Edit\", \"Delete\"]}}]',15,1),(6,'2024-07-03 06:17:30.191060','2','menu permission',2,'[{\"changed\": {\"fields\": [\"Menu path\"]}}]',9,1),(7,'2024-07-03 06:17:30.201129','1','user role',2,'[{\"changed\": {\"fields\": [\"Menu path\"]}}]',9,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=207 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (22,'accounts','branch'),(20,'accounts','location'),(23,'accounts','user'),(21,'accounts','userrole'),(1,'admin','logentry'),(130,'advance_payment','advancepayment'),(129,'advance_payment','advancepurpose'),(140,'approval','approvalrule'),(139,'approval','approvaltype'),(3,'auth','group'),(2,'auth','permission'),(6,'authtoken','token'),(7,'authtoken','tokenproxy'),(95,'billing','billid'),(96,'billing','billingdetails'),(124,'billing','billingdiamonddetails'),(123,'billing','billingoldgold'),(122,'billing','billingreturndiamonddetails'),(121,'billing','billingreturnstonedetails'),(120,'billing','billingsalereturnitems'),(119,'billing','billingstonedetails'),(97,'billing','billingtagitems'),(98,'billing','billingtype'),(118,'billing','billnumber'),(99,'billing','estimatedetails'),(117,'billing','estimationapproval'),(116,'billing','estimationdiamonddetails'),(115,'billing','estimationoldgold'),(114,'billing','estimationreturndiamonddetails'),(113,'billing','estimationreturnstonedetails'),(112,'billing','estimationsalereturnitems'),(111,'billing','estimationstonedetails'),(110,'billing','estimationtagitems'),(100,'billing','goldestimationid'),(109,'billing','goldestimationnumber'),(101,'billing','miscissuedetails'),(102,'billing','miscissueid'),(108,'billing','miscparticulars'),(107,'billing','sessionmiscissueid'),(103,'billing','silverbillid'),(106,'billing','silverbillnumber'),(104,'billing','silverestimationid'),(105,'billing','silverestimationnumber'),(174,'billing_backup','backupbillid'),(182,'billing_backup','backupbillnumber'),(175,'billing_backup','backupbillsilverbillid'),(181,'billing_backup','backupbillsilvernumber'),(176,'billing_backup','billingbackupdetails'),(180,'billing_backup','billingbackupdiamonddetails'),(179,'billing_backup','billingbackupoldgold'),(178,'billing_backup','billingbackupstonedetails'),(177,'billing_backup','billingbackuptagitems'),(51,'books','accountgroup'),(64,'books','accountheadaddress'),(63,'books','accountheadbankdetails'),(62,'books','accountheadcontact'),(52,'books','accountheaddetails'),(61,'books','accountheadgstdetails'),(53,'books','accounttype'),(60,'books','companyaddressdetails'),(59,'books','companybankdetails'),(54,'books','companydetails'),(58,'books','companygstdetails'),(55,'books','customertype'),(56,'books','groupledger'),(57,'books','grouptype'),(4,'contenttypes','contenttype'),(128,'customer','customer'),(127,'customer','customergroup'),(27,'infrastructure','counter'),(29,'infrastructure','countertarget'),(28,'infrastructure','floor'),(50,'masters','caratrate'),(49,'masters','cardtype'),(48,'masters','centgroup'),(47,'masters','claritydetails'),(46,'masters','colordetails'),(45,'masters','cutdetails'),(44,'masters','giftvoucher'),(43,'masters','gsttype'),(30,'masters','metal'),(42,'masters','metaloldrate'),(41,'masters','metalrate'),(40,'masters','purchasetaxdetails'),(39,'masters','purity'),(38,'masters','repairtype'),(37,'masters','salestaxdetails'),(36,'masters','shapedetails'),(35,'masters','stonedetails'),(34,'masters','tagtypes'),(31,'masters','taxdetails'),(33,'masters','taxdetailsaudit'),(32,'masters','vouchertype'),(138,'order_management','orderdetails'),(137,'order_management','orderfor'),(131,'order_management','orderid'),(136,'order_management','orderissue'),(132,'order_management','orderitemattachments'),(135,'order_management','orderitemdetails'),(134,'order_management','priority'),(133,'order_management','sessionorderid'),(24,'organizations','department'),(25,'organizations','designation'),(26,'organizations','staff'),(206,'payment_management','commonpaymentdetails'),(205,'payment_management','customerpaymenttabel'),(202,'payment_management','paymentmenthod'),(203,'payment_management','paymentmodule'),(204,'payment_management','paymentproviders'),(65,'product','calculationtype'),(80,'product','fixedrate'),(66,'product','item'),(67,'product','itemid'),(79,'product','measurement'),(68,'product','measurementtype'),(78,'product','pergramrate'),(77,'product','rangestock'),(69,'product','stocktype'),(70,'product','subitem'),(76,'product','subitemfixedrate'),(71,'product','subitemid'),(75,'product','subitempergramrate'),(74,'product','subitemweightcalculation'),(73,'product','weightcalculation'),(72,'product','weighttype'),(166,'purchase','amountsettle'),(165,'purchase','cashratecut'),(164,'purchase','metalratecut'),(153,'purchase','newpurchase'),(163,'purchase','newpurchasediamonddetails'),(154,'purchase','newpurchaseitemdetail'),(162,'purchase','newpurchasestonedetails'),(161,'purchase','purchasediamonddetails'),(155,'purchase','purchaseentry'),(156,'purchase','purchaseitemdetail'),(160,'purchase','purchasepayment'),(159,'purchase','purchasepersontype'),(158,'purchase','purchasestonedetails'),(157,'purchase','purchasetype'),(183,'refinery_management','bagid'),(201,'refinery_management','bagnumber'),(184,'refinery_management','meltingissue'),(185,'refinery_management','meltingissueid'),(200,'refinery_management','meltingissuenumber'),(186,'refinery_management','meltingrecipt'),(187,'refinery_management','meltingreciptid'),(199,'refinery_management','meltingreciptnumber'),(188,'refinery_management','oldgoldtype'),(189,'refinery_management','oldmetalcategory'),(190,'refinery_management','purificationissue'),(191,'refinery_management','purificationissueid'),(198,'refinery_management','purificationissuenumber'),(197,'refinery_management','purificationrecipt'),(192,'refinery_management','purificationreciptid'),(196,'refinery_management','purificationreciptnumber'),(193,'refinery_management','transfercreation'),(195,'refinery_management','transfercreationitems'),(194,'refinery_management','transfercreationtype'),(173,'repair_management','deliverybill'),(167,'repair_management','repairdetails'),(172,'repair_management','repairfor'),(171,'repair_management','repairitemdetails'),(170,'repair_management','repairorderissued'),(169,'repair_management','repairordernumber'),(168,'repair_management','repairorderoldgold'),(5,'sessions','session'),(19,'settings','gender'),(18,'settings','incentivepercent'),(17,'settings','incentivetype'),(8,'settings','mainmenugroup'),(9,'settings','menu'),(16,'settings','menugroup'),(15,'settings','menupermission'),(10,'settings','paymentmode'),(11,'settings','paymentstatus'),(14,'settings','printmodule'),(13,'settings','salereturnpolicy'),(12,'settings','statustable'),(141,'stock','approvalissue'),(142,'stock','approvalissueid'),(152,'stock','approvalissuenumber'),(151,'stock','approvalissuetagitems'),(143,'stock','receiveditem'),(150,'stock','receiveditemdetails'),(144,'stock','returnitem'),(149,'stock','returnitemdetails'),(145,'stock','transferitem'),(148,'stock','transferitemdetails'),(147,'stock','transferstatus'),(146,'stock','transfertype'),(94,'tagging','duplicatetag'),(81,'tagging','entrytype'),(82,'tagging','lot'),(83,'tagging','lotid'),(84,'tagging','lotitem'),(85,'tagging','lotitemdiamond'),(86,'tagging','lotitemstone'),(87,'tagging','ratetype'),(88,'tagging','stoneweighttype'),(89,'tagging','tagentry'),(93,'tagging','taggeditemdiamond'),(90,'tagging','taggeditems'),(92,'tagging','taggeditemstone'),(91,'tagging','tagnumber'),(126,'value_addition','valueadditioncustomer'),(125,'value_addition','valueadditiondesigner');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'accounts','0001_initial','2024-07-03 05:47:01.727911'),(2,'contenttypes','0001_initial','2024-07-03 05:47:01.761029'),(3,'admin','0001_initial','2024-07-03 05:47:01.895763'),(4,'admin','0002_logentry_remove_auto_add','2024-07-03 05:47:01.901774'),(5,'admin','0003_logentry_add_action_flag_choices','2024-07-03 05:47:01.906960'),(6,'customer','0001_initial','2024-07-03 05:47:02.220632'),(7,'advance_payment','0001_initial','2024-07-03 05:47:02.548845'),(8,'approval','0001_initial','2024-07-03 05:47:03.056460'),(9,'contenttypes','0002_remove_content_type_name','2024-07-03 05:47:03.114776'),(10,'auth','0001_initial','2024-07-03 05:47:03.371503'),(11,'auth','0002_alter_permission_name_max_length','2024-07-03 05:47:03.450784'),(12,'auth','0003_alter_user_email_max_length','2024-07-03 05:47:03.454798'),(13,'auth','0004_alter_user_username_opts','2024-07-03 05:47:03.461796'),(14,'auth','0005_alter_user_last_login_null','2024-07-03 05:47:03.465799'),(15,'auth','0006_require_contenttypes_0002','2024-07-03 05:47:03.468258'),(16,'auth','0007_alter_validators_add_error_messages','2024-07-03 05:47:03.474043'),(17,'auth','0008_alter_user_username_max_length','2024-07-03 05:47:03.478063'),(18,'auth','0009_alter_user_last_name_max_length','2024-07-03 05:47:03.481584'),(19,'auth','0010_alter_group_name_max_length','2024-07-03 05:47:03.495089'),(20,'auth','0011_update_proxy_permissions','2024-07-03 05:47:03.504095'),(21,'auth','0012_alter_user_first_name_max_length','2024-07-03 05:47:03.509089'),(22,'authtoken','0001_initial','2024-07-03 05:47:03.598888'),(23,'authtoken','0002_auto_20160226_1747','2024-07-03 05:47:03.619515'),(24,'authtoken','0003_tokenproxy','2024-07-03 05:47:03.623303'),(25,'settings','0001_initial','2024-07-03 05:47:05.039549'),(26,'books','0001_initial','2024-07-03 05:47:06.665861'),(27,'masters','0001_initial','2024-07-03 05:47:09.482653'),(28,'infrastructure','0001_initial','2024-07-03 05:47:10.124817'),(29,'product','0001_initial','2024-07-03 05:47:14.213365'),(30,'tagging','0001_initial','2024-07-03 05:47:18.544931'),(31,'billing','0001_initial','2024-07-03 05:47:28.165592'),(32,'billing_backup','0001_initial','2024-07-03 05:47:31.260625'),(33,'order_management','0001_initial','2024-07-03 05:47:34.064100'),(34,'organizations','0001_initial','2024-07-03 05:47:34.905248'),(35,'payment_management','0001_initial','2024-07-03 05:47:35.710925'),(36,'purchase','0001_initial','2024-07-03 05:47:40.602894'),(37,'refinery_management','0001_initial','2024-07-03 05:47:45.005266'),(38,'repair_management','0001_initial','2024-07-03 05:47:47.623709'),(39,'sessions','0001_initial','2024-07-03 05:47:47.655276'),(40,'stock','0001_initial','2024-07-03 05:47:52.165775'),(41,'value_addition','0001_initial','2024-07-03 05:47:53.174096');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('xahskqxo1zrkmasn2j2xmicq1fetp2cc','.eJxVjDkOwjAQAP_iGlne-KakzxusXR84gBwpTirE35GlFNDOjObNAh57DUfPW1gSuzJgl19GGJ-5DZEe2O4rj2vbt4X4SPhpO5_XlF-3s_0bVOx1bAWh1GTQeJUiOQlKFbSUCvlsFVFRVljnrQTQ2oE0MBky1kUnJwGRfb7fyjcQ:1sOsr3:hq3YaFejci7bCd16sHck-0q1-I5eWCQPcYiVEG4Km7k','2024-07-17 05:48:33.819113');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `duplicate_tag`
--

DROP TABLE IF EXISTS `duplicate_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `duplicate_tag` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `number_copies` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` bigint NOT NULL,
  `tag_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `duplicate_tag_created_by_id_103ded20_fk_users_id` (`created_by_id`),
  KEY `duplicate_tag_tag_details_id_cc923ccf_fk_tagged_item_id` (`tag_details_id`),
  CONSTRAINT `duplicate_tag_created_by_id_103ded20_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `duplicate_tag_tag_details_id_cc923ccf_fk_tagged_item_id` FOREIGN KEY (`tag_details_id`) REFERENCES `tagged_item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `duplicate_tag`
--

LOCK TABLES `duplicate_tag` WRITE;
/*!40000 ALTER TABLE `duplicate_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `duplicate_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entry_type`
--

DROP TABLE IF EXISTS `entry_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entry_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `entry_name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `entry_name` (`entry_name`),
  KEY `entry_type_created_by_id_33eb210b_fk_users_id` (`created_by_id`),
  CONSTRAINT `entry_type_created_by_id_33eb210b_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entry_type`
--

LOCK TABLES `entry_type` WRITE;
/*!40000 ALTER TABLE `entry_type` DISABLE KEYS */;
INSERT INTO `entry_type` VALUES (1,'Regular',1,NULL,NULL,NULL,NULL),(2,'Order',1,NULL,NULL,NULL,NULL),(3,'Repair',1,NULL,NULL,NULL,NULL),(4,'Sale Return',1,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `entry_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estimation_approval`
--

DROP TABLE IF EXISTS `estimation_approval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estimation_approval` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `approved_at` datetime(6) DEFAULT NULL,
  `approved_by_id` bigint NOT NULL,
  `estimation_details_id` bigint NOT NULL,
  `estimation_status_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `estimation_approval_approved_by_id_47dbc871_fk_users_id` (`approved_by_id`),
  KEY `estimation_approval_estimation_details_i_62271859_fk_estimatio` (`estimation_details_id`),
  KEY `estimation_approval_estimation_status_id_c6ed3b02_fk_status_ta` (`estimation_status_id`),
  CONSTRAINT `estimation_approval_approved_by_id_47dbc871_fk_users_id` FOREIGN KEY (`approved_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `estimation_approval_estimation_details_i_62271859_fk_estimatio` FOREIGN KEY (`estimation_details_id`) REFERENCES `estimation_detail` (`id`),
  CONSTRAINT `estimation_approval_estimation_status_id_c6ed3b02_fk_status_ta` FOREIGN KEY (`estimation_status_id`) REFERENCES `status_table` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estimation_approval`
--

LOCK TABLES `estimation_approval` WRITE;
/*!40000 ALTER TABLE `estimation_approval` DISABLE KEYS */;
/*!40000 ALTER TABLE `estimation_approval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estimation_detail`
--

DROP TABLE IF EXISTS `estimation_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estimation_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `estimate_no` varchar(100) NOT NULL,
  `estimation_date` datetime(6) NOT NULL,
  `total_amount` double NOT NULL,
  `discount_percentage` double NOT NULL,
  `discount_amount` double NOT NULL,
  `stone_amount` double NOT NULL,
  `diamond_amount` double NOT NULL,
  `chit_amount` double DEFAULT NULL,
  `salereturn_amount` double NOT NULL,
  `exchange_amount` double NOT NULL,
  `gst_percentage` double NOT NULL,
  `gst_amount` double NOT NULL,
  `payable_amount` double DEFAULT NULL,
  `advance_amount` double DEFAULT NULL,
  `balance_amount` double DEFAULT NULL,
  `is_billed` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `bill_type_id` bigint DEFAULT NULL,
  `branch_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `customer_details_id` bigint NOT NULL,
  `gst_type_id` bigint DEFAULT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `estimate_no` (`estimate_no`),
  KEY `estimation_detail_bill_type_id_2883f526_fk_bill_type_id` (`bill_type_id`),
  KEY `estimation_detail_branch_id_2aab24c8_fk_branches_id` (`branch_id`),
  KEY `estimation_detail_created_by_id_4e500e86_fk_users_id` (`created_by_id`),
  KEY `estimation_detail_customer_details_id_2e1f09ac_fk_customer_` (`customer_details_id`),
  KEY `estimation_detail_gst_type_id_7eb92d74_fk_gst_type_id` (`gst_type_id`),
  KEY `estimation_detail_modified_by_id_62492b88_fk_users_id` (`modified_by_id`),
  CONSTRAINT `estimation_detail_bill_type_id_2883f526_fk_bill_type_id` FOREIGN KEY (`bill_type_id`) REFERENCES `bill_type` (`id`),
  CONSTRAINT `estimation_detail_branch_id_2aab24c8_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `estimation_detail_created_by_id_4e500e86_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `estimation_detail_customer_details_id_2e1f09ac_fk_customer_` FOREIGN KEY (`customer_details_id`) REFERENCES `customer_details` (`id`),
  CONSTRAINT `estimation_detail_gst_type_id_7eb92d74_fk_gst_type_id` FOREIGN KEY (`gst_type_id`) REFERENCES `gst_type` (`id`),
  CONSTRAINT `estimation_detail_modified_by_id_62492b88_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estimation_detail`
--

LOCK TABLES `estimation_detail` WRITE;
/*!40000 ALTER TABLE `estimation_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `estimation_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estimation_item_diamond`
--

DROP TABLE IF EXISTS `estimation_item_diamond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estimation_item_diamond` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `diamond_pieces` int DEFAULT NULL,
  `diamond_weight` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `include_diamond_weight` tinyint(1) NOT NULL,
  `total_diamond_value` double DEFAULT NULL,
  `diamond_name_id` bigint NOT NULL,
  `diamond_rate_type_id` bigint NOT NULL,
  `diamond_weight_type_id` bigint NOT NULL,
  `estimation_details_id` bigint NOT NULL,
  `estimation_item_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `estimation_item_diam_diamond_name_id_eb8ddf1a_fk_stone_det` (`diamond_name_id`),
  KEY `estimation_item_diam_diamond_rate_type_id_d2df4090_fk_rate_type` (`diamond_rate_type_id`),
  KEY `estimation_item_diam_diamond_weight_type__1cb3c024_fk_stone_wei` (`diamond_weight_type_id`),
  KEY `estimation_item_diam_estimation_details_i_7a14db23_fk_estimatio` (`estimation_details_id`),
  KEY `estimation_item_diam_estimation_item_deta_485d5d3a_fk_estimatio` (`estimation_item_details_id`),
  CONSTRAINT `estimation_item_diam_diamond_name_id_eb8ddf1a_fk_stone_det` FOREIGN KEY (`diamond_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `estimation_item_diam_diamond_rate_type_id_d2df4090_fk_rate_type` FOREIGN KEY (`diamond_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `estimation_item_diam_diamond_weight_type__1cb3c024_fk_stone_wei` FOREIGN KEY (`diamond_weight_type_id`) REFERENCES `stone_weight_type` (`id`),
  CONSTRAINT `estimation_item_diam_estimation_details_i_7a14db23_fk_estimatio` FOREIGN KEY (`estimation_details_id`) REFERENCES `estimation_detail` (`id`),
  CONSTRAINT `estimation_item_diam_estimation_item_deta_485d5d3a_fk_estimatio` FOREIGN KEY (`estimation_item_details_id`) REFERENCES `estimation_tag_value` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estimation_item_diamond`
--

LOCK TABLES `estimation_item_diamond` WRITE;
/*!40000 ALTER TABLE `estimation_item_diamond` DISABLE KEYS */;
/*!40000 ALTER TABLE `estimation_item_diamond` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estimation_item_stone`
--

DROP TABLE IF EXISTS `estimation_item_stone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estimation_item_stone` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stone_pieces` int DEFAULT NULL,
  `stone_weight` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `include_stone_weight` tinyint(1) NOT NULL,
  `total_stone_value` double DEFAULT NULL,
  `estimation_details_id` bigint NOT NULL,
  `estimation_item_details_id` bigint NOT NULL,
  `stone_name_id` bigint NOT NULL,
  `stone_rate_type_id` bigint NOT NULL,
  `stone_weight_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `estimation_item_ston_estimation_details_i_c6b13e10_fk_estimatio` (`estimation_details_id`),
  KEY `estimation_item_ston_estimation_item_deta_62ed3843_fk_estimatio` (`estimation_item_details_id`),
  KEY `estimation_item_stone_stone_name_id_f4875a78_fk_stone_detail_id` (`stone_name_id`),
  KEY `estimation_item_ston_stone_rate_type_id_6417472c_fk_rate_type` (`stone_rate_type_id`),
  KEY `estimation_item_ston_stone_weight_type_id_b85c6bc3_fk_stone_wei` (`stone_weight_type_id`),
  CONSTRAINT `estimation_item_ston_estimation_details_i_c6b13e10_fk_estimatio` FOREIGN KEY (`estimation_details_id`) REFERENCES `estimation_detail` (`id`),
  CONSTRAINT `estimation_item_ston_estimation_item_deta_62ed3843_fk_estimatio` FOREIGN KEY (`estimation_item_details_id`) REFERENCES `estimation_tag_value` (`id`),
  CONSTRAINT `estimation_item_ston_stone_rate_type_id_6417472c_fk_rate_type` FOREIGN KEY (`stone_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `estimation_item_ston_stone_weight_type_id_b85c6bc3_fk_stone_wei` FOREIGN KEY (`stone_weight_type_id`) REFERENCES `stone_weight_type` (`id`),
  CONSTRAINT `estimation_item_stone_stone_name_id_f4875a78_fk_stone_detail_id` FOREIGN KEY (`stone_name_id`) REFERENCES `stone_detail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estimation_item_stone`
--

LOCK TABLES `estimation_item_stone` WRITE;
/*!40000 ALTER TABLE `estimation_item_stone` DISABLE KEYS */;
/*!40000 ALTER TABLE `estimation_item_stone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estimation_old_gold_value`
--

DROP TABLE IF EXISTS `estimation_old_gold_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estimation_old_gold_value` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_name` varchar(150) DEFAULT NULL,
  `old_gold_no` varchar(100) NOT NULL,
  `metal_rate` double DEFAULT NULL,
  `today_metal_rate` double DEFAULT NULL,
  `old_gross_weight` double DEFAULT NULL,
  `old_net_weight` double DEFAULT NULL,
  `dust_weight` double DEFAULT NULL,
  `old_metal_rate` double DEFAULT NULL,
  `total_old_gold_value` double DEFAULT NULL,
  `estimation_details_id` bigint NOT NULL,
  `old_metal_id` bigint NOT NULL,
  `purity_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `estimation_old_gold__estimation_details_i_0a312548_fk_estimatio` (`estimation_details_id`),
  KEY `estimation_old_gold_value_old_metal_id_4b2204ed_fk_metals_id` (`old_metal_id`),
  KEY `estimation_old_gold_value_purity_id_c8b2c89f_fk_purities_id` (`purity_id`),
  CONSTRAINT `estimation_old_gold__estimation_details_i_0a312548_fk_estimatio` FOREIGN KEY (`estimation_details_id`) REFERENCES `estimation_detail` (`id`),
  CONSTRAINT `estimation_old_gold_value_old_metal_id_4b2204ed_fk_metals_id` FOREIGN KEY (`old_metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `estimation_old_gold_value_purity_id_c8b2c89f_fk_purities_id` FOREIGN KEY (`purity_id`) REFERENCES `purities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estimation_old_gold_value`
--

LOCK TABLES `estimation_old_gold_value` WRITE;
/*!40000 ALTER TABLE `estimation_old_gold_value` DISABLE KEYS */;
/*!40000 ALTER TABLE `estimation_old_gold_value` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estimation_return_diamond`
--

DROP TABLE IF EXISTS `estimation_return_diamond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estimation_return_diamond` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `diamond_pieces` int DEFAULT NULL,
  `diamond_weight` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `include_diamond_weight` tinyint(1) NOT NULL,
  `total_diamond_value` double DEFAULT NULL,
  `diamond_name_id` bigint NOT NULL,
  `diamond_rate_type_id` bigint NOT NULL,
  `diamond_weight_type_id` bigint NOT NULL,
  `estimation_details_id` bigint NOT NULL,
  `estimation_return_item_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `estimation_return_di_diamond_name_id_b3aa6f0e_fk_stone_det` (`diamond_name_id`),
  KEY `estimation_return_di_diamond_rate_type_id_2ecfaa6c_fk_rate_type` (`diamond_rate_type_id`),
  KEY `estimation_return_di_diamond_weight_type__cafa5122_fk_stone_wei` (`diamond_weight_type_id`),
  KEY `estimation_return_di_estimation_details_i_5d624401_fk_estimatio` (`estimation_details_id`),
  KEY `estimation_return_di_estimation_return_it_6095404b_fk_estimatio` (`estimation_return_item_id`),
  CONSTRAINT `estimation_return_di_diamond_name_id_b3aa6f0e_fk_stone_det` FOREIGN KEY (`diamond_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `estimation_return_di_diamond_rate_type_id_2ecfaa6c_fk_rate_type` FOREIGN KEY (`diamond_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `estimation_return_di_diamond_weight_type__cafa5122_fk_stone_wei` FOREIGN KEY (`diamond_weight_type_id`) REFERENCES `stone_weight_type` (`id`),
  CONSTRAINT `estimation_return_di_estimation_details_i_5d624401_fk_estimatio` FOREIGN KEY (`estimation_details_id`) REFERENCES `estimation_detail` (`id`),
  CONSTRAINT `estimation_return_di_estimation_return_it_6095404b_fk_estimatio` FOREIGN KEY (`estimation_return_item_id`) REFERENCES `estimation_sale_return` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estimation_return_diamond`
--

LOCK TABLES `estimation_return_diamond` WRITE;
/*!40000 ALTER TABLE `estimation_return_diamond` DISABLE KEYS */;
/*!40000 ALTER TABLE `estimation_return_diamond` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estimation_return_stone`
--

DROP TABLE IF EXISTS `estimation_return_stone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estimation_return_stone` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stone_pieces` int DEFAULT NULL,
  `stone_weight` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `include_stone_weight` tinyint(1) NOT NULL,
  `total_stone_value` double DEFAULT NULL,
  `estimation_details_id` bigint NOT NULL,
  `estimation_return_item_id` bigint NOT NULL,
  `stone_name_id` bigint NOT NULL,
  `stone_rate_type_id` bigint NOT NULL,
  `stone_weight_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `estimation_return_st_estimation_details_i_707e03fd_fk_estimatio` (`estimation_details_id`),
  KEY `estimation_return_st_estimation_return_it_f3439b0c_fk_estimatio` (`estimation_return_item_id`),
  KEY `estimation_return_st_stone_name_id_3e0315d1_fk_stone_det` (`stone_name_id`),
  KEY `estimation_return_st_stone_rate_type_id_31926cf0_fk_rate_type` (`stone_rate_type_id`),
  KEY `estimation_return_st_stone_weight_type_id_fac9b315_fk_stone_wei` (`stone_weight_type_id`),
  CONSTRAINT `estimation_return_st_estimation_details_i_707e03fd_fk_estimatio` FOREIGN KEY (`estimation_details_id`) REFERENCES `estimation_detail` (`id`),
  CONSTRAINT `estimation_return_st_estimation_return_it_f3439b0c_fk_estimatio` FOREIGN KEY (`estimation_return_item_id`) REFERENCES `estimation_sale_return` (`id`),
  CONSTRAINT `estimation_return_st_stone_name_id_3e0315d1_fk_stone_det` FOREIGN KEY (`stone_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `estimation_return_st_stone_rate_type_id_31926cf0_fk_rate_type` FOREIGN KEY (`stone_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `estimation_return_st_stone_weight_type_id_fac9b315_fk_stone_wei` FOREIGN KEY (`stone_weight_type_id`) REFERENCES `stone_weight_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estimation_return_stone`
--

LOCK TABLES `estimation_return_stone` WRITE;
/*!40000 ALTER TABLE `estimation_return_stone` DISABLE KEYS */;
/*!40000 ALTER TABLE `estimation_return_stone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estimation_sale_return`
--

DROP TABLE IF EXISTS `estimation_sale_return`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estimation_sale_return` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_number` int DEFAULT NULL,
  `net_weight` double DEFAULT NULL,
  `gross_weight` double DEFAULT NULL,
  `tag_weight` double DEFAULT NULL,
  `cover_weight` double DEFAULT NULL,
  `loop_weight` double DEFAULT NULL,
  `other_weight` double DEFAULT NULL,
  `pieces` int DEFAULT NULL,
  `total_pieces` int DEFAULT NULL,
  `rate` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `wastage_percentage` double DEFAULT NULL,
  `flat_wastage` double DEFAULT NULL,
  `making_charge` double DEFAULT NULL,
  `flat_making_charge` double DEFAULT NULL,
  `tax_percent` double DEFAULT NULL,
  `additional_charges` double DEFAULT NULL,
  `total_stone_weight` double DEFAULT NULL,
  `total_diamond_weight` double DEFAULT NULL,
  `gst` double DEFAULT NULL,
  `total_rate` double DEFAULT NULL,
  `without_gst_rate` double DEFAULT NULL,
  `huid_rate` double DEFAULT NULL,
  `bill_details_id` bigint NOT NULL,
  `calculation_type_id` bigint NOT NULL,
  `estimation_details_id` bigint NOT NULL,
  `item_details_id` bigint NOT NULL,
  `making_charge_calculation_type_id` bigint DEFAULT NULL,
  `metal_id` bigint NOT NULL,
  `per_gram_weight_type_id` bigint DEFAULT NULL,
  `return_items_id` bigint NOT NULL,
  `stock_type_id` bigint NOT NULL,
  `sub_item_details_id` bigint NOT NULL,
  `wastage_calculation_type_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `estimation_sale_retu_bill_details_id_e41eaa15_fk_billing_d` (`bill_details_id`),
  KEY `estimation_sale_retu_calculation_type_id_4f0135cd_fk_calculati` (`calculation_type_id`),
  KEY `estimation_sale_retu_estimation_details_i_3ba6d63d_fk_estimatio` (`estimation_details_id`),
  KEY `estimation_sale_retu_item_details_id_ebaddaec_fk_item_deta` (`item_details_id`),
  KEY `estimation_sale_retu_making_charge_calcul_fc43630f_fk_weight_ty` (`making_charge_calculation_type_id`),
  KEY `estimation_sale_return_metal_id_315c2960_fk_metals_id` (`metal_id`),
  KEY `estimation_sale_retu_per_gram_weight_type_77c73f2d_fk_weight_ty` (`per_gram_weight_type_id`),
  KEY `estimation_sale_retu_return_items_id_23d3365a_fk_billing_t` (`return_items_id`),
  KEY `estimation_sale_return_stock_type_id_417442b1_fk_stock_type_id` (`stock_type_id`),
  KEY `estimation_sale_retu_sub_item_details_id_9dc6f4b0_fk_sub_item_` (`sub_item_details_id`),
  KEY `estimation_sale_retu_wastage_calculation__0280a7f2_fk_weight_ty` (`wastage_calculation_type_id`),
  CONSTRAINT `estimation_sale_retu_bill_details_id_e41eaa15_fk_billing_d` FOREIGN KEY (`bill_details_id`) REFERENCES `billing_detail` (`id`),
  CONSTRAINT `estimation_sale_retu_calculation_type_id_4f0135cd_fk_calculati` FOREIGN KEY (`calculation_type_id`) REFERENCES `calculation_type` (`id`),
  CONSTRAINT `estimation_sale_retu_estimation_details_i_3ba6d63d_fk_estimatio` FOREIGN KEY (`estimation_details_id`) REFERENCES `estimation_detail` (`id`),
  CONSTRAINT `estimation_sale_retu_item_details_id_ebaddaec_fk_item_deta` FOREIGN KEY (`item_details_id`) REFERENCES `item_detail` (`id`),
  CONSTRAINT `estimation_sale_retu_making_charge_calcul_fc43630f_fk_weight_ty` FOREIGN KEY (`making_charge_calculation_type_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `estimation_sale_retu_per_gram_weight_type_77c73f2d_fk_weight_ty` FOREIGN KEY (`per_gram_weight_type_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `estimation_sale_retu_return_items_id_23d3365a_fk_billing_t` FOREIGN KEY (`return_items_id`) REFERENCES `billing_tag_value` (`id`),
  CONSTRAINT `estimation_sale_retu_sub_item_details_id_9dc6f4b0_fk_sub_item_` FOREIGN KEY (`sub_item_details_id`) REFERENCES `sub_item_detail` (`id`),
  CONSTRAINT `estimation_sale_retu_wastage_calculation__0280a7f2_fk_weight_ty` FOREIGN KEY (`wastage_calculation_type_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `estimation_sale_return_metal_id_315c2960_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `estimation_sale_return_stock_type_id_417442b1_fk_stock_type_id` FOREIGN KEY (`stock_type_id`) REFERENCES `stock_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estimation_sale_return`
--

LOCK TABLES `estimation_sale_return` WRITE;
/*!40000 ALTER TABLE `estimation_sale_return` DISABLE KEYS */;
/*!40000 ALTER TABLE `estimation_sale_return` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estimation_tag_value`
--

DROP TABLE IF EXISTS `estimation_tag_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estimation_tag_value` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_number` int DEFAULT NULL,
  `net_weight` double DEFAULT NULL,
  `gross_weight` double DEFAULT NULL,
  `tag_weight` double DEFAULT NULL,
  `cover_weight` double DEFAULT NULL,
  `loop_weight` double DEFAULT NULL,
  `other_weight` double DEFAULT NULL,
  `pieces` int DEFAULT NULL,
  `total_pieces` int DEFAULT NULL,
  `rate` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `huid_rate` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `wastage_percentage` double DEFAULT NULL,
  `flat_wastage` double DEFAULT NULL,
  `making_charge` double DEFAULT NULL,
  `flat_making_charge` double DEFAULT NULL,
  `tax_percent` double DEFAULT NULL,
  `additional_charges` double DEFAULT NULL,
  `total_stone_weight` double DEFAULT NULL,
  `total_diamond_weight` double DEFAULT NULL,
  `gst` double DEFAULT NULL,
  `total_rate` double DEFAULT NULL,
  `without_gst_rate` double DEFAULT NULL,
  `calculation_type_id` bigint NOT NULL,
  `estimation_details_id` bigint NOT NULL,
  `estimation_tag_item_id` bigint NOT NULL,
  `item_details_id` bigint NOT NULL,
  `making_charge_calculation_type_id` bigint DEFAULT NULL,
  `metal_id` bigint NOT NULL,
  `per_gram_weight_type_id` bigint DEFAULT NULL,
  `stock_type_id` bigint NOT NULL,
  `sub_item_details_id` bigint NOT NULL,
  `wastage_calculation_type_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `estimation_tag_value_calculation_type_id_d6beb5d2_fk_calculati` (`calculation_type_id`),
  KEY `estimation_tag_value_estimation_details_i_44f4dce6_fk_estimatio` (`estimation_details_id`),
  KEY `estimation_tag_value_estimation_tag_item__623bb9dc_fk_tagged_it` (`estimation_tag_item_id`),
  KEY `estimation_tag_value_item_details_id_70a0515f_fk_item_detail_id` (`item_details_id`),
  KEY `estimation_tag_value_making_charge_calcul_ad9d168a_fk_weight_ty` (`making_charge_calculation_type_id`),
  KEY `estimation_tag_value_metal_id_587a0a37_fk_metals_id` (`metal_id`),
  KEY `estimation_tag_value_per_gram_weight_type_6af8e391_fk_weight_ty` (`per_gram_weight_type_id`),
  KEY `estimation_tag_value_stock_type_id_e4701bbc_fk_stock_type_id` (`stock_type_id`),
  KEY `estimation_tag_value_sub_item_details_id_da15a797_fk_sub_item_` (`sub_item_details_id`),
  KEY `estimation_tag_value_wastage_calculation__3d8f3366_fk_weight_ty` (`wastage_calculation_type_id`),
  CONSTRAINT `estimation_tag_value_calculation_type_id_d6beb5d2_fk_calculati` FOREIGN KEY (`calculation_type_id`) REFERENCES `calculation_type` (`id`),
  CONSTRAINT `estimation_tag_value_estimation_details_i_44f4dce6_fk_estimatio` FOREIGN KEY (`estimation_details_id`) REFERENCES `estimation_detail` (`id`),
  CONSTRAINT `estimation_tag_value_estimation_tag_item__623bb9dc_fk_tagged_it` FOREIGN KEY (`estimation_tag_item_id`) REFERENCES `tagged_item` (`id`),
  CONSTRAINT `estimation_tag_value_item_details_id_70a0515f_fk_item_detail_id` FOREIGN KEY (`item_details_id`) REFERENCES `item_detail` (`id`),
  CONSTRAINT `estimation_tag_value_making_charge_calcul_ad9d168a_fk_weight_ty` FOREIGN KEY (`making_charge_calculation_type_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `estimation_tag_value_metal_id_587a0a37_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `estimation_tag_value_per_gram_weight_type_6af8e391_fk_weight_ty` FOREIGN KEY (`per_gram_weight_type_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `estimation_tag_value_stock_type_id_e4701bbc_fk_stock_type_id` FOREIGN KEY (`stock_type_id`) REFERENCES `stock_type` (`id`),
  CONSTRAINT `estimation_tag_value_sub_item_details_id_da15a797_fk_sub_item_` FOREIGN KEY (`sub_item_details_id`) REFERENCES `sub_item_detail` (`id`),
  CONSTRAINT `estimation_tag_value_wastage_calculation__3d8f3366_fk_weight_ty` FOREIGN KEY (`wastage_calculation_type_id`) REFERENCES `weight_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estimation_tag_value`
--

LOCK TABLES `estimation_tag_value` WRITE;
/*!40000 ALTER TABLE `estimation_tag_value` DISABLE KEYS */;
/*!40000 ALTER TABLE `estimation_tag_value` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fixed_rate`
--

DROP TABLE IF EXISTS `fixed_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fixed_rate` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fixed_rate` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `item_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fixed_rate_created_by_id_64b7b330_fk_users_id` (`created_by_id`),
  KEY `fixed_rate_item_details_id_4d513775_fk_item_detail_id` (`item_details_id`),
  CONSTRAINT `fixed_rate_created_by_id_64b7b330_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `fixed_rate_item_details_id_4d513775_fk_item_detail_id` FOREIGN KEY (`item_details_id`) REFERENCES `item_detail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fixed_rate`
--

LOCK TABLES `fixed_rate` WRITE;
/*!40000 ALTER TABLE `fixed_rate` DISABLE KEYS */;
/*!40000 ALTER TABLE `fixed_rate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `floors`
--

DROP TABLE IF EXISTS `floors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `floors` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `floor_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `branch_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `floors_branch_id_db70600c_fk_branches_id` (`branch_id`),
  KEY `floors_created_by_id_7df13d70_fk_users_id` (`created_by_id`),
  CONSTRAINT `floors_branch_id_db70600c_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `floors_created_by_id_7df13d70_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `floors`
--

LOCK TABLES `floors` WRITE;
/*!40000 ALTER TABLE `floors` DISABLE KEYS */;
/*!40000 ALTER TABLE `floors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gift_voucher`
--

DROP TABLE IF EXISTS `gift_voucher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gift_voucher` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `voucher_no` varchar(100) NOT NULL,
  `cash` double NOT NULL,
  `from_date` date NOT NULL,
  `to_date` date NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_redeemed` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `voucher_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gift_voucher_created_by_id_e9dbf5f7_fk_users_id` (`created_by_id`),
  KEY `gift_voucher_voucher_type_id_9de1a88e_fk_voucher_type_id` (`voucher_type_id`),
  CONSTRAINT `gift_voucher_created_by_id_e9dbf5f7_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `gift_voucher_voucher_type_id_9de1a88e_fk_voucher_type_id` FOREIGN KEY (`voucher_type_id`) REFERENCES `voucher_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gift_voucher`
--

LOCK TABLES `gift_voucher` WRITE;
/*!40000 ALTER TABLE `gift_voucher` DISABLE KEYS */;
/*!40000 ALTER TABLE `gift_voucher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gold_estimation_id`
--

DROP TABLE IF EXISTS `gold_estimation_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gold_estimation_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `gold_estimation_id` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gold_estimation_id` (`gold_estimation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gold_estimation_id`
--

LOCK TABLES `gold_estimation_id` WRITE;
/*!40000 ALTER TABLE `gold_estimation_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `gold_estimation_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gold_estimation_number`
--

DROP TABLE IF EXISTS `gold_estimation_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gold_estimation_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `gold_estimation_number` varchar(10) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gold_estimation_number` (`gold_estimation_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `gold_estimation_number_user_id_58edabe9_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gold_estimation_number`
--

LOCK TABLES `gold_estimation_number` WRITE;
/*!40000 ALTER TABLE `gold_estimation_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `gold_estimation_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_ledgers`
--

DROP TABLE IF EXISTS `group_ledgers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group_ledgers` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_ledger_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_ledgers`
--

LOCK TABLES `group_ledgers` WRITE;
/*!40000 ALTER TABLE `group_ledgers` DISABLE KEYS */;
INSERT INTO `group_ledgers` VALUES (1,'Profit & Loss'),(2,'Balance Sheet'),(3,'Trading');
/*!40000 ALTER TABLE `group_ledgers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_types`
--

DROP TABLE IF EXISTS `group_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_type_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_types`
--

LOCK TABLES `group_types` WRITE;
/*!40000 ALTER TABLE `group_types` DISABLE KEYS */;
INSERT INTO `group_types` VALUES (1,'Assets'),(2,'Liabilities'),(3,'Income'),(4,'Expense');
/*!40000 ALTER TABLE `group_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gst_type`
--

DROP TABLE IF EXISTS `gst_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gst_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `gst_type_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gst_type_name` (`gst_type_name`),
  KEY `gst_type_created_by_id_8ae20f8a_fk_users_id` (`created_by_id`),
  CONSTRAINT `gst_type_created_by_id_8ae20f8a_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gst_type`
--

LOCK TABLES `gst_type` WRITE;
/*!40000 ALTER TABLE `gst_type` DISABLE KEYS */;
INSERT INTO `gst_type` VALUES (1,'Intra-state GST',1,NULL,NULL,NULL,1),(2,'Inter-state GST',1,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `gst_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incentive_percent`
--

DROP TABLE IF EXISTS `incentive_percent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incentive_percent` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `incentive_percent` double DEFAULT NULL,
  `incentive_amount` double DEFAULT NULL,
  `from_amount` double NOT NULL,
  `to_amount` double NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `incentive_type_id` bigint NOT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `incentive_percent_created_by_id_fe9a9e46_fk_users_id` (`created_by_id`),
  KEY `incentive_percent_incentive_type_id_3931b56a_fk_incentive` (`incentive_type_id`),
  KEY `incentive_percent_modified_by_id_41d1b8ce_fk_users_id` (`modified_by_id`),
  CONSTRAINT `incentive_percent_created_by_id_fe9a9e46_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `incentive_percent_incentive_type_id_3931b56a_fk_incentive` FOREIGN KEY (`incentive_type_id`) REFERENCES `incentive_type` (`id`),
  CONSTRAINT `incentive_percent_modified_by_id_41d1b8ce_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incentive_percent`
--

LOCK TABLES `incentive_percent` WRITE;
/*!40000 ALTER TABLE `incentive_percent` DISABLE KEYS */;
/*!40000 ALTER TABLE `incentive_percent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incentive_type`
--

DROP TABLE IF EXISTS `incentive_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incentive_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `incentive_typename` varchar(10) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `incentive_type_created_by_id_df070bb6_fk_users_id` (`created_by_id`),
  KEY `incentive_type_modified_by_id_44e34cc0_fk_users_id` (`modified_by_id`),
  CONSTRAINT `incentive_type_created_by_id_df070bb6_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `incentive_type_modified_by_id_44e34cc0_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incentive_type`
--

LOCK TABLES `incentive_type` WRITE;
/*!40000 ALTER TABLE `incentive_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `incentive_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_detail`
--

DROP TABLE IF EXISTS `item_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `hsn_code` varchar(15) NOT NULL,
  `item_id` varchar(10) NOT NULL,
  `item_code` varchar(25) NOT NULL,
  `item_name` varchar(50) NOT NULL,
  `allow_zero_weight` tinyint(1) NOT NULL,
  `item_image` varchar(250) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `huid_rate` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `calculation_type_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `item_counter_id` bigint NOT NULL,
  `metal_id` bigint NOT NULL,
  `purity_id` bigint NOT NULL,
  `stock_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_id` (`item_id`),
  UNIQUE KEY `item_code` (`item_code`),
  KEY `item_detail_stock_type_id_f13afe51_fk_stock_type_id` (`stock_type_id`),
  KEY `item_detail_calculation_type_id_538219ea_fk_calculation_type_id` (`calculation_type_id`),
  KEY `item_detail_created_by_id_b1718ddf_fk_users_id` (`created_by_id`),
  KEY `item_detail_item_counter_id_cec07bec_fk_counters_id` (`item_counter_id`),
  KEY `item_detail_metal_id_89846893_fk_metals_id` (`metal_id`),
  KEY `item_detail_purity_id_3980f05e_fk_purities_id` (`purity_id`),
  CONSTRAINT `item_detail_calculation_type_id_538219ea_fk_calculation_type_id` FOREIGN KEY (`calculation_type_id`) REFERENCES `calculation_type` (`id`),
  CONSTRAINT `item_detail_created_by_id_b1718ddf_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `item_detail_item_counter_id_cec07bec_fk_counters_id` FOREIGN KEY (`item_counter_id`) REFERENCES `counters` (`id`),
  CONSTRAINT `item_detail_metal_id_89846893_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `item_detail_purity_id_3980f05e_fk_purities_id` FOREIGN KEY (`purity_id`) REFERENCES `purities` (`id`),
  CONSTRAINT `item_detail_stock_type_id_f13afe51_fk_stock_type_id` FOREIGN KEY (`stock_type_id`) REFERENCES `stock_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_detail`
--

LOCK TABLES `item_detail` WRITE;
/*!40000 ALTER TABLE `item_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `item_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_id`
--

DROP TABLE IF EXISTS `item_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_id` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_id` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_id`
--

LOCK TABLES `item_id` WRITE;
/*!40000 ALTER TABLE `item_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `item_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `locations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `location_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `created_by` varchar(50) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `location_name` (`location_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locations`
--

LOCK TABLES `locations` WRITE;
/*!40000 ALTER TABLE `locations` DISABLE KEYS */;
INSERT INTO `locations` VALUES (1,'Coimbatore',1,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lot`
--

DROP TABLE IF EXISTS `lot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lot` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `lot_number` varchar(10) NOT NULL,
  `entry_date` date NOT NULL,
  `invoice_number` varchar(50) NOT NULL,
  `total_pieces` int DEFAULT NULL,
  `total_tag_count` int DEFAULT NULL,
  `total_grossweight` double DEFAULT NULL,
  `total_netweight` double DEFAULT NULL,
  `total_stone_pieces` int DEFAULT NULL,
  `total_stone_weight` double DEFAULT NULL,
  `total_stone_rate` double DEFAULT NULL,
  `total_diamond_pieces` int DEFAULT NULL,
  `total_diamond_weight` double DEFAULT NULL,
  `total_diamond_rate` double DEFAULT NULL,
  `tagged_grossweight` double DEFAULT NULL,
  `tagged_netweight` double DEFAULT NULL,
  `tagged_pieces` int DEFAULT NULL,
  `tagged_stone_pieces` int DEFAULT NULL,
  `tagged_stone_weight` double DEFAULT NULL,
  `tagged_diamond_pieces` int DEFAULT NULL,
  `tagged_diamond_weight` double DEFAULT NULL,
  `tagged_tag_count` int DEFAULT NULL,
  `hallmark_number` varchar(100) NOT NULL,
  `hallmark_center` varchar(100) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `branch_id` bigint DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `designer_name_id` bigint NOT NULL,
  `entry_type_id` bigint NOT NULL,
  `tag_status_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lot_number` (`lot_number`),
  UNIQUE KEY `invoice_number` (`invoice_number`),
  KEY `lot_branch_id_1ef542b7_fk_branches_id` (`branch_id`),
  KEY `lot_created_by_id_d4dd3c70_fk_users_id` (`created_by_id`),
  KEY `lot_designer_name_id_d66a71c9_fk_account_head_id` (`designer_name_id`),
  KEY `lot_entry_type_id_a14a823b_fk_entry_type_id` (`entry_type_id`),
  KEY `lot_tag_status_id_36d22b70_fk_status_table_id` (`tag_status_id`),
  CONSTRAINT `lot_branch_id_1ef542b7_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `lot_created_by_id_d4dd3c70_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `lot_designer_name_id_d66a71c9_fk_account_head_id` FOREIGN KEY (`designer_name_id`) REFERENCES `account_head` (`id`),
  CONSTRAINT `lot_entry_type_id_a14a823b_fk_entry_type_id` FOREIGN KEY (`entry_type_id`) REFERENCES `entry_type` (`id`),
  CONSTRAINT `lot_tag_status_id_36d22b70_fk_status_table_id` FOREIGN KEY (`tag_status_id`) REFERENCES `status_table` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lot`
--

LOCK TABLES `lot` WRITE;
/*!40000 ALTER TABLE `lot` DISABLE KEYS */;
/*!40000 ALTER TABLE `lot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lot_id`
--

DROP TABLE IF EXISTS `lot_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lot_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `lot_number` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lot_number` (`lot_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lot_id`
--

LOCK TABLES `lot_id` WRITE;
/*!40000 ALTER TABLE `lot_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `lot_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lot_item`
--

DROP TABLE IF EXISTS `lot_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lot_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bulk_tag` tinyint(1) NOT NULL,
  `pieces` int NOT NULL,
  `tag_count` int NOT NULL,
  `gross_weight` double NOT NULL,
  `net_weight` double NOT NULL,
  `tag_weight` double NOT NULL,
  `cover_weight` double NOT NULL,
  `loop_weight` double NOT NULL,
  `other_weight` double NOT NULL,
  `tagged_grossweight` double DEFAULT NULL,
  `tagged_netweight` double DEFAULT NULL,
  `tagged_pieces` int DEFAULT NULL,
  `tagged_tag_count` int DEFAULT NULL,
  `item_stone_pieces` int DEFAULT NULL,
  `item_stone_weight` double DEFAULT NULL,
  `item_diamond_pieces` int DEFAULT NULL,
  `item_diamond_weight` double DEFAULT NULL,
  `remark` varchar(100) DEFAULT NULL,
  `item_details_id` bigint NOT NULL,
  `lot_details_id` bigint NOT NULL,
  `subitem_details_id` bigint DEFAULT NULL,
  `tag_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lot_item_item_details_id_803d1b78_fk_item_detail_id` (`item_details_id`),
  KEY `lot_item_lot_details_id_b91ff20b_fk_lot_id` (`lot_details_id`),
  KEY `lot_item_subitem_details_id_a859a8d3_fk_sub_item_detail_id` (`subitem_details_id`),
  KEY `lot_item_tag_type_id_8ae45fc1_fk_tag_type_id` (`tag_type_id`),
  CONSTRAINT `lot_item_item_details_id_803d1b78_fk_item_detail_id` FOREIGN KEY (`item_details_id`) REFERENCES `item_detail` (`id`),
  CONSTRAINT `lot_item_lot_details_id_b91ff20b_fk_lot_id` FOREIGN KEY (`lot_details_id`) REFERENCES `lot` (`id`),
  CONSTRAINT `lot_item_subitem_details_id_a859a8d3_fk_sub_item_detail_id` FOREIGN KEY (`subitem_details_id`) REFERENCES `sub_item_detail` (`id`),
  CONSTRAINT `lot_item_tag_type_id_8ae45fc1_fk_tag_type_id` FOREIGN KEY (`tag_type_id`) REFERENCES `tag_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lot_item`
--

LOCK TABLES `lot_item` WRITE;
/*!40000 ALTER TABLE `lot_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `lot_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lot_item_diamond`
--

DROP TABLE IF EXISTS `lot_item_diamond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lot_item_diamond` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `diamond_pieces` int DEFAULT NULL,
  `diamond_weight` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `total_diamond_value` double DEFAULT NULL,
  `tagged_diamond_weight` double DEFAULT NULL,
  `tagged_diamond_pieces` int DEFAULT NULL,
  `include_diamond_weight` tinyint(1) NOT NULL,
  `diamond_name_id` bigint NOT NULL,
  `diamond_rate_type_id` bigint NOT NULL,
  `diamond_weight_type_id` bigint NOT NULL,
  `lot_details_id` bigint NOT NULL,
  `lot_item_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lot_item_diamond_diamond_rate_type_id_baf8c2fb_fk_rate_type_id` (`diamond_rate_type_id`),
  KEY `lot_item_diamond_diamond_weight_type__e7da4f2b_fk_stone_wei` (`diamond_weight_type_id`),
  KEY `lot_item_diamond_lot_details_id_da27600d_fk_lot_id` (`lot_details_id`),
  KEY `lot_item_diamond_lot_item_id_76399d78_fk_lot_item_id` (`lot_item_id`),
  KEY `lot_item_diamond_diamond_name_id_47a3ccba_fk_stone_detail_id` (`diamond_name_id`),
  CONSTRAINT `lot_item_diamond_diamond_name_id_47a3ccba_fk_stone_detail_id` FOREIGN KEY (`diamond_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `lot_item_diamond_diamond_rate_type_id_baf8c2fb_fk_rate_type_id` FOREIGN KEY (`diamond_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `lot_item_diamond_diamond_weight_type__e7da4f2b_fk_stone_wei` FOREIGN KEY (`diamond_weight_type_id`) REFERENCES `stone_weight_type` (`id`),
  CONSTRAINT `lot_item_diamond_lot_details_id_da27600d_fk_lot_id` FOREIGN KEY (`lot_details_id`) REFERENCES `lot` (`id`),
  CONSTRAINT `lot_item_diamond_lot_item_id_76399d78_fk_lot_item_id` FOREIGN KEY (`lot_item_id`) REFERENCES `lot_item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lot_item_diamond`
--

LOCK TABLES `lot_item_diamond` WRITE;
/*!40000 ALTER TABLE `lot_item_diamond` DISABLE KEYS */;
/*!40000 ALTER TABLE `lot_item_diamond` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lot_item_stone`
--

DROP TABLE IF EXISTS `lot_item_stone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lot_item_stone` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stone_pieces` int DEFAULT NULL,
  `stone_weight` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `total_stone_value` double DEFAULT NULL,
  `tagged_stone_weight` double DEFAULT NULL,
  `tagged_stone_pieces` int DEFAULT NULL,
  `include_stone_weight` tinyint(1) NOT NULL,
  `lot_details_id` bigint NOT NULL,
  `lot_item_id` bigint NOT NULL,
  `stone_name_id` bigint NOT NULL,
  `stone_rate_type_id` bigint NOT NULL,
  `stone_weight_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lot_item_stone_stone_rate_type_id_82832fc2_fk_rate_type_id` (`stone_rate_type_id`),
  KEY `lot_item_stone_stone_weight_type_id_d2988b5a_fk_stone_wei` (`stone_weight_type_id`),
  KEY `lot_item_stone_lot_details_id_c70a8748_fk_lot_id` (`lot_details_id`),
  KEY `lot_item_stone_lot_item_id_1b1fdbba_fk_lot_item_id` (`lot_item_id`),
  KEY `lot_item_stone_stone_name_id_e9be2a45_fk_stone_detail_id` (`stone_name_id`),
  CONSTRAINT `lot_item_stone_lot_details_id_c70a8748_fk_lot_id` FOREIGN KEY (`lot_details_id`) REFERENCES `lot` (`id`),
  CONSTRAINT `lot_item_stone_lot_item_id_1b1fdbba_fk_lot_item_id` FOREIGN KEY (`lot_item_id`) REFERENCES `lot_item` (`id`),
  CONSTRAINT `lot_item_stone_stone_name_id_e9be2a45_fk_stone_detail_id` FOREIGN KEY (`stone_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `lot_item_stone_stone_rate_type_id_82832fc2_fk_rate_type_id` FOREIGN KEY (`stone_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `lot_item_stone_stone_weight_type_id_d2988b5a_fk_stone_wei` FOREIGN KEY (`stone_weight_type_id`) REFERENCES `stone_weight_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lot_item_stone`
--

LOCK TABLES `lot_item_stone` WRITE;
/*!40000 ALTER TABLE `lot_item_stone` DISABLE KEYS */;
/*!40000 ALTER TABLE `lot_item_stone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_menu_group`
--

DROP TABLE IF EXISTS `main_menu_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_menu_group` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `main_menugroup_name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `main_menugroup_name` (`main_menugroup_name`),
  KEY `main_menu_group_created_by_id_a481762b_fk_users_id` (`created_by_id`),
  CONSTRAINT `main_menu_group_created_by_id_a481762b_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_menu_group`
--

LOCK TABLES `main_menu_group` WRITE;
/*!40000 ALTER TABLE `main_menu_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_menu_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measurement_detail`
--

DROP TABLE IF EXISTS `measurement_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `measurement_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `measurement_name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `measurement_name` (`measurement_name`),
  KEY `measurement_detail_created_by_id_92ba0371_fk_users_id` (`created_by_id`),
  CONSTRAINT `measurement_detail_created_by_id_92ba0371_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measurement_detail`
--

LOCK TABLES `measurement_detail` WRITE;
/*!40000 ALTER TABLE `measurement_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `measurement_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measurement_type`
--

DROP TABLE IF EXISTS `measurement_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `measurement_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `measurement_name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `measurement_name` (`measurement_name`),
  KEY `measurement_type_created_by_id_8221f395_fk_users_id` (`created_by_id`),
  CONSTRAINT `measurement_type_created_by_id_8221f395_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measurement_type`
--

LOCK TABLES `measurement_type` WRITE;
/*!40000 ALTER TABLE `measurement_type` DISABLE KEYS */;
INSERT INTO `measurement_type` VALUES (1,'length',1,NULL,NULL,NULL,NULL),(2,'size',1,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `measurement_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `melting_issue`
--

DROP TABLE IF EXISTS `melting_issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `melting_issue` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `melting_issue_id` varchar(50) NOT NULL,
  `issued_date` date NOT NULL,
  `return_days` int NOT NULL,
  `return_date` date NOT NULL,
  `bullion_rate` double NOT NULL,
  `stone_weight` double NOT NULL,
  `gross_weight` double NOT NULL,
  `net_weight` double NOT NULL,
  `notes` longtext,
  `issued_at` datetime(6) DEFAULT NULL,
  `branch_id` bigint NOT NULL,
  `issued_by_id` bigint NOT NULL,
  `issued_category_id` bigint NOT NULL,
  `melting_status_id` bigint NOT NULL,
  `transfer_creation_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `transfer_creation_details_id` (`transfer_creation_details_id`),
  KEY `melting_issue_issued_category_id_6f645d00_fk_old_metal` (`issued_category_id`),
  KEY `melting_issue_melting_status_id_82ec89e0_fk_status_table_id` (`melting_status_id`),
  KEY `melting_issue_branch_id_80107501_fk_branches_id` (`branch_id`),
  KEY `melting_issue_issued_by_id_a9af4626_fk_users_id` (`issued_by_id`),
  CONSTRAINT `melting_issue_branch_id_80107501_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `melting_issue_issued_by_id_a9af4626_fk_users_id` FOREIGN KEY (`issued_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `melting_issue_issued_category_id_6f645d00_fk_old_metal` FOREIGN KEY (`issued_category_id`) REFERENCES `old_metal_category` (`id`),
  CONSTRAINT `melting_issue_melting_status_id_82ec89e0_fk_status_table_id` FOREIGN KEY (`melting_status_id`) REFERENCES `status_table` (`id`),
  CONSTRAINT `melting_issue_transfer_creation_de_d38fc6db_fk_transfer_` FOREIGN KEY (`transfer_creation_details_id`) REFERENCES `transfer_creation` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `melting_issue`
--

LOCK TABLES `melting_issue` WRITE;
/*!40000 ALTER TABLE `melting_issue` DISABLE KEYS */;
/*!40000 ALTER TABLE `melting_issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `melting_issue_id`
--

DROP TABLE IF EXISTS `melting_issue_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `melting_issue_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `melting_issue_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `melting_issue_id` (`melting_issue_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `melting_issue_id`
--

LOCK TABLES `melting_issue_id` WRITE;
/*!40000 ALTER TABLE `melting_issue_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `melting_issue_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `melting_issue_number`
--

DROP TABLE IF EXISTS `melting_issue_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `melting_issue_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `melting_issue_number` varchar(50) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `melting_issue_number` (`melting_issue_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `melting_issue_number_user_id_c46de04f_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `melting_issue_number`
--

LOCK TABLES `melting_issue_number` WRITE;
/*!40000 ALTER TABLE `melting_issue_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `melting_issue_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `melting_recipt`
--

DROP TABLE IF EXISTS `melting_recipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `melting_recipt` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `melting_recipt_id` varchar(50) NOT NULL,
  `received_date` date NOT NULL,
  `melting_loss_weight` double NOT NULL,
  `recipt_net_weight` double NOT NULL,
  `melting_charges` double NOT NULL,
  `amount_paid` double NOT NULL,
  `remark` longtext,
  `received_at` datetime(6) DEFAULT NULL,
  `branch_id` bigint NOT NULL,
  `melting_issue_details_id` bigint NOT NULL,
  `melting_status_id` bigint NOT NULL,
  `payment_status_id` bigint NOT NULL,
  `received_by_id` bigint NOT NULL,
  `received_category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `melting_issue_details_id` (`melting_issue_details_id`),
  KEY `melting_recipt_received_category_id_511dcb55_fk_old_metal` (`received_category_id`),
  KEY `melting_recipt_branch_id_2f137e9a_fk_branches_id` (`branch_id`),
  KEY `melting_recipt_melting_status_id_2bf45515_fk_status_table_id` (`melting_status_id`),
  KEY `melting_recipt_payment_status_id_83a7898b_fk_status_table_id` (`payment_status_id`),
  KEY `melting_recipt_received_by_id_9b60e6d1_fk_users_id` (`received_by_id`),
  CONSTRAINT `melting_recipt_branch_id_2f137e9a_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `melting_recipt_melting_issue_detail_dfd1847a_fk_melting_i` FOREIGN KEY (`melting_issue_details_id`) REFERENCES `melting_issue` (`id`),
  CONSTRAINT `melting_recipt_melting_status_id_2bf45515_fk_status_table_id` FOREIGN KEY (`melting_status_id`) REFERENCES `status_table` (`id`),
  CONSTRAINT `melting_recipt_payment_status_id_83a7898b_fk_status_table_id` FOREIGN KEY (`payment_status_id`) REFERENCES `status_table` (`id`),
  CONSTRAINT `melting_recipt_received_by_id_9b60e6d1_fk_users_id` FOREIGN KEY (`received_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `melting_recipt_received_category_id_511dcb55_fk_old_metal` FOREIGN KEY (`received_category_id`) REFERENCES `old_metal_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `melting_recipt`
--

LOCK TABLES `melting_recipt` WRITE;
/*!40000 ALTER TABLE `melting_recipt` DISABLE KEYS */;
/*!40000 ALTER TABLE `melting_recipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `melting_recipt_id`
--

DROP TABLE IF EXISTS `melting_recipt_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `melting_recipt_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `melting_recipt_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `melting_recipt_id` (`melting_recipt_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `melting_recipt_id`
--

LOCK TABLES `melting_recipt_id` WRITE;
/*!40000 ALTER TABLE `melting_recipt_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `melting_recipt_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `melting_recipt_number`
--

DROP TABLE IF EXISTS `melting_recipt_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `melting_recipt_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `melting_recipt_number` varchar(50) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `melting_recipt_number` (`melting_recipt_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `melting_recipt_number_user_id_a8957a8b_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `melting_recipt_number`
--

LOCK TABLES `melting_recipt_number` WRITE;
/*!40000 ALTER TABLE `melting_recipt_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `melting_recipt_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_groups`
--

DROP TABLE IF EXISTS `menu_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_group_name` varchar(50) NOT NULL,
  `icon` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `main_menu_group_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `menu_group_name` (`menu_group_name`),
  KEY `menu_groups_created_by_id_8d0cfa3c_fk_users_id` (`created_by_id`),
  KEY `menu_groups_main_menu_group_id_73c68cc1_fk_main_menu_group_id` (`main_menu_group_id`),
  CONSTRAINT `menu_groups_created_by_id_8d0cfa3c_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `menu_groups_main_menu_group_id_73c68cc1_fk_main_menu_group_id` FOREIGN KEY (`main_menu_group_id`) REFERENCES `main_menu_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_groups`
--

LOCK TABLES `menu_groups` WRITE;
/*!40000 ALTER TABLE `menu_groups` DISABLE KEYS */;
INSERT INTO `menu_groups` VALUES (1,'approval','',1,'2024-07-03 05:59:36.649646',NULL,NULL,1,NULL),(2,'billing','',1,'2024-07-03 05:59:36.690643',NULL,NULL,1,NULL),(3,'books','',1,'2024-07-03 05:59:36.789232',NULL,NULL,1,NULL),(4,'infrastructure','',1,'2024-07-03 05:59:36.953209',NULL,NULL,1,NULL),(5,'masters','',1,'2024-07-03 05:59:37.096873',NULL,NULL,1,NULL),(6,'purchase & order','',1,'2024-07-03 05:59:37.226572',NULL,NULL,1,NULL),(7,'organization','',1,'2024-07-03 05:59:37.333408',NULL,NULL,1,NULL),(8,'payments & target','',1,'2024-07-03 05:59:37.424033',NULL,NULL,1,NULL),(9,'product master','',1,'2024-07-03 05:59:37.595653',NULL,NULL,1,NULL),(10,'refinery management','',1,'2024-07-03 05:59:37.732425',NULL,NULL,1,NULL),(11,'repair management','',1,'2024-07-03 05:59:37.845942',NULL,NULL,1,NULL),(12,'reports','',1,'2024-07-03 05:59:37.954352',NULL,NULL,1,NULL),(13,'settings','',1,'2024-07-03 05:59:38.031363',NULL,NULL,1,NULL),(14,'stock','',1,'2024-07-03 05:59:38.108949',NULL,NULL,1,NULL),(15,'valueaddition','',1,'2024-07-03 05:59:38.261027',NULL,NULL,1,NULL);
/*!40000 ALTER TABLE `menu_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_permissions`
--

DROP TABLE IF EXISTS `menu_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `view_permit` tinyint(1) NOT NULL,
  `add_permit` tinyint(1) NOT NULL,
  `edit_permit` tinyint(1) NOT NULL,
  `delete_permit` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `menu_id` bigint NOT NULL,
  `user_role_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `menu_permissions_created_by_id_ea308b66_fk_users_id` (`created_by_id`),
  KEY `menu_permissions_menu_id_96757d9c_fk_menus_id` (`menu_id`),
  KEY `menu_permissions_user_role_id_49244274_fk_user_roles_id` (`user_role_id`),
  CONSTRAINT `menu_permissions_created_by_id_ea308b66_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `menu_permissions_menu_id_96757d9c_fk_menus_id` FOREIGN KEY (`menu_id`) REFERENCES `menus` (`id`),
  CONSTRAINT `menu_permissions_user_role_id_49244274_fk_user_roles_id` FOREIGN KEY (`user_role_id`) REFERENCES `user_roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_permissions`
--

LOCK TABLES `menu_permissions` WRITE;
/*!40000 ALTER TABLE `menu_permissions` DISABLE KEYS */;
INSERT INTO `menu_permissions` VALUES (1,1,1,1,1,'2024-07-03 06:14:07.000000',NULL,1,2,1),(2,1,1,1,1,'2024-07-03 06:17:42.253904','2024-07-03 06:18:18.158061',1,30,1),(3,1,1,1,1,'2024-07-03 06:17:42.848946',NULL,1,39,1),(4,1,1,1,1,'2024-07-03 06:17:43.443917',NULL,1,28,1),(5,1,1,1,1,'2024-07-03 06:17:44.019907',NULL,1,29,1),(6,1,1,1,1,'2024-07-03 06:17:44.742247',NULL,1,71,1),(7,1,1,1,1,'2024-07-03 06:17:45.360726',NULL,1,13,1),(8,1,1,1,1,'2024-07-03 06:17:45.969701',NULL,1,14,1),(9,1,1,1,1,'2024-07-03 06:17:47.415695',NULL,1,15,1),(10,1,1,1,1,'2024-07-03 06:17:48.450627',NULL,1,16,1),(11,1,1,1,1,'2024-07-03 06:17:48.627332',NULL,1,17,1),(12,1,1,1,1,'2024-07-03 06:17:49.396187',NULL,1,18,1),(13,1,1,1,1,'2024-07-03 06:17:49.734002',NULL,1,65,1),(14,1,1,1,1,'2024-07-03 06:17:51.332395',NULL,1,69,1),(15,1,1,1,1,'2024-07-03 06:17:55.948800',NULL,1,12,1),(16,1,1,1,1,'2024-07-03 06:17:55.981527',NULL,1,6,1),(17,1,1,1,1,'2024-07-03 06:17:56.680098',NULL,1,7,1),(18,1,1,1,1,'2024-07-03 06:17:57.197377',NULL,1,8,1),(19,1,1,1,1,'2024-07-03 06:17:57.770459',NULL,1,9,1),(20,1,1,1,1,'2024-07-03 06:17:58.734056',NULL,1,10,1),(21,1,1,1,1,'2024-07-03 06:18:00.586727',NULL,1,11,1),(22,1,1,1,1,'2024-07-03 06:18:00.995781',NULL,1,33,1),(23,1,1,1,1,'2024-07-03 06:18:01.621185',NULL,1,38,1),(24,1,1,1,1,'2024-07-03 06:18:02.431115',NULL,1,47,1),(25,1,1,1,1,'2024-07-03 06:18:02.944207',NULL,1,3,1),(26,1,1,1,1,'2024-07-03 06:18:03.508327',NULL,1,4,1),(27,1,1,1,1,'2024-07-03 06:18:04.295022',NULL,1,5,1),(28,1,1,1,1,'2024-07-03 06:18:04.768260',NULL,1,41,1),(29,1,1,1,1,'2024-07-03 06:18:05.741080',NULL,1,48,1),(30,1,1,1,1,'2024-07-03 06:18:07.575734',NULL,1,19,1),(31,1,1,1,1,'2024-07-03 06:18:08.018090',NULL,1,20,1),(32,1,1,1,1,'2024-07-03 06:18:08.675411',NULL,1,42,1),(33,1,1,1,1,'2024-07-03 06:18:09.252503',NULL,1,43,1),(34,1,1,1,1,'2024-07-03 06:18:10.255381',NULL,1,44,1),(35,1,1,1,1,'2024-07-03 06:18:11.465829',NULL,1,45,1),(36,1,1,1,1,'2024-07-03 06:18:12.339761',NULL,1,46,1),(37,1,1,1,1,'2024-07-03 06:18:13.116837',NULL,1,40,1),(38,1,1,1,1,'2024-07-03 06:18:15.705067',NULL,1,34,1),(39,1,1,1,1,'2024-07-03 06:18:22.228405',NULL,1,35,1),(40,1,1,1,1,'2024-07-03 06:18:22.636907',NULL,1,36,1),(41,1,1,1,1,'2024-07-03 06:18:23.263235',NULL,1,37,1),(42,1,1,1,1,'2024-07-03 06:18:23.872703',NULL,1,49,1),(43,1,1,1,1,'2024-07-03 06:18:24.586684',NULL,1,50,1),(44,1,1,1,1,'2024-07-03 06:18:24.950534',NULL,1,51,1),(45,1,1,1,1,'2024-07-03 06:18:26.861329',NULL,1,52,1),(46,1,1,1,1,'2024-07-03 06:18:27.983469',NULL,1,53,1),(47,1,1,1,1,'2024-07-03 06:18:28.808063',NULL,1,54,1),(48,1,1,1,1,'2024-07-03 06:18:29.625450',NULL,1,55,1),(49,1,1,1,1,'2024-07-03 06:18:30.570415',NULL,1,56,1),(50,1,1,1,1,'2024-07-03 06:18:34.798491',NULL,1,57,1),(51,1,1,1,1,'2024-07-03 06:18:34.806491',NULL,1,58,1),(52,1,1,1,1,'2024-07-03 06:18:34.817722',NULL,1,59,1),(53,1,1,1,1,'2024-07-03 06:18:36.384949',NULL,1,60,1),(54,1,1,1,1,'2024-07-03 06:18:36.392971',NULL,1,61,1),(55,1,1,1,1,'2024-07-03 06:18:37.298315',NULL,1,62,1),(56,1,1,1,1,'2024-07-03 06:18:37.635079',NULL,1,63,1),(57,1,1,1,1,'2024-07-03 06:18:38.997082',NULL,1,64,1),(58,1,1,1,1,'2024-07-03 06:18:40.730042',NULL,1,66,1),(59,1,1,1,1,'2024-07-03 06:18:43.193694',NULL,1,67,1),(60,1,1,1,1,'2024-07-03 06:18:43.926423',NULL,1,68,1),(61,1,1,1,1,'2024-07-03 06:18:44.952775',NULL,1,1,1),(62,1,1,1,1,'2024-07-03 06:18:47.632299',NULL,1,70,1),(63,1,1,1,1,'2024-07-03 06:18:49.894747',NULL,1,21,1),(64,1,1,1,1,'2024-07-03 06:18:50.712177',NULL,1,22,1),(65,1,1,1,1,'2024-07-03 06:18:51.553795',NULL,1,23,1),(66,1,1,1,1,'2024-07-03 06:18:52.170730',NULL,1,24,1),(67,1,1,1,1,'2024-07-03 06:18:52.676167',NULL,1,25,1),(68,1,1,1,1,'2024-07-03 06:18:53.164995',NULL,1,26,1),(69,1,1,1,1,'2024-07-03 06:18:53.702112',NULL,1,27,1),(70,1,1,1,1,'2024-07-03 06:18:54.423394',NULL,1,31,1),(71,1,1,1,1,'2024-07-03 06:18:54.937918',NULL,1,32,1);
/*!40000 ALTER TABLE `menu_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menus`
--

DROP TABLE IF EXISTS `menus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `menu_name` varchar(50) NOT NULL,
  `menu_path` varchar(50) NOT NULL,
  `icon` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `menu_group_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `menu_name` (`menu_name`),
  UNIQUE KEY `menu_path` (`menu_path`),
  KEY `menus_menu_group_id_b3ae3c78_fk_menu_groups_id` (`menu_group_id`),
  KEY `menus_created_by_id_55141c08_fk_users_id` (`created_by_id`),
  CONSTRAINT `menus_created_by_id_55141c08_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `menus_menu_group_id_b3ae3c78_fk_menu_groups_id` FOREIGN KEY (`menu_group_id`) REFERENCES `menu_groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menus`
--

LOCK TABLES `menus` WRITE;
/*!40000 ALTER TABLE `menus` DISABLE KEYS */;
INSERT INTO `menus` VALUES (1,'user role','/userrole','',1,'2024-07-03 06:13:45.120601',NULL,NULL,1,13),(2,'menu permission','/menupermission','',1,'2024-07-03 06:13:45.171499',NULL,NULL,1,13),(3,'organizations','/organization/organizations','',1,'2024-07-03 06:13:45.255304',NULL,NULL,1,7),(4,'staff','/organization/staff','',1,'2024-07-03 06:13:45.357172',NULL,NULL,1,7),(5,'user','/organization/user','',1,'2024-07-03 06:13:45.449306',NULL,NULL,1,7),(6,'metal purity','/masters/metal-purity','',1,'2024-07-03 06:13:45.533005',NULL,NULL,1,5),(7,'metal rates','/masters/metal-rates','',1,'2024-07-03 06:13:45.615523',NULL,NULL,1,5),(8,'tag','/masters/tag','',1,'2024-07-03 06:13:45.704319',NULL,NULL,1,5),(9,'tax','/masters/tax','',1,'2024-07-03 06:13:45.793772',NULL,NULL,1,5),(10,'standard','/masters/standard','',1,'2024-07-03 06:13:45.887025',NULL,NULL,1,5),(11,'rangestock','/masters/rangestock','',1,'2024-07-03 06:13:45.973912',NULL,NULL,1,5),(12,'floor counter','/infrastructure/floor-counter','',1,'2024-07-03 06:13:46.346614',NULL,NULL,1,4),(13,'company','/books/company','',1,'2024-07-03 06:13:46.512857',NULL,NULL,1,3),(14,'account head','/books/account-head','',1,'2024-07-03 06:13:46.603248',NULL,NULL,1,3),(15,'account group','/books/account-group','',1,'2024-07-03 06:13:46.682613',NULL,NULL,1,3),(16,'customer','/books/customer','',1,'2024-07-03 06:13:46.863076',NULL,NULL,1,3),(17,'customergroup','/books/customergroup','',1,'2024-07-03 06:13:46.956162',NULL,NULL,1,3),(18,'advance payment','/books/advance-payment','',1,'2024-07-03 06:13:47.047006',NULL,NULL,1,3),(19,'item master','/product-master/item-master','',1,'2024-07-03 06:13:47.128521',NULL,NULL,1,9),(20,'sub item master','/product-master/sub-item-master','',1,'2024-07-03 06:13:47.325892',NULL,NULL,1,9),(21,'itemtag','/stock/itemtag','',1,'2024-07-03 06:13:47.408421',NULL,NULL,1,14),(22,'lot','/stock/lot','',1,'2024-07-03 06:13:47.499747',NULL,NULL,1,14),(23,'tag update','/stock/tag-update','',1,'2024-07-03 06:13:47.599726',NULL,NULL,1,14),(24,'tag details','/stock/tag-details','',1,'2024-07-03 06:13:47.711013',NULL,NULL,1,14),(25,'duplicate tag','/stock/duplicate-tag','',1,'2024-07-03 06:13:47.823380',NULL,NULL,1,14),(26,'stock list','/stock/stock-list','',1,'2024-07-03 06:13:47.957890',NULL,NULL,1,14),(27,'stock transfer','/stock/stock-transfer','',1,'2024-07-03 06:13:48.044424',NULL,NULL,1,14),(28,'estimate billing','/billing/estimate-billing','',1,'2024-07-03 06:13:48.129258',NULL,NULL,1,2),(29,'billing','/billing/billing','',1,'2024-07-03 06:13:48.219855',NULL,NULL,1,2),(30,'billing & estimation approval','/approval/billing-&-estimation-approval','',1,'2024-07-03 06:13:48.357091',NULL,NULL,1,1),(31,'valueaddition customer','/valueaddition/valueaddition-customer','',1,'2024-07-03 06:13:48.441203',NULL,NULL,1,15),(32,'valueaddition designer','/valueaddition/valueaddition-designer','',1,'2024-07-03 06:13:48.574578',NULL,NULL,1,15),(33,'order','/purchase-&-order/order','',1,'2024-07-03 06:13:48.660329',NULL,NULL,1,6),(34,'sale report','/reports/sale-report','',1,'2024-07-03 06:13:48.737822',NULL,NULL,1,12),(35,'tag report','/reports/tag-report','',1,'2024-07-03 06:13:48.813736',NULL,NULL,1,12),(36,'sales details report','/reports/sales-details-report','',1,'2024-07-03 06:13:48.907179',NULL,NULL,1,12),(37,'itemwise report','/reports/itemwise-report','',1,'2024-07-03 06:13:48.984803',NULL,NULL,1,12),(38,'old purchase','/purchase-&-order/old-purchase','',1,'2024-07-03 06:13:49.069589',NULL,NULL,1,6),(39,'approval type and rule','/approval/approval-type-and-rule','',1,'2024-07-03 06:13:49.155780',NULL,NULL,1,1),(40,'repair creation','/repair-management/repair-creation','',1,'2024-07-03 06:13:49.256047',NULL,NULL,1,11),(41,'counter target','/payments-&-target/counter-target','',1,'2024-07-03 06:13:49.449197',NULL,NULL,1,8),(42,'transfer creation','/refinery-management/transfer-creation','',1,'2024-07-03 06:13:49.584048',NULL,NULL,1,10),(43,'melting issue','/refinery-management/melting-issue','',1,'2024-07-03 06:13:49.975037',NULL,NULL,1,10),(44,'melting receipt','/refinery-management/melting-receipt','',1,'2024-07-03 06:13:50.026183',NULL,NULL,1,10),(45,'purification issue','/refinery-management/purification-issue','',1,'2024-07-03 06:13:50.127939',NULL,NULL,1,10),(46,'purification receipt','/refinery-management/purification-receipt','',1,'2024-07-03 06:13:50.266858',NULL,NULL,1,10),(47,'new purchase','/purchase-&-order/new-purchase','',1,'2024-07-03 06:13:50.503446',NULL,NULL,1,6),(48,'vendor payment','/payments-&-target/vendor-payment','',1,'2024-07-03 06:13:50.578414',NULL,NULL,1,8),(49,'sale detail report','/reports/sale-detail-report','',1,'2024-07-03 06:13:50.655724',NULL,NULL,1,12),(50,'item wise sale report','/reports/item-wise-sale-report','',1,'2024-07-03 06:13:50.740421',NULL,NULL,1,12),(51,'lot entry report','/reports/lot-entry-report','',1,'2024-07-03 06:13:50.872200',NULL,NULL,1,12),(52,'vendor wise lot report','/reports/vendor-wise-lot-report','',1,'2024-07-03 06:13:50.976540',NULL,NULL,1,12),(53,'stock summary report','/reports/stock-summary-report','',1,'2024-07-03 06:13:51.134458',NULL,NULL,1,12),(54,'stocke report tag wise','/reports/stocke-report-tag-wise','',1,'2024-07-03 06:13:51.243706',NULL,NULL,1,12),(55,'stocke report item wise','/reports/stocke-report-item-wise','',1,'2024-07-03 06:13:51.422084',NULL,NULL,1,12),(56,'range value stock report','/reports/range-value-stock-report','',1,'2024-07-03 06:13:51.503330',NULL,NULL,1,12),(57,'purchase report','/reports/purchase-report','',1,'2024-07-03 06:13:51.590960',NULL,NULL,1,12),(58,'item wise purchase report','/reports/item-wise-purchase-report','',1,'2024-07-03 06:13:51.708184',NULL,NULL,1,12),(59,'vendor wise purchase report','/reports/vendor-wise-purchase-report','',1,'2024-07-03 06:13:51.797272',NULL,NULL,1,12),(60,'old purchase report','/reports/old-purchase-report','',1,'2024-07-03 06:13:51.886290',NULL,NULL,1,12),(61,'customer repair report','/reports/customer-repair-report','',1,'2024-07-03 06:13:51.965272',NULL,NULL,1,12),(62,'vendor repair report','/reports/vendor-repair-report','',1,'2024-07-03 06:13:52.078861',NULL,NULL,1,12),(63,'daily sales report','/reports/daily-sales-report','',1,'2024-07-03 06:13:52.160203',NULL,NULL,1,12),(64,'customer sale report','/reports/customer-sale-report','',1,'2024-07-03 06:13:52.483288',NULL,NULL,1,12),(65,'credit/debit','/books/credit/debit','',1,'2024-07-03 06:13:52.771630',NULL,NULL,1,3),(66,'payment report','/reports/payment-report','',1,'2024-07-03 06:13:52.875995',NULL,NULL,1,12),(67,'sales incentive percentage report','/reports/sales-incentive-percentage-report','',1,'2024-07-03 06:13:52.974010',NULL,NULL,1,12),(68,'sales incentive amount report','/reports/sales-incentive-amount-report','',1,'2024-07-03 06:13:53.059199',NULL,NULL,1,12),(69,'incentive','/books/incentive','',1,'2024-07-03 06:13:53.137234',NULL,NULL,1,3),(70,'settings','/settings/settings','',1,'2024-07-03 06:13:53.241652',NULL,NULL,1,13),(71,'misc billing','/billing/misc-billing','',1,'2024-07-03 06:13:53.351379',NULL,NULL,1,2);
/*!40000 ALTER TABLE `menus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metal_old_rate`
--

DROP TABLE IF EXISTS `metal_old_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metal_old_rate` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `old_metal_rate` double DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `metal_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `metal_old_rate_created_by_id_aa097934_fk_users_id` (`created_by_id`),
  KEY `metal_old_rate_metal_id_b963290a_fk_metals_id` (`metal_id`),
  CONSTRAINT `metal_old_rate_created_by_id_aa097934_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `metal_old_rate_metal_id_b963290a_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metal_old_rate`
--

LOCK TABLES `metal_old_rate` WRITE;
/*!40000 ALTER TABLE `metal_old_rate` DISABLE KEYS */;
/*!40000 ALTER TABLE `metal_old_rate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metal_rates`
--

DROP TABLE IF EXISTS `metal_rates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metal_rates` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `association_rate` json NOT NULL,
  `rate` json NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `metal_rates_created_by_id_7c375473_fk_users_id` (`created_by_id`),
  CONSTRAINT `metal_rates_created_by_id_7c375473_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metal_rates`
--

LOCK TABLES `metal_rates` WRITE;
/*!40000 ALTER TABLE `metal_rates` DISABLE KEYS */;
/*!40000 ALTER TABLE `metal_rates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metals`
--

DROP TABLE IF EXISTS `metals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metals` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `metal_name` varchar(100) NOT NULL,
  `metal_code` varchar(10) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `metal_name` (`metal_name`),
  UNIQUE KEY `metal_code` (`metal_code`),
  KEY `metals_created_by_id_855044de_fk_users_id` (`created_by_id`),
  CONSTRAINT `metals_created_by_id_855044de_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metals`
--

LOCK TABLES `metals` WRITE;
/*!40000 ALTER TABLE `metals` DISABLE KEYS */;
/*!40000 ALTER TABLE `metals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `newpurchase`
--

DROP TABLE IF EXISTS `newpurchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `newpurchase` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `total_pieces` int DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `order_date` date DEFAULT NULL,
  `total_item` int DEFAULT NULL,
  `total_net_weight` double DEFAULT NULL,
  `total_gross_weight` double DEFAULT NULL,
  `others` int DEFAULT NULL,
  `hallmark` int DEFAULT NULL,
  `total_amount` double DEFAULT NULL,
  `is_billed` tinyint(1) DEFAULT NULL,
  `purchase_order_id` varchar(100) DEFAULT NULL,
  `total_pure_weight` double DEFAULT NULL,
  `paid_weight` double DEFAULT NULL,
  `paid_amount` double DEFAULT NULL,
  `no_of_days` int DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `branch_id` bigint DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `designer_name_id` bigint DEFAULT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `newpurchase_branch_id_8ea9ee84_fk_branches_id` (`branch_id`),
  KEY `newpurchase_created_by_id_7e6bf8e5_fk_users_id` (`created_by_id`),
  KEY `newpurchase_designer_name_id_2d0439f2_fk_account_head_id` (`designer_name_id`),
  KEY `newpurchase_modified_by_id_b93123fa_fk_users_id` (`modified_by_id`),
  CONSTRAINT `newpurchase_branch_id_8ea9ee84_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `newpurchase_created_by_id_7e6bf8e5_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `newpurchase_designer_name_id_2d0439f2_fk_account_head_id` FOREIGN KEY (`designer_name_id`) REFERENCES `account_head` (`id`),
  CONSTRAINT `newpurchase_modified_by_id_b93123fa_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `newpurchase`
--

LOCK TABLES `newpurchase` WRITE;
/*!40000 ALTER TABLE `newpurchase` DISABLE KEYS */;
/*!40000 ALTER TABLE `newpurchase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `newpurchase_item_detail`
--

DROP TABLE IF EXISTS `newpurchase_item_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `newpurchase_item_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `item_code` varchar(100) DEFAULT NULL,
  `flat_wastage` double DEFAULT NULL,
  `wastage` double DEFAULT NULL,
  `making_charge_pergram` double DEFAULT NULL,
  `flat_makingcharge` double DEFAULT NULL,
  `pieces` int DEFAULT NULL,
  `gross_weight` double DEFAULT NULL,
  `less_weight` double DEFAULT NULL,
  `net_weight` double DEFAULT NULL,
  `touch` double DEFAULT NULL,
  `pure_weight` double DEFAULT NULL,
  `no_stone_pieces` int DEFAULT NULL,
  `stone_weight` double DEFAULT NULL,
  `no_diamond_pieces` int DEFAULT NULL,
  `diamond_weight` double DEFAULT NULL,
  `stone_amount` double DEFAULT NULL,
  `total_amount` double DEFAULT NULL,
  `diamond_amount` double DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `item_id` bigint DEFAULT NULL,
  `metal_id` bigint DEFAULT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  `purchase_order_id` bigint DEFAULT NULL,
  `sub_item_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `newpurchase_item_detail_created_by_id_86efa44f_fk_users_id` (`created_by_id`),
  KEY `newpurchase_item_detail_item_id_5cebf00f_fk_item_detail_id` (`item_id`),
  KEY `newpurchase_item_detail_metal_id_2a3a7169_fk_metals_id` (`metal_id`),
  KEY `newpurchase_item_detail_modified_by_id_f8b15a47_fk_users_id` (`modified_by_id`),
  KEY `newpurchase_item_det_purchase_order_id_070a35f1_fk_newpurcha` (`purchase_order_id`),
  KEY `newpurchase_item_det_sub_item_id_2c7aa9a4_fk_sub_item_` (`sub_item_id`),
  CONSTRAINT `newpurchase_item_det_purchase_order_id_070a35f1_fk_newpurcha` FOREIGN KEY (`purchase_order_id`) REFERENCES `newpurchase` (`id`),
  CONSTRAINT `newpurchase_item_det_sub_item_id_2c7aa9a4_fk_sub_item_` FOREIGN KEY (`sub_item_id`) REFERENCES `sub_item_detail` (`id`),
  CONSTRAINT `newpurchase_item_detail_created_by_id_86efa44f_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `newpurchase_item_detail_item_id_5cebf00f_fk_item_detail_id` FOREIGN KEY (`item_id`) REFERENCES `item_detail` (`id`),
  CONSTRAINT `newpurchase_item_detail_metal_id_2a3a7169_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `newpurchase_item_detail_modified_by_id_f8b15a47_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `newpurchase_item_detail`
--

LOCK TABLES `newpurchase_item_detail` WRITE;
/*!40000 ALTER TABLE `newpurchase_item_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `newpurchase_item_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `newpurchase_item_diamond`
--

DROP TABLE IF EXISTS `newpurchase_item_diamond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `newpurchase_item_diamond` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `diamond_pieces` int DEFAULT NULL,
  `diamond_weight` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `include_diamond_weight` tinyint(1) NOT NULL,
  `total_diamond_value` double DEFAULT NULL,
  `diamond_name_id` bigint NOT NULL,
  `diamond_rate_type_id` bigint NOT NULL,
  `diamond_weight_type_id` bigint NOT NULL,
  `purchase_item_id` bigint DEFAULT NULL,
  `purchase_order_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `newpurchase_item_dia_diamond_name_id_c1e4e937_fk_stone_det` (`diamond_name_id`),
  KEY `newpurchase_item_dia_diamond_rate_type_id_d8564898_fk_rate_type` (`diamond_rate_type_id`),
  KEY `newpurchase_item_dia_diamond_weight_type__298fd3a8_fk_stone_wei` (`diamond_weight_type_id`),
  KEY `newpurchase_item_dia_purchase_item_id_4087da85_fk_newpurcha` (`purchase_item_id`),
  KEY `newpurchase_item_dia_purchase_order_id_7c771a47_fk_newpurcha` (`purchase_order_id`),
  CONSTRAINT `newpurchase_item_dia_diamond_name_id_c1e4e937_fk_stone_det` FOREIGN KEY (`diamond_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `newpurchase_item_dia_diamond_rate_type_id_d8564898_fk_rate_type` FOREIGN KEY (`diamond_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `newpurchase_item_dia_diamond_weight_type__298fd3a8_fk_stone_wei` FOREIGN KEY (`diamond_weight_type_id`) REFERENCES `stone_weight_type` (`id`),
  CONSTRAINT `newpurchase_item_dia_purchase_item_id_4087da85_fk_newpurcha` FOREIGN KEY (`purchase_item_id`) REFERENCES `newpurchase_item_detail` (`id`),
  CONSTRAINT `newpurchase_item_dia_purchase_order_id_7c771a47_fk_newpurcha` FOREIGN KEY (`purchase_order_id`) REFERENCES `newpurchase` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `newpurchase_item_diamond`
--

LOCK TABLES `newpurchase_item_diamond` WRITE;
/*!40000 ALTER TABLE `newpurchase_item_diamond` DISABLE KEYS */;
/*!40000 ALTER TABLE `newpurchase_item_diamond` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `newpurchase_item_stone`
--

DROP TABLE IF EXISTS `newpurchase_item_stone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `newpurchase_item_stone` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stone_pieces` int DEFAULT NULL,
  `stone_weight` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `include_stone_weight` tinyint(1) NOT NULL,
  `total_stone_value` double DEFAULT NULL,
  `purchase_item_id` bigint DEFAULT NULL,
  `purchase_order_id` bigint DEFAULT NULL,
  `stone_name_id` bigint NOT NULL,
  `stone_rate_type_id` bigint NOT NULL,
  `stone_weight_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `newpurchase_item_sto_purchase_item_id_71470364_fk_newpurcha` (`purchase_item_id`),
  KEY `newpurchase_item_sto_purchase_order_id_afd7f5b1_fk_newpurcha` (`purchase_order_id`),
  KEY `newpurchase_item_stone_stone_name_id_bcccfa20_fk_stone_detail_id` (`stone_name_id`),
  KEY `newpurchase_item_sto_stone_rate_type_id_66c744aa_fk_rate_type` (`stone_rate_type_id`),
  KEY `newpurchase_item_sto_stone_weight_type_id_0d517f0c_fk_stone_wei` (`stone_weight_type_id`),
  CONSTRAINT `newpurchase_item_sto_purchase_item_id_71470364_fk_newpurcha` FOREIGN KEY (`purchase_item_id`) REFERENCES `newpurchase_item_detail` (`id`),
  CONSTRAINT `newpurchase_item_sto_purchase_order_id_afd7f5b1_fk_newpurcha` FOREIGN KEY (`purchase_order_id`) REFERENCES `newpurchase` (`id`),
  CONSTRAINT `newpurchase_item_sto_stone_rate_type_id_66c744aa_fk_rate_type` FOREIGN KEY (`stone_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `newpurchase_item_sto_stone_weight_type_id_0d517f0c_fk_stone_wei` FOREIGN KEY (`stone_weight_type_id`) REFERENCES `stone_weight_type` (`id`),
  CONSTRAINT `newpurchase_item_stone_stone_name_id_bcccfa20_fk_stone_detail_id` FOREIGN KEY (`stone_name_id`) REFERENCES `stone_detail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `newpurchase_item_stone`
--

LOCK TABLES `newpurchase_item_stone` WRITE;
/*!40000 ALTER TABLE `newpurchase_item_stone` DISABLE KEYS */;
/*!40000 ALTER TABLE `newpurchase_item_stone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `old_gold_type`
--

DROP TABLE IF EXISTS `old_gold_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `old_gold_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_name` (`type_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `old_gold_type`
--

LOCK TABLES `old_gold_type` WRITE;
/*!40000 ALTER TABLE `old_gold_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `old_gold_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `old_metal_category`
--

DROP TABLE IF EXISTS `old_metal_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `old_metal_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `old_metal_category`
--

LOCK TABLES `old_metal_category` WRITE;
/*!40000 ALTER TABLE `old_metal_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `old_metal_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_management_order_detail`
--

DROP TABLE IF EXISTS `order_management_order_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_management_order_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_date` date NOT NULL,
  `no_of_days` int NOT NULL,
  `due_date` date NOT NULL,
  `customer_name` varchar(50) DEFAULT NULL,
  `total_weight` double NOT NULL,
  `total_quantity` int NOT NULL,
  `approximate_amount` double NOT NULL,
  `is_order_scheduled` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `branch_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `customer_id` bigint DEFAULT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  `order_for_id` bigint NOT NULL,
  `order_id_id` bigint NOT NULL,
  `order_status_id` bigint NOT NULL,
  `payment_status_id` bigint NOT NULL,
  `priority_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id_id` (`order_id_id`),
  KEY `order_management_order_detail_branch_id_95997ff7_fk_branches_id` (`branch_id`),
  KEY `order_management_order_detail_created_by_id_c02452f0_fk_users_id` (`created_by_id`),
  KEY `order_management_ord_customer_id_1d8165ed_fk_customer_` (`customer_id`),
  KEY `order_management_orde_modified_by_id_19e20491_fk_users_id` (`modified_by_id`),
  KEY `order_management_ord_order_for_id_6a562d3e_fk_order_man` (`order_for_id`),
  KEY `order_management_ord_order_status_id_e4376ece_fk_status_ta` (`order_status_id`),
  KEY `order_management_ord_payment_status_id_617b3032_fk_payment_s` (`payment_status_id`),
  KEY `order_management_ord_priority_id_bec8f8c7_fk_order_man` (`priority_id`),
  CONSTRAINT `order_management_ord_customer_id_1d8165ed_fk_customer_` FOREIGN KEY (`customer_id`) REFERENCES `customer_details` (`id`),
  CONSTRAINT `order_management_ord_order_for_id_6a562d3e_fk_order_man` FOREIGN KEY (`order_for_id`) REFERENCES `order_management_order_for` (`id`),
  CONSTRAINT `order_management_ord_order_id_id_954d1adc_fk_order_man` FOREIGN KEY (`order_id_id`) REFERENCES `order_management_order_id` (`id`),
  CONSTRAINT `order_management_ord_order_status_id_e4376ece_fk_status_ta` FOREIGN KEY (`order_status_id`) REFERENCES `status_table` (`id`),
  CONSTRAINT `order_management_ord_payment_status_id_617b3032_fk_payment_s` FOREIGN KEY (`payment_status_id`) REFERENCES `payment_status` (`id`),
  CONSTRAINT `order_management_ord_priority_id_bec8f8c7_fk_order_man` FOREIGN KEY (`priority_id`) REFERENCES `order_management_priority` (`id`),
  CONSTRAINT `order_management_orde_modified_by_id_19e20491_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `order_management_order_detail_branch_id_95997ff7_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `order_management_order_detail_created_by_id_c02452f0_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_management_order_detail`
--

LOCK TABLES `order_management_order_detail` WRITE;
/*!40000 ALTER TABLE `order_management_order_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_management_order_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_management_order_for`
--

DROP TABLE IF EXISTS `order_management_order_for`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_management_order_for` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_management_order_for_created_by_id_991b0385_fk_users_id` (`created_by_id`),
  CONSTRAINT `order_management_order_for_created_by_id_991b0385_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_management_order_for`
--

LOCK TABLES `order_management_order_for` WRITE;
/*!40000 ALTER TABLE `order_management_order_for` DISABLE KEYS */;
INSERT INTO `order_management_order_for` VALUES (1,'shop',1,NULL,NULL),(2,'Customer',1,NULL,NULL);
/*!40000 ALTER TABLE `order_management_order_for` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_management_order_id`
--

DROP TABLE IF EXISTS `order_management_order_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_management_order_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  KEY `order_management_order_id_created_by_id_7129194f_fk_users_id` (`created_by_id`),
  CONSTRAINT `order_management_order_id_created_by_id_7129194f_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_management_order_id`
--

LOCK TABLES `order_management_order_id` WRITE;
/*!40000 ALTER TABLE `order_management_order_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_management_order_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_management_order_issue`
--

DROP TABLE IF EXISTS `order_management_order_issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_management_order_issue` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `issue_date` date NOT NULL,
  `no_of_days` int NOT NULL,
  `remainder_date` date NOT NULL,
  `paid_amount` double DEFAULT NULL,
  `paid_weight` double DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  `order_id_id` bigint NOT NULL,
  `order_item_id` bigint NOT NULL,
  `payment_status_id` bigint NOT NULL,
  `vendor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_item_id` (`order_item_id`),
  KEY `order_management_order_issue_created_by_id_d9a1e1df_fk_users_id` (`created_by_id`),
  KEY `order_management_order_issue_modified_by_id_218bdd1f_fk_users_id` (`modified_by_id`),
  KEY `order_management_ord_order_id_id_f2cf3be9_fk_order_man` (`order_id_id`),
  KEY `order_management_ord_payment_status_id_af37e3b1_fk_payment_s` (`payment_status_id`),
  KEY `order_management_ord_vendor_id_a205a427_fk_account_h` (`vendor_id`),
  CONSTRAINT `order_management_ord_order_id_id_f2cf3be9_fk_order_man` FOREIGN KEY (`order_id_id`) REFERENCES `order_management_order_id` (`id`),
  CONSTRAINT `order_management_ord_order_item_id_df4da258_fk_order_man` FOREIGN KEY (`order_item_id`) REFERENCES `order_management_order_item` (`id`),
  CONSTRAINT `order_management_ord_payment_status_id_af37e3b1_fk_payment_s` FOREIGN KEY (`payment_status_id`) REFERENCES `payment_status` (`id`),
  CONSTRAINT `order_management_ord_vendor_id_a205a427_fk_account_h` FOREIGN KEY (`vendor_id`) REFERENCES `account_head` (`id`),
  CONSTRAINT `order_management_order_issue_created_by_id_d9a1e1df_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `order_management_order_issue_modified_by_id_218bdd1f_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_management_order_issue`
--

LOCK TABLES `order_management_order_issue` WRITE;
/*!40000 ALTER TABLE `order_management_order_issue` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_management_order_issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_management_order_item`
--

DROP TABLE IF EXISTS `order_management_order_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_management_order_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `gross_weight` double NOT NULL,
  `net_weight` double NOT NULL,
  `metal_rate` double NOT NULL,
  `measurement_value` varchar(50) DEFAULT NULL,
  `total_stone_weight` double NOT NULL,
  `total_stone_pieces` int NOT NULL,
  `total_stone_amount` double NOT NULL,
  `stone_description` varchar(500) DEFAULT NULL,
  `total_diamond_weight` double NOT NULL,
  `total_diamond_pieces` int NOT NULL,
  `total_diamond_amount` double NOT NULL,
  `diamond_description` varchar(500) DEFAULT NULL,
  `actual_amount` double NOT NULL,
  `total_amount` double NOT NULL,
  `is_assigned` tinyint(1) NOT NULL,
  `is_recieved` tinyint(1) NOT NULL,
  `is_delivered` tinyint(1) NOT NULL,
  `delivered_at` datetime(6) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `assigned_by_id` bigint DEFAULT NULL,
  `gender_id` bigint NOT NULL,
  `item_id` bigint NOT NULL,
  `measurement_type_id` bigint DEFAULT NULL,
  `metal_id` bigint NOT NULL,
  `order_id_id` bigint NOT NULL,
  `order_status_id` bigint NOT NULL,
  `purity_id` bigint NOT NULL,
  `sub_item_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_management_order_item_assigned_by_id_400f80f9_fk_users_id` (`assigned_by_id`),
  KEY `order_management_ord_gender_id_caa34efc_fk_settings_` (`gender_id`),
  KEY `order_management_order_item_item_id_f051a5f2_fk_item_detail_id` (`item_id`),
  KEY `order_management_ord_measurement_type_id_56e17ae4_fk_measureme` (`measurement_type_id`),
  KEY `order_management_order_item_metal_id_f986bca1_fk_metals_id` (`metal_id`),
  KEY `order_management_ord_order_id_id_1f1bad57_fk_order_man` (`order_id_id`),
  KEY `order_management_ord_order_status_id_20f79bb7_fk_status_ta` (`order_status_id`),
  KEY `order_management_order_item_purity_id_38d00556_fk_purities_id` (`purity_id`),
  KEY `order_management_ord_sub_item_id_cb81f346_fk_sub_item_` (`sub_item_id`),
  CONSTRAINT `order_management_ord_gender_id_caa34efc_fk_settings_` FOREIGN KEY (`gender_id`) REFERENCES `settings_gender` (`id`),
  CONSTRAINT `order_management_ord_measurement_type_id_56e17ae4_fk_measureme` FOREIGN KEY (`measurement_type_id`) REFERENCES `measurement_type` (`id`),
  CONSTRAINT `order_management_ord_order_id_id_1f1bad57_fk_order_man` FOREIGN KEY (`order_id_id`) REFERENCES `order_management_order_id` (`id`),
  CONSTRAINT `order_management_ord_order_status_id_20f79bb7_fk_status_ta` FOREIGN KEY (`order_status_id`) REFERENCES `status_table` (`id`),
  CONSTRAINT `order_management_ord_sub_item_id_cb81f346_fk_sub_item_` FOREIGN KEY (`sub_item_id`) REFERENCES `sub_item_detail` (`id`),
  CONSTRAINT `order_management_order_item_assigned_by_id_400f80f9_fk_users_id` FOREIGN KEY (`assigned_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `order_management_order_item_item_id_f051a5f2_fk_item_detail_id` FOREIGN KEY (`item_id`) REFERENCES `item_detail` (`id`),
  CONSTRAINT `order_management_order_item_metal_id_f986bca1_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `order_management_order_item_purity_id_38d00556_fk_purities_id` FOREIGN KEY (`purity_id`) REFERENCES `purities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_management_order_item`
--

LOCK TABLES `order_management_order_item` WRITE;
/*!40000 ALTER TABLE `order_management_order_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_management_order_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_management_order_item_attachement`
--

DROP TABLE IF EXISTS `order_management_order_item_attachement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_management_order_item_attachement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` varchar(100) NOT NULL,
  `order_item` varchar(100) NOT NULL,
  `image` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_management_order_item_attachement`
--

LOCK TABLES `order_management_order_item_attachement` WRITE;
/*!40000 ALTER TABLE `order_management_order_item_attachement` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_management_order_item_attachement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_management_priority`
--

DROP TABLE IF EXISTS `order_management_priority`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_management_priority` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_management_priority_created_by_id_02ab2045_fk_users_id` (`created_by_id`),
  CONSTRAINT `order_management_priority_created_by_id_02ab2045_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_management_priority`
--

LOCK TABLES `order_management_priority` WRITE;
/*!40000 ALTER TABLE `order_management_priority` DISABLE KEYS */;
INSERT INTO `order_management_priority` VALUES (1,'Low',1,NULL,NULL),(2,'Medium',1,NULL,NULL),(3,'High',1,NULL,NULL);
/*!40000 ALTER TABLE `order_management_priority` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_management_session_order_id`
--

DROP TABLE IF EXISTS `order_management_session_order_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_management_session_order_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ses_order_id_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ses_order_id_id` (`ses_order_id_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `order_management_ses_ses_order_id_id_b0225009_fk_order_man` FOREIGN KEY (`ses_order_id_id`) REFERENCES `order_management_order_id` (`id`),
  CONSTRAINT `order_management_session_order_id_user_id_0b38bc80_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_management_session_order_id`
--

LOCK TABLES `order_management_session_order_id` WRITE;
/*!40000 ALTER TABLE `order_management_session_order_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_management_session_order_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_method`
--

DROP TABLE IF EXISTS `payment_method`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_method` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_method_name` varchar(50) NOT NULL,
  `color` varchar(50) NOT NULL,
  `bg_color` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `payment_method_name` (`payment_method_name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_method`
--

LOCK TABLES `payment_method` WRITE;
/*!40000 ALTER TABLE `payment_method` DISABLE KEYS */;
INSERT INTO `payment_method` VALUES (1,'Cash','#1D1D1D','#E2E8F0'),(2,'UPI','#1D1D1D','#E2E8F0'),(3,'Card','#1D1D1D','#E2E8F0'),(4,'Bank','#1D1D1D','#E2E8F0'),(5,'Scheme','#FFFFFF','#1E4E87');
/*!40000 ALTER TABLE `payment_method` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_mode`
--

DROP TABLE IF EXISTS `payment_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_mode` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `mode_name` varchar(50) NOT NULL,
  `short_code` varchar(50) NOT NULL,
  `color` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_mode`
--

LOCK TABLES `payment_mode` WRITE;
/*!40000 ALTER TABLE `payment_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_module`
--

DROP TABLE IF EXISTS `payment_module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_module` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `module_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `module_name` (`module_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_module`
--

LOCK TABLES `payment_module` WRITE;
/*!40000 ALTER TABLE `payment_module` DISABLE KEYS */;
INSERT INTO `payment_module` VALUES (3,'Billing'),(1,'Order'),(2,'Repair');
/*!40000 ALTER TABLE `payment_module` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_provider`
--

DROP TABLE IF EXISTS `payment_provider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_provider` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_provider_name` varchar(50) NOT NULL,
  `payment_method_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payment_provider_payment_method_id_fe246798_fk_payment_method_id` (`payment_method_id`),
  CONSTRAINT `payment_provider_payment_method_id_fe246798_fk_payment_method_id` FOREIGN KEY (`payment_method_id`) REFERENCES `payment_method` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_provider`
--

LOCK TABLES `payment_provider` WRITE;
/*!40000 ALTER TABLE `payment_provider` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_provider` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_status`
--

DROP TABLE IF EXISTS `payment_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_status` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status_name` varchar(50) NOT NULL,
  `color` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_status`
--

LOCK TABLES `payment_status` WRITE;
/*!40000 ALTER TABLE `payment_status` DISABLE KEYS */;
INSERT INTO `payment_status` VALUES (1,'Pending','#FFFFFF'),(2,'Partially Paid','#FFFFFF'),(3,'Paid','#FFFFFF');
/*!40000 ALTER TABLE `payment_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_table`
--

DROP TABLE IF EXISTS `payment_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_table` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `refference_number` varchar(100) NOT NULL,
  `paid_amount` double NOT NULL,
  `payment_refference_number` varchar(100) DEFAULT NULL,
  `payment_date` datetime(6) DEFAULT NULL,
  `customer_details_id` bigint NOT NULL,
  `payment_method_id` bigint NOT NULL,
  `payment_module_id` bigint NOT NULL,
  `payment_provider_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `payment_table_customer_details_id_96cd6039_fk_customer_` (`customer_details_id`),
  KEY `payment_table_payment_method_id_206b7cef_fk_payment_method_id` (`payment_method_id`),
  KEY `payment_table_payment_module_id_ee653f13_fk_payment_module_id` (`payment_module_id`),
  KEY `payment_table_payment_provider_id_75ce687b_fk_payment_p` (`payment_provider_id`),
  CONSTRAINT `payment_table_customer_details_id_96cd6039_fk_customer_` FOREIGN KEY (`customer_details_id`) REFERENCES `customer_details` (`id`),
  CONSTRAINT `payment_table_payment_method_id_206b7cef_fk_payment_method_id` FOREIGN KEY (`payment_method_id`) REFERENCES `payment_method` (`id`),
  CONSTRAINT `payment_table_payment_module_id_ee653f13_fk_payment_module_id` FOREIGN KEY (`payment_module_id`) REFERENCES `payment_module` (`id`),
  CONSTRAINT `payment_table_payment_provider_id_75ce687b_fk_payment_p` FOREIGN KEY (`payment_provider_id`) REFERENCES `payment_provider` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_table`
--

LOCK TABLES `payment_table` WRITE;
/*!40000 ALTER TABLE `payment_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `per_gram_rate`
--

DROP TABLE IF EXISTS `per_gram_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `per_gram_rate` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `per_gram_rate` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `item_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `per_gram_rate_created_by_id_16392acb_fk_users_id` (`created_by_id`),
  KEY `per_gram_rate_item_details_id_4289611d_fk_item_detail_id` (`item_details_id`),
  CONSTRAINT `per_gram_rate_created_by_id_16392acb_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `per_gram_rate_item_details_id_4289611d_fk_item_detail_id` FOREIGN KEY (`item_details_id`) REFERENCES `item_detail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `per_gram_rate`
--

LOCK TABLES `per_gram_rate` WRITE;
/*!40000 ALTER TABLE `per_gram_rate` DISABLE KEYS */;
/*!40000 ALTER TABLE `per_gram_rate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `print_module`
--

DROP TABLE IF EXISTS `print_module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `print_module` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `estimation_is_a4` tinyint(1) NOT NULL,
  `billing_is_a4` tinyint(1) NOT NULL,
  `billing_backup_is_a4` tinyint(1) NOT NULL,
  `order_is_a4` tinyint(1) NOT NULL,
  `repair_is_a4` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `print_module_created_by_id_32abec3b_fk_users_id` (`created_by_id`),
  CONSTRAINT `print_module_created_by_id_32abec3b_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `print_module`
--

LOCK TABLES `print_module` WRITE;
/*!40000 ALTER TABLE `print_module` DISABLE KEYS */;
INSERT INTO `print_module` VALUES (1,1,1,1,1,1,NULL,NULL),(2,1,1,1,1,1,NULL,NULL);
/*!40000 ALTER TABLE `print_module` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_entry`
--

DROP TABLE IF EXISTS `purchase_entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_entry` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bill_no` varchar(100) DEFAULT NULL,
  `po_id` varchar(100) DEFAULT NULL,
  `person_id` int NOT NULL,
  `sgst` double DEFAULT NULL,
  `igst` double DEFAULT NULL,
  `gst` double DEFAULT NULL,
  `total_pieces` double DEFAULT NULL,
  `total_netweight` double DEFAULT NULL,
  `total_grossweight` double DEFAULT NULL,
  `sub_total` double DEFAULT NULL,
  `total_amount` double DEFAULT NULL,
  `total_stone_amount` double DEFAULT NULL,
  `hallmark_amount` double DEFAULT NULL,
  `mc_amount` double DEFAULT NULL,
  `purchase_date` date DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `branch_id` bigint DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `purchase_person_type_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_entry_purchase_person_type_0b001683_fk_purchase_` (`purchase_person_type_id`),
  KEY `purchase_entry_branch_id_1017ca2e_fk_branches_id` (`branch_id`),
  KEY `purchase_entry_created_by_id_7edf16cf_fk_users_id` (`created_by_id`),
  CONSTRAINT `purchase_entry_branch_id_1017ca2e_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `purchase_entry_created_by_id_7edf16cf_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `purchase_entry_purchase_person_type_0b001683_fk_purchase_` FOREIGN KEY (`purchase_person_type_id`) REFERENCES `purchase_person_types` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_entry`
--

LOCK TABLES `purchase_entry` WRITE;
/*!40000 ALTER TABLE `purchase_entry` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_entry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_item_detail`
--

DROP TABLE IF EXISTS `purchase_item_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_item_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `purchase_item` int DEFAULT NULL,
  `purchase_subitem` int DEFAULT NULL,
  `pieces` varchar(100) DEFAULT NULL,
  `stone_pieces` varchar(100) DEFAULT NULL,
  `stone_weight` double DEFAULT NULL,
  `diamond_pieces` varchar(100) DEFAULT NULL,
  `diamond_weight` double DEFAULT NULL,
  `gross_weight` double DEFAULT NULL,
  `less_weight` double DEFAULT NULL,
  `net_weight` double DEFAULT NULL,
  `total_amount` double DEFAULT NULL,
  `purchase_metal_id` bigint DEFAULT NULL,
  `purchase_purity_id` bigint DEFAULT NULL,
  `purchaseentry_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_item_detail_purchase_metal_id_2f20ebbf_fk_metals_id` (`purchase_metal_id`),
  KEY `purchase_item_detail_purchase_purity_id_2d6ca7de_fk_purities_id` (`purchase_purity_id`),
  KEY `purchase_item_detail_purchaseentry_id_98be13e2_fk_purchase_` (`purchaseentry_id`),
  CONSTRAINT `purchase_item_detail_purchase_metal_id_2f20ebbf_fk_metals_id` FOREIGN KEY (`purchase_metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `purchase_item_detail_purchase_purity_id_2d6ca7de_fk_purities_id` FOREIGN KEY (`purchase_purity_id`) REFERENCES `purities` (`id`),
  CONSTRAINT `purchase_item_detail_purchaseentry_id_98be13e2_fk_purchase_` FOREIGN KEY (`purchaseentry_id`) REFERENCES `purchase_entry` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_item_detail`
--

LOCK TABLES `purchase_item_detail` WRITE;
/*!40000 ALTER TABLE `purchase_item_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_item_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_item_diamond`
--

DROP TABLE IF EXISTS `purchase_item_diamond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_item_diamond` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `diamond_pieces` int DEFAULT NULL,
  `diamond_weight` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `include_diamond_weight` tinyint(1) NOT NULL,
  `total_diamond_value` double DEFAULT NULL,
  `diamond_name_id` bigint NOT NULL,
  `diamond_rate_type_id` bigint NOT NULL,
  `diamond_weight_type_id` bigint NOT NULL,
  `purchase_item_id` bigint DEFAULT NULL,
  `purchaseentry_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_item_diamon_diamond_name_id_f9caf41a_fk_stone_det` (`diamond_name_id`),
  KEY `purchase_item_diamon_diamond_rate_type_id_983daca8_fk_rate_type` (`diamond_rate_type_id`),
  KEY `purchase_item_diamon_diamond_weight_type__4e3d3a82_fk_stone_wei` (`diamond_weight_type_id`),
  KEY `purchase_item_diamon_purchase_item_id_78ef80ef_fk_purchase_` (`purchase_item_id`),
  KEY `purchase_item_diamon_purchaseentry_id_9f587823_fk_purchase_` (`purchaseentry_id`),
  CONSTRAINT `purchase_item_diamon_diamond_name_id_f9caf41a_fk_stone_det` FOREIGN KEY (`diamond_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `purchase_item_diamon_diamond_rate_type_id_983daca8_fk_rate_type` FOREIGN KEY (`diamond_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `purchase_item_diamon_diamond_weight_type__4e3d3a82_fk_stone_wei` FOREIGN KEY (`diamond_weight_type_id`) REFERENCES `stone_weight_type` (`id`),
  CONSTRAINT `purchase_item_diamon_purchase_item_id_78ef80ef_fk_purchase_` FOREIGN KEY (`purchase_item_id`) REFERENCES `purchase_item_detail` (`id`),
  CONSTRAINT `purchase_item_diamon_purchaseentry_id_9f587823_fk_purchase_` FOREIGN KEY (`purchaseentry_id`) REFERENCES `purchase_entry` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_item_diamond`
--

LOCK TABLES `purchase_item_diamond` WRITE;
/*!40000 ALTER TABLE `purchase_item_diamond` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_item_diamond` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_item_stone`
--

DROP TABLE IF EXISTS `purchase_item_stone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_item_stone` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stone_pieces` int DEFAULT NULL,
  `stone_weight` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `include_stone_weight` tinyint(1) NOT NULL,
  `total_stone_value` double DEFAULT NULL,
  `purchase_item_id` bigint DEFAULT NULL,
  `purchaseentry_id` bigint DEFAULT NULL,
  `stone_name_id` bigint NOT NULL,
  `stone_rate_type_id` bigint NOT NULL,
  `stone_weight_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_item_stone_purchase_item_id_877faa70_fk_purchase_` (`purchase_item_id`),
  KEY `purchase_item_stone_purchaseentry_id_2c7fd96f_fk_purchase_` (`purchaseentry_id`),
  KEY `purchase_item_stone_stone_name_id_f9f4be48_fk_stone_detail_id` (`stone_name_id`),
  KEY `purchase_item_stone_stone_rate_type_id_b638a79e_fk_rate_type_id` (`stone_rate_type_id`),
  KEY `purchase_item_stone_stone_weight_type_id_8a1287d8_fk_stone_wei` (`stone_weight_type_id`),
  CONSTRAINT `purchase_item_stone_purchase_item_id_877faa70_fk_purchase_` FOREIGN KEY (`purchase_item_id`) REFERENCES `purchase_item_detail` (`id`),
  CONSTRAINT `purchase_item_stone_purchaseentry_id_2c7fd96f_fk_purchase_` FOREIGN KEY (`purchaseentry_id`) REFERENCES `purchase_entry` (`id`),
  CONSTRAINT `purchase_item_stone_stone_name_id_f9f4be48_fk_stone_detail_id` FOREIGN KEY (`stone_name_id`) REFERENCES `stone_detail` (`id`),
  CONSTRAINT `purchase_item_stone_stone_rate_type_id_b638a79e_fk_rate_type_id` FOREIGN KEY (`stone_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `purchase_item_stone_stone_weight_type_id_8a1287d8_fk_stone_wei` FOREIGN KEY (`stone_weight_type_id`) REFERENCES `stone_weight_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_item_stone`
--

LOCK TABLES `purchase_item_stone` WRITE;
/*!40000 ALTER TABLE `purchase_item_stone` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_item_stone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_payment`
--

DROP TABLE IF EXISTS `purchase_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `paid_amount` double DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `purchase_paymode_id` bigint DEFAULT NULL,
  `purchaseentry_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_payment_created_by_id_cc094787_fk_users_id` (`created_by_id`),
  KEY `purchase_payment_purchase_paymode_id_5e559899_fk_payment_mode_id` (`purchase_paymode_id`),
  KEY `purchase_payment_purchaseentry_id_b3a9930e_fk_purchase_entry_id` (`purchaseentry_id`),
  CONSTRAINT `purchase_payment_created_by_id_cc094787_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `purchase_payment_purchase_paymode_id_5e559899_fk_payment_mode_id` FOREIGN KEY (`purchase_paymode_id`) REFERENCES `payment_mode` (`id`),
  CONSTRAINT `purchase_payment_purchaseentry_id_b3a9930e_fk_purchase_entry_id` FOREIGN KEY (`purchaseentry_id`) REFERENCES `purchase_entry` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_payment`
--

LOCK TABLES `purchase_payment` WRITE;
/*!40000 ALTER TABLE `purchase_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_person_types`
--

DROP TABLE IF EXISTS `purchase_person_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_person_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `purchase_person_name` varchar(55) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `purchase_person_name` (`purchase_person_name`),
  KEY `purchase_person_types_created_by_id_458c8ae1_fk_users_id` (`created_by_id`),
  CONSTRAINT `purchase_person_types_created_by_id_458c8ae1_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_person_types`
--

LOCK TABLES `purchase_person_types` WRITE;
/*!40000 ALTER TABLE `purchase_person_types` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_person_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_tax_detail`
--

DROP TABLE IF EXISTS `purchase_tax_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_tax_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `purchase_tax_igst` double NOT NULL,
  `purchase_tax_cgst` double NOT NULL,
  `purchase_tax_sgst` double NOT NULL,
  `purchase_surcharge_percent` double NOT NULL,
  `purchase_additional_charges` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `tax_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_tax_detail_created_by_id_34d54d47_fk_users_id` (`created_by_id`),
  KEY `purchase_tax_detail_tax_details_id_49014d89_fk_tax_detail_id` (`tax_details_id`),
  CONSTRAINT `purchase_tax_detail_created_by_id_34d54d47_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `purchase_tax_detail_tax_details_id_49014d89_fk_tax_detail_id` FOREIGN KEY (`tax_details_id`) REFERENCES `tax_detail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_tax_detail`
--

LOCK TABLES `purchase_tax_detail` WRITE;
/*!40000 ALTER TABLE `purchase_tax_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_tax_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_types`
--

DROP TABLE IF EXISTS `purchase_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `purchase_type_name` varchar(55) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `purchase_type_name` (`purchase_type_name`),
  KEY `purchase_types_created_by_id_6dbd1d8b_fk_users_id` (`created_by_id`),
  CONSTRAINT `purchase_types_created_by_id_6dbd1d8b_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_types`
--

LOCK TABLES `purchase_types` WRITE;
/*!40000 ALTER TABLE `purchase_types` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purification_issue`
--

DROP TABLE IF EXISTS `purification_issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purification_issue` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `purification_issue_id` varchar(100) NOT NULL,
  `issued_date` date NOT NULL,
  `return_days` int NOT NULL,
  `return_date` date NOT NULL,
  `bag_weight` double NOT NULL,
  `recipt_metal_weight` double NOT NULL,
  `issued_pure_weight` double NOT NULL,
  `notes` longtext,
  `issued_at` datetime(6) DEFAULT NULL,
  `branch_id` bigint NOT NULL,
  `issued_by_id` bigint DEFAULT NULL,
  `issued_category_id` bigint NOT NULL,
  `melting_recipt_details_id` bigint NOT NULL,
  `purification_status_id` bigint NOT NULL,
  `smith_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `purification_issue_id` (`purification_issue_id`),
  UNIQUE KEY `melting_recipt_details_id` (`melting_recipt_details_id`),
  KEY `purification_issue_branch_id_6099fb7f_fk_branches_id` (`branch_id`),
  KEY `purification_issue_issued_by_id_be88bd5c_fk_users_id` (`issued_by_id`),
  KEY `purification_issue_issued_category_id_afcf6e30_fk_old_metal` (`issued_category_id`),
  KEY `purification_issue_purification_status__e8eb6720_fk_status_ta` (`purification_status_id`),
  KEY `purification_issue_smith_id_0da70e10_fk_account_head_id` (`smith_id`),
  CONSTRAINT `purification_issue_branch_id_6099fb7f_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `purification_issue_issued_by_id_be88bd5c_fk_users_id` FOREIGN KEY (`issued_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `purification_issue_issued_category_id_afcf6e30_fk_old_metal` FOREIGN KEY (`issued_category_id`) REFERENCES `old_metal_category` (`id`),
  CONSTRAINT `purification_issue_melting_recipt_detai_91bf35ef_fk_melting_r` FOREIGN KEY (`melting_recipt_details_id`) REFERENCES `melting_recipt` (`id`),
  CONSTRAINT `purification_issue_purification_status__e8eb6720_fk_status_ta` FOREIGN KEY (`purification_status_id`) REFERENCES `status_table` (`id`),
  CONSTRAINT `purification_issue_smith_id_0da70e10_fk_account_head_id` FOREIGN KEY (`smith_id`) REFERENCES `account_head` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purification_issue`
--

LOCK TABLES `purification_issue` WRITE;
/*!40000 ALTER TABLE `purification_issue` DISABLE KEYS */;
/*!40000 ALTER TABLE `purification_issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purification_issue_id`
--

DROP TABLE IF EXISTS `purification_issue_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purification_issue_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `purification_issue_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `purification_issue_id` (`purification_issue_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purification_issue_id`
--

LOCK TABLES `purification_issue_id` WRITE;
/*!40000 ALTER TABLE `purification_issue_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `purification_issue_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purification_issue_number`
--

DROP TABLE IF EXISTS `purification_issue_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purification_issue_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `purification_issue_number` varchar(50) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `purification_issue_number` (`purification_issue_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `purification_issue_number_user_id_a944813b_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purification_issue_number`
--

LOCK TABLES `purification_issue_number` WRITE;
/*!40000 ALTER TABLE `purification_issue_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `purification_issue_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purification_recipt`
--

DROP TABLE IF EXISTS `purification_recipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purification_recipt` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `putification_recipt_id` varchar(50) NOT NULL,
  `received_date` date NOT NULL,
  `issued_weight` double NOT NULL,
  `issued_pure_weight` double NOT NULL,
  `received_pure_weight` double NOT NULL,
  `touch` double NOT NULL,
  `melting_bullion_rate` double NOT NULL,
  `purification_charges` double NOT NULL,
  `amount_paid` double NOT NULL,
  `received_at` datetime(6) DEFAULT NULL,
  `branch_id` bigint NOT NULL,
  `payment_status_id` bigint NOT NULL,
  `purification_issue_details_id` bigint NOT NULL,
  `purification_status_id` bigint NOT NULL,
  `received_by_id` bigint DEFAULT NULL,
  `received_category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `putification_recipt_id` (`putification_recipt_id`),
  UNIQUE KEY `purification_issue_details_id` (`purification_issue_details_id`),
  KEY `purification_recipt_branch_id_4d017b49_fk_branches_id` (`branch_id`),
  KEY `purification_recipt_payment_status_id_1f1732c7_fk_status_ta` (`payment_status_id`),
  KEY `purification_recipt_purification_status__38418f34_fk_status_ta` (`purification_status_id`),
  KEY `purification_recipt_received_by_id_fdc6c0ce_fk_users_id` (`received_by_id`),
  KEY `purification_recipt_received_category_id_e96c7593_fk_old_metal` (`received_category_id`),
  CONSTRAINT `purification_recipt_branch_id_4d017b49_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `purification_recipt_payment_status_id_1f1732c7_fk_status_ta` FOREIGN KEY (`payment_status_id`) REFERENCES `status_table` (`id`),
  CONSTRAINT `purification_recipt_purification_issue_d_2e5cf6b6_fk_purificat` FOREIGN KEY (`purification_issue_details_id`) REFERENCES `purification_issue` (`id`),
  CONSTRAINT `purification_recipt_purification_status__38418f34_fk_status_ta` FOREIGN KEY (`purification_status_id`) REFERENCES `status_table` (`id`),
  CONSTRAINT `purification_recipt_received_by_id_fdc6c0ce_fk_users_id` FOREIGN KEY (`received_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `purification_recipt_received_category_id_e96c7593_fk_old_metal` FOREIGN KEY (`received_category_id`) REFERENCES `old_metal_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purification_recipt`
--

LOCK TABLES `purification_recipt` WRITE;
/*!40000 ALTER TABLE `purification_recipt` DISABLE KEYS */;
/*!40000 ALTER TABLE `purification_recipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purification_recipt_id`
--

DROP TABLE IF EXISTS `purification_recipt_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purification_recipt_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `purification_recipt_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `purification_recipt_id` (`purification_recipt_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purification_recipt_id`
--

LOCK TABLES `purification_recipt_id` WRITE;
/*!40000 ALTER TABLE `purification_recipt_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `purification_recipt_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purification_recipt_number`
--

DROP TABLE IF EXISTS `purification_recipt_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purification_recipt_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `purification_recipt_number` varchar(50) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `purification_recipt_number` (`purification_recipt_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `purification_recipt_number_user_id_b2ae92fd_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purification_recipt_number`
--

LOCK TABLES `purification_recipt_number` WRITE;
/*!40000 ALTER TABLE `purification_recipt_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `purification_recipt_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purities`
--

DROP TABLE IF EXISTS `purities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purities` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `purity_name` varchar(100) NOT NULL,
  `purity_code` varchar(10) NOT NULL,
  `purrity_percent` double NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_visible` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `metal_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `purity_code` (`purity_code`),
  KEY `purities_created_by_id_cc496cfe_fk_users_id` (`created_by_id`),
  KEY `purities_metal_id_20e24704_fk_metals_id` (`metal_id`),
  CONSTRAINT `purities_created_by_id_cc496cfe_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `purities_metal_id_20e24704_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purities`
--

LOCK TABLES `purities` WRITE;
/*!40000 ALTER TABLE `purities` DISABLE KEYS */;
/*!40000 ALTER TABLE `purities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `range_stock`
--

DROP TABLE IF EXISTS `range_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `range_stock` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `from_weight` double NOT NULL,
  `to_weight` double NOT NULL,
  `range_value` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `item_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `range_stock_created_by_id_c86dab3b_fk_users_id` (`created_by_id`),
  KEY `range_stock_item_details_id_218a3825_fk_item_detail_id` (`item_details_id`),
  CONSTRAINT `range_stock_created_by_id_c86dab3b_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `range_stock_item_details_id_218a3825_fk_item_detail_id` FOREIGN KEY (`item_details_id`) REFERENCES `item_detail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `range_stock`
--

LOCK TABLES `range_stock` WRITE;
/*!40000 ALTER TABLE `range_stock` DISABLE KEYS */;
/*!40000 ALTER TABLE `range_stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rate_type`
--

DROP TABLE IF EXISTS `rate_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rate_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type_name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_name` (`type_name`),
  KEY `rate_type_created_by_id_4e17e59a_fk_users_id` (`created_by_id`),
  CONSTRAINT `rate_type_created_by_id_4e17e59a_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rate_type`
--

LOCK TABLES `rate_type` WRITE;
/*!40000 ALTER TABLE `rate_type` DISABLE KEYS */;
INSERT INTO `rate_type` VALUES (1,'Gross Weight',1,NULL,NULL,NULL,NULL),(2,'Net Weight',1,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `rate_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `received_items`
--

DROP TABLE IF EXISTS `received_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `received_items` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `received_date` date DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `transfer_itemid` bigint DEFAULT NULL,
  `transfer_status` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `received_items_transfer_itemid_58cc5440_fk_transerfer_items_id` (`transfer_itemid`),
  KEY `received_items_transfer_status_15744d66_fk_transferstatus_id` (`transfer_status`),
  KEY `received_items_created_by_id_a5c8cf0b_fk_users_id` (`created_by_id`),
  CONSTRAINT `received_items_created_by_id_a5c8cf0b_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `received_items_transfer_itemid_58cc5440_fk_transerfer_items_id` FOREIGN KEY (`transfer_itemid`) REFERENCES `transerfer_items` (`id`),
  CONSTRAINT `received_items_transfer_status_15744d66_fk_transferstatus_id` FOREIGN KEY (`transfer_status`) REFERENCES `transferstatus` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `received_items`
--

LOCK TABLES `received_items` WRITE;
/*!40000 ALTER TABLE `received_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `received_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receiveditem_details`
--

DROP TABLE IF EXISTS `receiveditem_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receiveditem_details` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_number` varchar(255) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `received_itemid` bigint NOT NULL,
  `tagitems_id` bigint NOT NULL,
  `transfer_itemid` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `receiveditem_details_created_by_id_dfb77e69_fk_users_id` (`created_by_id`),
  KEY `receiveditem_details_received_itemid_ee65c7d0_fk_received_` (`received_itemid`),
  KEY `receiveditem_details_tagitems_id_2aa0dc05_fk_tagged_item_id` (`tagitems_id`),
  KEY `receiveditem_details_transfer_itemid_1fca7137_fk_transerfe` (`transfer_itemid`),
  CONSTRAINT `receiveditem_details_created_by_id_dfb77e69_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `receiveditem_details_received_itemid_ee65c7d0_fk_received_` FOREIGN KEY (`received_itemid`) REFERENCES `received_items` (`id`),
  CONSTRAINT `receiveditem_details_tagitems_id_2aa0dc05_fk_tagged_item_id` FOREIGN KEY (`tagitems_id`) REFERENCES `tagged_item` (`id`),
  CONSTRAINT `receiveditem_details_transfer_itemid_1fca7137_fk_transerfe` FOREIGN KEY (`transfer_itemid`) REFERENCES `transerfer_items` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receiveditem_details`
--

LOCK TABLES `receiveditem_details` WRITE;
/*!40000 ALTER TABLE `receiveditem_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `receiveditem_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repair_detail`
--

DROP TABLE IF EXISTS `repair_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `repair_number` varchar(20) NOT NULL,
  `repair_recived_date` date NOT NULL,
  `est_repair_delivery_days` int DEFAULT NULL,
  `est_repair_delivery_date` date NOT NULL,
  `total_issued_weight` int DEFAULT NULL,
  `total_customer_charges` int DEFAULT NULL,
  `total_vendor_charges` int DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(20) DEFAULT NULL,
  `branch_id` bigint DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `customer_details_id` bigint DEFAULT NULL,
  `payment_status_id` bigint DEFAULT NULL,
  `repair_for_id` bigint NOT NULL,
  `status_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `repair_number` (`repair_number`),
  KEY `repair_detail_repair_for_id_3fd2cdcd_fk_repair_for_id` (`repair_for_id`),
  KEY `repair_detail_status_id_5d7e22a5_fk_status_table_id` (`status_id`),
  KEY `repair_detail_branch_id_6e2d8fd6_fk_branches_id` (`branch_id`),
  KEY `repair_detail_created_by_id_088427d3_fk_users_id` (`created_by_id`),
  KEY `repair_detail_customer_details_id_07a989e4_fk_customer_` (`customer_details_id`),
  KEY `repair_detail_payment_status_id_e152111c_fk_payment_status_id` (`payment_status_id`),
  CONSTRAINT `repair_detail_branch_id_6e2d8fd6_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `repair_detail_created_by_id_088427d3_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `repair_detail_customer_details_id_07a989e4_fk_customer_` FOREIGN KEY (`customer_details_id`) REFERENCES `customer_details` (`id`),
  CONSTRAINT `repair_detail_payment_status_id_e152111c_fk_payment_status_id` FOREIGN KEY (`payment_status_id`) REFERENCES `payment_status` (`id`),
  CONSTRAINT `repair_detail_repair_for_id_3fd2cdcd_fk_repair_for_id` FOREIGN KEY (`repair_for_id`) REFERENCES `repair_for` (`id`),
  CONSTRAINT `repair_detail_status_id_5d7e22a5_fk_status_table_id` FOREIGN KEY (`status_id`) REFERENCES `status_table` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repair_detail`
--

LOCK TABLES `repair_detail` WRITE;
/*!40000 ALTER TABLE `repair_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `repair_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repair_for`
--

DROP TABLE IF EXISTS `repair_for`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair_for` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `repair_for` varchar(20) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(20) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `repair_for` (`repair_for`),
  KEY `repair_for_created_by_id_df5fa19d_fk_users_id` (`created_by_id`),
  CONSTRAINT `repair_for_created_by_id_df5fa19d_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repair_for`
--

LOCK TABLES `repair_for` WRITE;
/*!40000 ALTER TABLE `repair_for` DISABLE KEYS */;
INSERT INTO `repair_for` VALUES (1,'shop',NULL,NULL,NULL,NULL),(2,'Customer',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `repair_for` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repair_item_detail`
--

DROP TABLE IF EXISTS `repair_item_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair_item_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `issued_gross_weight` double DEFAULT NULL,
  `issued_net_weight` double DEFAULT NULL,
  `added_net_weight` double DEFAULT NULL,
  `less_weight` double DEFAULT NULL,
  `old_stone` int DEFAULT NULL,
  `old_diamond` int DEFAULT NULL,
  `total_pieces` int DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `customer_charges` int DEFAULT NULL,
  `vendor_charges` int DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(20) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `item_details_id` bigint NOT NULL,
  `metal_details_id` bigint NOT NULL,
  `repair_order_details_id` bigint NOT NULL,
  `repair_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `repair_item_detail_created_by_id_2ed7dc8b_fk_users_id` (`created_by_id`),
  KEY `repair_item_detail_item_details_id_ec0d86f2_fk_item_detail_id` (`item_details_id`),
  KEY `repair_item_detail_metal_details_id_c6dda5c0_fk_metals_id` (`metal_details_id`),
  KEY `repair_item_detail_repair_order_details_2f5c61bb_fk_repair_de` (`repair_order_details_id`),
  KEY `repair_item_detail_repair_type_id_9ab111c7_fk_repair_type_id` (`repair_type_id`),
  CONSTRAINT `repair_item_detail_created_by_id_2ed7dc8b_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `repair_item_detail_item_details_id_ec0d86f2_fk_item_detail_id` FOREIGN KEY (`item_details_id`) REFERENCES `item_detail` (`id`),
  CONSTRAINT `repair_item_detail_metal_details_id_c6dda5c0_fk_metals_id` FOREIGN KEY (`metal_details_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `repair_item_detail_repair_order_details_2f5c61bb_fk_repair_de` FOREIGN KEY (`repair_order_details_id`) REFERENCES `repair_detail` (`id`),
  CONSTRAINT `repair_item_detail_repair_type_id_9ab111c7_fk_repair_type_id` FOREIGN KEY (`repair_type_id`) REFERENCES `repair_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repair_item_detail`
--

LOCK TABLES `repair_item_detail` WRITE;
/*!40000 ALTER TABLE `repair_item_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `repair_item_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repair_number`
--

DROP TABLE IF EXISTS `repair_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `repair_number` varchar(20) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(20) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `repair_number` (`repair_number`),
  KEY `repair_number_created_by_id_7df0f6e1_fk_users_id` (`created_by_id`),
  CONSTRAINT `repair_number_created_by_id_7df0f6e1_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repair_number`
--

LOCK TABLES `repair_number` WRITE;
/*!40000 ALTER TABLE `repair_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `repair_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repair_order_issued`
--

DROP TABLE IF EXISTS `repair_order_issued`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair_order_issued` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `issue_date` date DEFAULT NULL,
  `estimate_due_date` date DEFAULT NULL,
  `remainder_days` int DEFAULT NULL,
  `remainder_date` date DEFAULT NULL,
  `paid_amount` double DEFAULT NULL,
  `paid_weight` double DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `payment_status_id` bigint DEFAULT NULL,
  `repair_details_id` bigint NOT NULL,
  `vendor_name_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `repair_order_issued_created_by_id_2c57e3fe_fk_users_id` (`created_by_id`),
  KEY `repair_order_issued_payment_status_id_df1d4016_fk_payment_s` (`payment_status_id`),
  KEY `repair_order_issued_repair_details_id_871f9ca6_fk_repair_de` (`repair_details_id`),
  KEY `repair_order_issued_vendor_name_id_dd6b6e6d_fk_account_head_id` (`vendor_name_id`),
  CONSTRAINT `repair_order_issued_created_by_id_2c57e3fe_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `repair_order_issued_payment_status_id_df1d4016_fk_payment_s` FOREIGN KEY (`payment_status_id`) REFERENCES `payment_status` (`id`),
  CONSTRAINT `repair_order_issued_repair_details_id_871f9ca6_fk_repair_de` FOREIGN KEY (`repair_details_id`) REFERENCES `repair_detail` (`id`),
  CONSTRAINT `repair_order_issued_vendor_name_id_dd6b6e6d_fk_account_head_id` FOREIGN KEY (`vendor_name_id`) REFERENCES `account_head` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repair_order_issued`
--

LOCK TABLES `repair_order_issued` WRITE;
/*!40000 ALTER TABLE `repair_order_issued` DISABLE KEYS */;
/*!40000 ALTER TABLE `repair_order_issued` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repair_order_oldgold`
--

DROP TABLE IF EXISTS `repair_order_oldgold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair_order_oldgold` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `refference_number` varchar(50) NOT NULL,
  `old_gold_no` varchar(100) DEFAULT NULL,
  `gross_weight` double DEFAULT NULL,
  `net_weight` double DEFAULT NULL,
  `dust_weight` double DEFAULT NULL,
  `metal_rate` double DEFAULT NULL,
  `today_metal_rate` double DEFAULT NULL,
  `old_rate` double DEFAULT NULL,
  `total_amount` double DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `metal_id` bigint DEFAULT NULL,
  `purity_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `repair_order_oldgold_created_by_id_7a868063_fk_users_id` (`created_by_id`),
  KEY `repair_order_oldgold_metal_id_5f19fb43_fk_metals_id` (`metal_id`),
  KEY `repair_order_oldgold_purity_id_1898d79d_fk_purities_id` (`purity_id`),
  CONSTRAINT `repair_order_oldgold_created_by_id_7a868063_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `repair_order_oldgold_metal_id_5f19fb43_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `repair_order_oldgold_purity_id_1898d79d_fk_purities_id` FOREIGN KEY (`purity_id`) REFERENCES `purities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repair_order_oldgold`
--

LOCK TABLES `repair_order_oldgold` WRITE;
/*!40000 ALTER TABLE `repair_order_oldgold` DISABLE KEYS */;
/*!40000 ALTER TABLE `repair_order_oldgold` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repair_type`
--

DROP TABLE IF EXISTS `repair_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repair_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `repair_type_name` varchar(30) NOT NULL,
  `min_vendor_charges` double NOT NULL,
  `max_vendor_charges` double NOT NULL,
  `min_customer_charges` double NOT NULL,
  `max_customer_charges` double NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `repair_type_created_by_id_0ae04f8a_fk_users_id` (`created_by_id`),
  KEY `repair_type_modified_by_id_6c90d76e_fk_users_id` (`modified_by_id`),
  CONSTRAINT `repair_type_created_by_id_0ae04f8a_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `repair_type_modified_by_id_6c90d76e_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repair_type`
--

LOCK TABLES `repair_type` WRITE;
/*!40000 ALTER TABLE `repair_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `repair_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `return_items`
--

DROP TABLE IF EXISTS `return_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `return_items` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `return_date` datetime(6) NOT NULL,
  `reason` longtext,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `transfer_itemid` bigint NOT NULL,
  `transfer_status` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `return_items_transfer_itemid_5b701d15_fk_transerfer_items_id` (`transfer_itemid`),
  KEY `return_items_transfer_status_9b122186_fk_transferstatus_id` (`transfer_status`),
  KEY `return_items_created_by_id_35a94569_fk_users_id` (`created_by_id`),
  CONSTRAINT `return_items_created_by_id_35a94569_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `return_items_transfer_itemid_5b701d15_fk_transerfer_items_id` FOREIGN KEY (`transfer_itemid`) REFERENCES `transerfer_items` (`id`),
  CONSTRAINT `return_items_transfer_status_9b122186_fk_transferstatus_id` FOREIGN KEY (`transfer_status`) REFERENCES `transferstatus` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `return_items`
--

LOCK TABLES `return_items` WRITE;
/*!40000 ALTER TABLE `return_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `return_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `returnitem_details`
--

DROP TABLE IF EXISTS `returnitem_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `returnitem_details` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_number` varchar(255) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `return_itemid` bigint NOT NULL,
  `tagitems_id` bigint NOT NULL,
  `transfer_itemid` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `returnitem_details_created_by_id_de8035e3_fk_users_id` (`created_by_id`),
  KEY `returnitem_details_return_itemid_f02aec2e_fk_return_items_id` (`return_itemid`),
  KEY `returnitem_details_tagitems_id_c845bb51_fk_tagged_item_id` (`tagitems_id`),
  KEY `returnitem_details_transfer_itemid_2a852c74_fk_transerfe` (`transfer_itemid`),
  CONSTRAINT `returnitem_details_created_by_id_de8035e3_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `returnitem_details_return_itemid_f02aec2e_fk_return_items_id` FOREIGN KEY (`return_itemid`) REFERENCES `return_items` (`id`),
  CONSTRAINT `returnitem_details_tagitems_id_c845bb51_fk_tagged_item_id` FOREIGN KEY (`tagitems_id`) REFERENCES `tagged_item` (`id`),
  CONSTRAINT `returnitem_details_transfer_itemid_2a852c74_fk_transerfe` FOREIGN KEY (`transfer_itemid`) REFERENCES `transerfer_items` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `returnitem_details`
--

LOCK TABLES `returnitem_details` WRITE;
/*!40000 ALTER TABLE `returnitem_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `returnitem_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sale_return_policy`
--

DROP TABLE IF EXISTS `sale_return_policy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sale_return_policy` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `return_days` int NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sale_return_policy_created_by_id_e61638d7_fk_users_id` (`created_by_id`),
  KEY `sale_return_policy_modified_by_id_89ade099_fk_users_id` (`modified_by_id`),
  CONSTRAINT `sale_return_policy_created_by_id_e61638d7_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `sale_return_policy_modified_by_id_89ade099_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale_return_policy`
--

LOCK TABLES `sale_return_policy` WRITE;
/*!40000 ALTER TABLE `sale_return_policy` DISABLE KEYS */;
/*!40000 ALTER TABLE `sale_return_policy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_tax_detail`
--

DROP TABLE IF EXISTS `sales_tax_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_tax_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sales_tax_igst` double NOT NULL,
  `sales_tax_cgst` double NOT NULL,
  `sales_tax_sgst` double NOT NULL,
  `sales_surcharge_percent` double NOT NULL,
  `sales_additional_charges` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `tax_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sales_tax_detail_created_by_id_da843139_fk_users_id` (`created_by_id`),
  KEY `sales_tax_detail_tax_details_id_6168599e_fk_tax_detail_id` (`tax_details_id`),
  CONSTRAINT `sales_tax_detail_created_by_id_da843139_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `sales_tax_detail_tax_details_id_6168599e_fk_tax_detail_id` FOREIGN KEY (`tax_details_id`) REFERENCES `tax_detail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_tax_detail`
--

LOCK TABLES `sales_tax_detail` WRITE;
/*!40000 ALTER TABLE `sales_tax_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_tax_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings_gender`
--

DROP TABLE IF EXISTS `settings_gender`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settings_gender` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `settings_gender_created_by_id_7ebbda03_fk_users_id` (`created_by_id`),
  CONSTRAINT `settings_gender_created_by_id_7ebbda03_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings_gender`
--

LOCK TABLES `settings_gender` WRITE;
/*!40000 ALTER TABLE `settings_gender` DISABLE KEYS */;
INSERT INTO `settings_gender` VALUES (1,'Male',1,NULL,NULL),(2,'Female',1,NULL,NULL);
/*!40000 ALTER TABLE `settings_gender` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shape_detail`
--

DROP TABLE IF EXISTS `shape_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shape_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `shape_name` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shape_name` (`shape_name`),
  KEY `shape_detail_created_by_id_5d3a05fe_fk_users_id` (`created_by_id`),
  CONSTRAINT `shape_detail_created_by_id_5d3a05fe_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shape_detail`
--

LOCK TABLES `shape_detail` WRITE;
/*!40000 ALTER TABLE `shape_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `shape_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `silver_bill_id`
--

DROP TABLE IF EXISTS `silver_bill_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `silver_bill_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `silver_bill_id` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `silver_bill_id` (`silver_bill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `silver_bill_id`
--

LOCK TABLES `silver_bill_id` WRITE;
/*!40000 ALTER TABLE `silver_bill_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `silver_bill_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `silver_bill_number`
--

DROP TABLE IF EXISTS `silver_bill_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `silver_bill_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `silver_bill_number` varchar(10) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `silver_bill_number` (`silver_bill_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `silver_bill_number_user_id_73b4abea_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `silver_bill_number`
--

LOCK TABLES `silver_bill_number` WRITE;
/*!40000 ALTER TABLE `silver_bill_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `silver_bill_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `silver_estimation_id`
--

DROP TABLE IF EXISTS `silver_estimation_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `silver_estimation_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `silver_estimation_id` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `silver_estimation_id` (`silver_estimation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `silver_estimation_id`
--

LOCK TABLES `silver_estimation_id` WRITE;
/*!40000 ALTER TABLE `silver_estimation_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `silver_estimation_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `silver_estimation_number`
--

DROP TABLE IF EXISTS `silver_estimation_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `silver_estimation_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `silver_estimation_number` varchar(10) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `silver_estimation_number` (`silver_estimation_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `silver_estimation_number_user_id_52d10d96_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `silver_estimation_number`
--

LOCK TABLES `silver_estimation_number` WRITE;
/*!40000 ALTER TABLE `silver_estimation_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `silver_estimation_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staffs`
--

DROP TABLE IF EXISTS `staffs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staffs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `staff_id` varchar(100) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(60) DEFAULT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `address` varchar(500) DEFAULT NULL,
  `pincode` varchar(10) DEFAULT NULL,
  `aadhar_card` varchar(500) DEFAULT NULL,
  `pan_card` varchar(500) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `branch_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `department_id` bigint NOT NULL,
  `designation_id` bigint NOT NULL,
  `location_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `staff_id` (`staff_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  KEY `staffs_branch_id_ca53fae6_fk_branches_id` (`branch_id`),
  KEY `staffs_created_by_id_bf6a1a31_fk_users_id` (`created_by_id`),
  KEY `staffs_department_id_ab62f65b_fk_departments_id` (`department_id`),
  KEY `staffs_designation_id_7027e66f_fk_designations_id` (`designation_id`),
  KEY `staffs_location_id_4af579a2_fk_locations_id` (`location_id`),
  CONSTRAINT `staffs_branch_id_ca53fae6_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `staffs_created_by_id_bf6a1a31_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `staffs_department_id_ab62f65b_fk_departments_id` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`),
  CONSTRAINT `staffs_designation_id_7027e66f_fk_designations_id` FOREIGN KEY (`designation_id`) REFERENCES `designations` (`id`),
  CONSTRAINT `staffs_location_id_4af579a2_fk_locations_id` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staffs`
--

LOCK TABLES `staffs` WRITE;
/*!40000 ALTER TABLE `staffs` DISABLE KEYS */;
INSERT INTO `staffs` VALUES (1,'STAFF00001','boopathi','d','boopathi@atts.in','9677826398','Abiramam','{\"name\":\"Tamil Nadu\",\"isoCode\":\"TN\"}','{\"name\":\"India\",\"isoCode\":\"IN\"}','coimbatore','641041','','','2',1,'2024-07-03 06:19:55.619681',NULL,NULL,1,1,1,1,1),(2,'STAFF00002','dhinagaran','m','dhinagaran@atts.in','7305685960','Aduthurai','{\"name\":\"Tamil Nadu\",\"isoCode\":\"TN\"}','{\"name\":\"India\",\"isoCode\":\"IN\"}','coimbatore','641041','','','3',1,'2024-07-03 06:20:26.099700',NULL,NULL,1,1,1,1,1),(3,'STAFF00003','jeyasekar','s','jeyasekar@atts.in','9677826379','Alandur','{\"name\":\"Tamil Nadu\",\"isoCode\":\"TN\"}','{\"name\":\"India\",\"isoCode\":\"IN\"}','coimbatore','641041','','','4',1,'2024-07-03 06:21:16.535906',NULL,NULL,1,1,1,1,1),(4,'STAFF00004','gokul','c','gokul@atts.in','6589654125','Adirampattinam','{\"name\":\"Tamil Nadu\",\"isoCode\":\"TN\"}','{\"name\":\"India\",\"isoCode\":\"IN\"}','coimbatore','641041','','','5',1,'2024-07-03 06:21:40.156401',NULL,NULL,1,1,1,1,1);
/*!40000 ALTER TABLE `staffs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status_table`
--

DROP TABLE IF EXISTS `status_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_table` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status_name` varchar(50) NOT NULL,
  `module` varchar(50) NOT NULL,
  `color` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_table`
--

LOCK TABLES `status_table` WRITE;
/*!40000 ALTER TABLE `status_table` DISABLE KEYS */;
INSERT INTO `status_table` VALUES (1,'Pending','1','#AD9FFF'),(2,'Partial','1','#AD9FFF'),(3,'Completed','1','#AD9FFF'),(4,'Order Issued','1','#AD9FFF'),(5,'Order Received','1','#AD9FFF'),(6,'Order Delivered','1','#AD9FFF'),(7,'Cancelled','1','#AD9FFF'),(8,'Estimation Approval','1','#AD9FFF'),(9,'Estimation Denied','1','#AD9FFF'),(10,'Melting Issued','1','#AD9FFF'),(11,'Melting Received','1','#AD9FFF'),(12,'Purification Issued','1','#AD9FFF'),(13,'Purification Received','1','#AD9FFF'),(14,'Approval Issued','1','#AD9FFF'),(15,'Approval Received','1','#AD9FFF'),(16,'Repair Issued','1','#AD9FFF'),(17,'Repair Received','1','#AD9FFF'),(18,'Repair Deliverd','1','#AD9FFF');
/*!40000 ALTER TABLE `status_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_type`
--

DROP TABLE IF EXISTS `stock_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stock_type_name` varchar(25) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stock_type_name` (`stock_type_name`),
  KEY `stock_type_created_by_id_810d985e_fk_users_id` (`created_by_id`),
  CONSTRAINT `stock_type_created_by_id_810d985e_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_type`
--

LOCK TABLES `stock_type` WRITE;
/*!40000 ALTER TABLE `stock_type` DISABLE KEYS */;
INSERT INTO `stock_type` VALUES (1,'tag',1,NULL,NULL,NULL,NULL),(2,'non tag',1,NULL,NULL,NULL,NULL),(3,'packet',1,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `stock_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stone_detail`
--

DROP TABLE IF EXISTS `stone_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stone_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stone_name` varchar(50) NOT NULL,
  `stone_code` varchar(10) NOT NULL,
  `reduce_weight` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `stone_detail_created_by_id_5d606e41_fk_users_id` (`created_by_id`),
  CONSTRAINT `stone_detail_created_by_id_5d606e41_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stone_detail`
--

LOCK TABLES `stone_detail` WRITE;
/*!40000 ALTER TABLE `stone_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `stone_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stone_weight_type`
--

DROP TABLE IF EXISTS `stone_weight_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stone_weight_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `weight_name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `weight_name` (`weight_name`),
  KEY `stone_weight_type_created_by_id_1b46867a_fk_users_id` (`created_by_id`),
  CONSTRAINT `stone_weight_type_created_by_id_1b46867a_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stone_weight_type`
--

LOCK TABLES `stone_weight_type` WRITE;
/*!40000 ALTER TABLE `stone_weight_type` DISABLE KEYS */;
INSERT INTO `stone_weight_type` VALUES (1,'Carat',1,NULL,NULL,NULL,NULL),(2,'Gram',1,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `stone_weight_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sub_item_detail`
--

DROP TABLE IF EXISTS `sub_item_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sub_item_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sub_item_id` varchar(10) NOT NULL,
  `subitem_hsn_code` varchar(15) NOT NULL,
  `sub_item_code` varchar(25) NOT NULL,
  `sub_item_name` varchar(50) NOT NULL,
  `allow_zero_weight` tinyint(1) NOT NULL,
  `sub_item_image` varchar(250) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `calculation_type_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `item_details_id` bigint NOT NULL,
  `measurement_type_id` bigint NOT NULL,
  `metal_id` bigint NOT NULL,
  `purity_id` bigint NOT NULL,
  `stock_type_id` bigint NOT NULL,
  `sub_item_counter_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sub_item_id` (`sub_item_id`),
  UNIQUE KEY `sub_item_code` (`sub_item_code`),
  KEY `sub_item_detail_calculation_type_id_bb610ab1_fk_calculati` (`calculation_type_id`),
  KEY `sub_item_detail_created_by_id_82df5db4_fk_users_id` (`created_by_id`),
  KEY `sub_item_detail_item_details_id_4487d9df_fk_item_detail_id` (`item_details_id`),
  KEY `sub_item_detail_measurement_type_id_1b261a68_fk_measureme` (`measurement_type_id`),
  KEY `sub_item_detail_metal_id_398f76e0_fk_metals_id` (`metal_id`),
  KEY `sub_item_detail_purity_id_eca5ee03_fk_purities_id` (`purity_id`),
  KEY `sub_item_detail_stock_type_id_d342f627_fk_stock_type_id` (`stock_type_id`),
  KEY `sub_item_detail_sub_item_counter_id_3e3d4582_fk_counters_id` (`sub_item_counter_id`),
  CONSTRAINT `sub_item_detail_calculation_type_id_bb610ab1_fk_calculati` FOREIGN KEY (`calculation_type_id`) REFERENCES `calculation_type` (`id`),
  CONSTRAINT `sub_item_detail_created_by_id_82df5db4_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `sub_item_detail_item_details_id_4487d9df_fk_item_detail_id` FOREIGN KEY (`item_details_id`) REFERENCES `item_detail` (`id`),
  CONSTRAINT `sub_item_detail_measurement_type_id_1b261a68_fk_measureme` FOREIGN KEY (`measurement_type_id`) REFERENCES `measurement_type` (`id`),
  CONSTRAINT `sub_item_detail_metal_id_398f76e0_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `sub_item_detail_purity_id_eca5ee03_fk_purities_id` FOREIGN KEY (`purity_id`) REFERENCES `purities` (`id`),
  CONSTRAINT `sub_item_detail_stock_type_id_d342f627_fk_stock_type_id` FOREIGN KEY (`stock_type_id`) REFERENCES `stock_type` (`id`),
  CONSTRAINT `sub_item_detail_sub_item_counter_id_3e3d4582_fk_counters_id` FOREIGN KEY (`sub_item_counter_id`) REFERENCES `counters` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sub_item_detail`
--

LOCK TABLES `sub_item_detail` WRITE;
/*!40000 ALTER TABLE `sub_item_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `sub_item_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sub_item_id`
--

DROP TABLE IF EXISTS `sub_item_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sub_item_id` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sub_item_id` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sub_item_id` (`sub_item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sub_item_id`
--

LOCK TABLES `sub_item_id` WRITE;
/*!40000 ALTER TABLE `sub_item_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `sub_item_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sub_per_gram_rate`
--

DROP TABLE IF EXISTS `sub_per_gram_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sub_per_gram_rate` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `per_gram_rate` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `sub_item_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sub_per_gram_rate_created_by_id_9eb17a29_fk_users_id` (`created_by_id`),
  KEY `sub_per_gram_rate_sub_item_details_id_391f12af_fk_sub_item_` (`sub_item_details_id`),
  CONSTRAINT `sub_per_gram_rate_created_by_id_9eb17a29_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `sub_per_gram_rate_sub_item_details_id_391f12af_fk_sub_item_` FOREIGN KEY (`sub_item_details_id`) REFERENCES `sub_item_detail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sub_per_gram_rate`
--

LOCK TABLES `sub_per_gram_rate` WRITE;
/*!40000 ALTER TABLE `sub_per_gram_rate` DISABLE KEYS */;
/*!40000 ALTER TABLE `sub_per_gram_rate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subitem_fixed_rate`
--

DROP TABLE IF EXISTS `subitem_fixed_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subitem_fixed_rate` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fixed_rate` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `sub_item_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `subitem_fixed_rate_created_by_id_93751985_fk_users_id` (`created_by_id`),
  KEY `subitem_fixed_rate_sub_item_details_id_dd645cf2_fk_sub_item_` (`sub_item_details_id`),
  CONSTRAINT `subitem_fixed_rate_created_by_id_93751985_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `subitem_fixed_rate_sub_item_details_id_dd645cf2_fk_sub_item_` FOREIGN KEY (`sub_item_details_id`) REFERENCES `sub_item_detail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subitem_fixed_rate`
--

LOCK TABLES `subitem_fixed_rate` WRITE;
/*!40000 ALTER TABLE `subitem_fixed_rate` DISABLE KEYS */;
/*!40000 ALTER TABLE `subitem_fixed_rate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subitem_weight_calculation`
--

DROP TABLE IF EXISTS `subitem_weight_calculation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subitem_weight_calculation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `wastage_percent` double NOT NULL,
  `flat_wastage` double NOT NULL,
  `making_charge_gram` double NOT NULL,
  `flat_making_charge` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `making_charge_calculation_id` bigint NOT NULL,
  `sub_item_details_id` bigint NOT NULL,
  `wastage_calculation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `subitem_weight_calculation_created_by_id_854f8456_fk_users_id` (`created_by_id`),
  KEY `subitem_weight_calcu_making_charge_calcul_62e54e4a_fk_weight_ty` (`making_charge_calculation_id`),
  KEY `subitem_weight_calcu_sub_item_details_id_27812c41_fk_sub_item_` (`sub_item_details_id`),
  KEY `subitem_weight_calcu_wastage_calculation__0fb7a013_fk_weight_ty` (`wastage_calculation_id`),
  CONSTRAINT `subitem_weight_calcu_making_charge_calcul_62e54e4a_fk_weight_ty` FOREIGN KEY (`making_charge_calculation_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `subitem_weight_calcu_sub_item_details_id_27812c41_fk_sub_item_` FOREIGN KEY (`sub_item_details_id`) REFERENCES `sub_item_detail` (`id`),
  CONSTRAINT `subitem_weight_calcu_wastage_calculation__0fb7a013_fk_weight_ty` FOREIGN KEY (`wastage_calculation_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `subitem_weight_calculation_created_by_id_854f8456_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subitem_weight_calculation`
--

LOCK TABLES `subitem_weight_calculation` WRITE;
/*!40000 ALTER TABLE `subitem_weight_calculation` DISABLE KEYS */;
/*!40000 ALTER TABLE `subitem_weight_calculation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag_entry`
--

DROP TABLE IF EXISTS `tag_entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tag_entry` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `branch` bigint DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `lot_details_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tag_entry_branch_4f3633ae_fk_branches_id` (`branch`),
  KEY `tag_entry_created_by_id_193f205b_fk_users_id` (`created_by_id`),
  KEY `tag_entry_lot_details_id_0de93adb_fk_lot_id` (`lot_details_id`),
  CONSTRAINT `tag_entry_branch_4f3633ae_fk_branches_id` FOREIGN KEY (`branch`) REFERENCES `branches` (`id`),
  CONSTRAINT `tag_entry_created_by_id_193f205b_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `tag_entry_lot_details_id_0de93adb_fk_lot_id` FOREIGN KEY (`lot_details_id`) REFERENCES `lot` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag_entry`
--

LOCK TABLES `tag_entry` WRITE;
/*!40000 ALTER TABLE `tag_entry` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag_entry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag_number`
--

DROP TABLE IF EXISTS `tag_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tag_number` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_number` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag_number`
--

LOCK TABLES `tag_number` WRITE;
/*!40000 ALTER TABLE `tag_number` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag_number` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag_type`
--

DROP TABLE IF EXISTS `tag_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tag_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(25) NOT NULL,
  `tag_code` varchar(10) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `metal_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag_name` (`tag_name`),
  UNIQUE KEY `tag_code` (`tag_code`),
  KEY `tag_type_created_by_id_987fa9eb_fk_users_id` (`created_by_id`),
  KEY `tag_type_metal_id_71fc42d8_fk_metals_id` (`metal_id`),
  CONSTRAINT `tag_type_created_by_id_987fa9eb_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `tag_type_metal_id_71fc42d8_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag_type`
--

LOCK TABLES `tag_type` WRITE;
/*!40000 ALTER TABLE `tag_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tagged_item`
--

DROP TABLE IF EXISTS `tagged_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tagged_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_number` varchar(50) NOT NULL,
  `size_value` int DEFAULT NULL,
  `tag_pieces` int NOT NULL,
  `tag_count` int NOT NULL,
  `gross_weight` double NOT NULL,
  `net_weight` double DEFAULT NULL,
  `tag_weight` double NOT NULL,
  `cover_weight` double NOT NULL,
  `loop_weight` double NOT NULL,
  `other_weight` double NOT NULL,
  `stone_weight` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `stone_pieces` int DEFAULT NULL,
  `diamond_weight` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `diamond_pieces` int DEFAULT NULL,
  `min_fixed_rate` double DEFAULT NULL,
  `max_fixed_rate` double DEFAULT NULL,
  `min_wastage_percent` double DEFAULT NULL,
  `min_flat_wastage` double DEFAULT NULL,
  `max_wastage_percent` double DEFAULT NULL,
  `max_flat_wastage` double DEFAULT NULL,
  `min_making_charge_gram` double DEFAULT NULL,
  `min_flat_making_charge` double DEFAULT NULL,
  `max_making_charge_gram` double DEFAULT NULL,
  `max_flat_making_charge` double DEFAULT NULL,
  `min_pergram_rate` double DEFAULT NULL,
  `max_pergram_rate` double DEFAULT NULL,
  `rough_sale_value` double DEFAULT NULL,
  `halmark_huid` varchar(50) NOT NULL,
  `halmark_center` varchar(50) NOT NULL,
  `remaining_pieces` int DEFAULT NULL,
  `remaining_gross_weight` double DEFAULT NULL,
  `remaining_net_weight` double DEFAULT NULL,
  `remaining_tag_count` double DEFAULT NULL,
  `is_billed` tinyint(1) NOT NULL,
  `transfer` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `branch` bigint DEFAULT NULL,
  `calculation_type_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `display_counter_id` bigint NOT NULL,
  `item_details_id` bigint NOT NULL,
  `per_gram_weight_type_id` bigint DEFAULT NULL,
  `sub_item_details_id` bigint NOT NULL,
  `tag_entry_details_id` bigint NOT NULL,
  `tag_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag_number` (`tag_number`),
  KEY `tagged_item_branch_95d41635_fk_branches_id` (`branch`),
  KEY `tagged_item_calculation_type_id_9e4ac81f_fk_calculation_type_id` (`calculation_type_id`),
  KEY `tagged_item_created_by_id_c997547b_fk_users_id` (`created_by_id`),
  KEY `tagged_item_display_counter_id_41aa7daa_fk_counters_id` (`display_counter_id`),
  KEY `tagged_item_item_details_id_742398ed_fk_lot_item_id` (`item_details_id`),
  KEY `tagged_item_per_gram_weight_type_id_30429bde_fk_weight_type_id` (`per_gram_weight_type_id`),
  KEY `tagged_item_sub_item_details_id_69a7a118_fk_sub_item_detail_id` (`sub_item_details_id`),
  KEY `tagged_item_tag_entry_details_id_f3e5ca59_fk_tag_entry_id` (`tag_entry_details_id`),
  KEY `tagged_item_tag_type_id_5de94c0b_fk_tag_type_id` (`tag_type_id`),
  CONSTRAINT `tagged_item_branch_95d41635_fk_branches_id` FOREIGN KEY (`branch`) REFERENCES `branches` (`id`),
  CONSTRAINT `tagged_item_calculation_type_id_9e4ac81f_fk_calculation_type_id` FOREIGN KEY (`calculation_type_id`) REFERENCES `calculation_type` (`id`),
  CONSTRAINT `tagged_item_created_by_id_c997547b_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `tagged_item_display_counter_id_41aa7daa_fk_counters_id` FOREIGN KEY (`display_counter_id`) REFERENCES `counters` (`id`),
  CONSTRAINT `tagged_item_item_details_id_742398ed_fk_lot_item_id` FOREIGN KEY (`item_details_id`) REFERENCES `lot_item` (`id`),
  CONSTRAINT `tagged_item_per_gram_weight_type_id_30429bde_fk_weight_type_id` FOREIGN KEY (`per_gram_weight_type_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `tagged_item_sub_item_details_id_69a7a118_fk_sub_item_detail_id` FOREIGN KEY (`sub_item_details_id`) REFERENCES `sub_item_detail` (`id`),
  CONSTRAINT `tagged_item_tag_entry_details_id_f3e5ca59_fk_tag_entry_id` FOREIGN KEY (`tag_entry_details_id`) REFERENCES `tag_entry` (`id`),
  CONSTRAINT `tagged_item_tag_type_id_5de94c0b_fk_tag_type_id` FOREIGN KEY (`tag_type_id`) REFERENCES `tag_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tagged_item`
--

LOCK TABLES `tagged_item` WRITE;
/*!40000 ALTER TABLE `tagged_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `tagged_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tagged_item_diamond`
--

DROP TABLE IF EXISTS `tagged_item_diamond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tagged_item_diamond` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `diamond_pieces` int DEFAULT NULL,
  `diamond_weight` double DEFAULT NULL,
  `diamond_rate` double DEFAULT NULL,
  `total_diamond_value` double DEFAULT NULL,
  `include_diamond_weight` tinyint(1) NOT NULL,
  `diamond_name_id` bigint NOT NULL,
  `diamond_rate_type_id` bigint NOT NULL,
  `diamond_weight_type_id` bigint NOT NULL,
  `tag_details_id` bigint NOT NULL,
  `tag_entry_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tagged_item_diamond_diamond_name_id_680224b3_fk_lot_item_` (`diamond_name_id`),
  KEY `tagged_item_diamond_diamond_rate_type_id_ea236c9a_fk_rate_type` (`diamond_rate_type_id`),
  KEY `tagged_item_diamond_diamond_weight_type__0e881f7a_fk_stone_wei` (`diamond_weight_type_id`),
  KEY `tagged_item_diamond_tag_details_id_d53e43ef_fk_tagged_item_id` (`tag_details_id`),
  KEY `tagged_item_diamond_tag_entry_details_id_977a33c7_fk_tag_entry` (`tag_entry_details_id`),
  CONSTRAINT `tagged_item_diamond_diamond_name_id_680224b3_fk_lot_item_` FOREIGN KEY (`diamond_name_id`) REFERENCES `lot_item_diamond` (`id`),
  CONSTRAINT `tagged_item_diamond_diamond_rate_type_id_ea236c9a_fk_rate_type` FOREIGN KEY (`diamond_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `tagged_item_diamond_diamond_weight_type__0e881f7a_fk_stone_wei` FOREIGN KEY (`diamond_weight_type_id`) REFERENCES `stone_weight_type` (`id`),
  CONSTRAINT `tagged_item_diamond_tag_details_id_d53e43ef_fk_tagged_item_id` FOREIGN KEY (`tag_details_id`) REFERENCES `tagged_item` (`id`),
  CONSTRAINT `tagged_item_diamond_tag_entry_details_id_977a33c7_fk_tag_entry` FOREIGN KEY (`tag_entry_details_id`) REFERENCES `tag_entry` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tagged_item_diamond`
--

LOCK TABLES `tagged_item_diamond` WRITE;
/*!40000 ALTER TABLE `tagged_item_diamond` DISABLE KEYS */;
/*!40000 ALTER TABLE `tagged_item_diamond` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tagged_item_stone`
--

DROP TABLE IF EXISTS `tagged_item_stone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tagged_item_stone` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stone_pieces` int DEFAULT NULL,
  `stone_weight` double DEFAULT NULL,
  `stone_rate` double DEFAULT NULL,
  `total_stone_value` double DEFAULT NULL,
  `include_stone_weight` tinyint(1) NOT NULL,
  `stone_name_id` bigint NOT NULL,
  `stone_rate_type_id` bigint NOT NULL,
  `stone_weight_type_id` bigint NOT NULL,
  `tag_details_id` bigint NOT NULL,
  `tag_entry_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tagged_item_stone_stone_name_id_ba50ab6d_fk_lot_item_stone_id` (`stone_name_id`),
  KEY `tagged_item_stone_stone_rate_type_id_2c34f35c_fk_rate_type_id` (`stone_rate_type_id`),
  KEY `tagged_item_stone_stone_weight_type_id_72ca9ee0_fk_stone_wei` (`stone_weight_type_id`),
  KEY `tagged_item_stone_tag_details_id_86e902aa_fk_tagged_item_id` (`tag_details_id`),
  KEY `tagged_item_stone_tag_entry_details_id_3ef620ce_fk_tag_entry_id` (`tag_entry_details_id`),
  CONSTRAINT `tagged_item_stone_stone_name_id_ba50ab6d_fk_lot_item_stone_id` FOREIGN KEY (`stone_name_id`) REFERENCES `lot_item_stone` (`id`),
  CONSTRAINT `tagged_item_stone_stone_rate_type_id_2c34f35c_fk_rate_type_id` FOREIGN KEY (`stone_rate_type_id`) REFERENCES `rate_type` (`id`),
  CONSTRAINT `tagged_item_stone_stone_weight_type_id_72ca9ee0_fk_stone_wei` FOREIGN KEY (`stone_weight_type_id`) REFERENCES `stone_weight_type` (`id`),
  CONSTRAINT `tagged_item_stone_tag_details_id_86e902aa_fk_tagged_item_id` FOREIGN KEY (`tag_details_id`) REFERENCES `tagged_item` (`id`),
  CONSTRAINT `tagged_item_stone_tag_entry_details_id_3ef620ce_fk_tag_entry_id` FOREIGN KEY (`tag_entry_details_id`) REFERENCES `tag_entry` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tagged_item_stone`
--

LOCK TABLES `tagged_item_stone` WRITE;
/*!40000 ALTER TABLE `tagged_item_stone` DISABLE KEYS */;
/*!40000 ALTER TABLE `tagged_item_stone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tax_detail`
--

DROP TABLE IF EXISTS `tax_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tax_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tax_code` varchar(50) NOT NULL,
  `tax_name` varchar(50) NOT NULL,
  `tax_description` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `metal_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tax_code` (`tax_code`),
  KEY `tax_detail_created_by_id_ba689644_fk_users_id` (`created_by_id`),
  KEY `tax_detail_metal_id_59541bdb_fk_metals_id` (`metal_id`),
  CONSTRAINT `tax_detail_created_by_id_ba689644_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `tax_detail_metal_id_59541bdb_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tax_detail`
--

LOCK TABLES `tax_detail` WRITE;
/*!40000 ALTER TABLE `tax_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `tax_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tax_details_audit`
--

DROP TABLE IF EXISTS `tax_details_audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tax_details_audit` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `metal_id` bigint NOT NULL,
  `tax_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `metal_id` (`metal_id`),
  UNIQUE KEY `tax_details_id` (`tax_details_id`),
  KEY `tax_details_audit_created_by_id_84f589cb_fk_users_id` (`created_by_id`),
  CONSTRAINT `tax_details_audit_created_by_id_84f589cb_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `tax_details_audit_metal_id_b3b64bdb_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `tax_details_audit_tax_details_id_e441ca9d_fk_tax_detail_id` FOREIGN KEY (`tax_details_id`) REFERENCES `tax_detail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tax_details_audit`
--

LOCK TABLES `tax_details_audit` WRITE;
/*!40000 ALTER TABLE `tax_details_audit` DISABLE KEYS */;
/*!40000 ALTER TABLE `tax_details_audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transerfer_items`
--

DROP TABLE IF EXISTS `transerfer_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transerfer_items` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `transfer_date` date NOT NULL,
  `required_date` date NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `stock_authority` bigint NOT NULL,
  `transfer_from` bigint NOT NULL,
  `transfer_status` bigint NOT NULL,
  `transfer_to` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `transerfer_items_transfer_status_68e6fc77_fk_transferstatus_id` (`transfer_status`),
  KEY `transerfer_items_transfer_to_6c326bed_fk_branches_id` (`transfer_to`),
  KEY `transerfer_items_created_by_id_89b69d37_fk_users_id` (`created_by_id`),
  KEY `transerfer_items_stock_authority_f9e42f02_fk_staffs_id` (`stock_authority`),
  KEY `transerfer_items_transfer_from_4a3f370e_fk_branches_id` (`transfer_from`),
  CONSTRAINT `transerfer_items_created_by_id_89b69d37_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `transerfer_items_stock_authority_f9e42f02_fk_staffs_id` FOREIGN KEY (`stock_authority`) REFERENCES `staffs` (`id`),
  CONSTRAINT `transerfer_items_transfer_from_4a3f370e_fk_branches_id` FOREIGN KEY (`transfer_from`) REFERENCES `branches` (`id`),
  CONSTRAINT `transerfer_items_transfer_status_68e6fc77_fk_transferstatus_id` FOREIGN KEY (`transfer_status`) REFERENCES `transferstatus` (`id`),
  CONSTRAINT `transerfer_items_transfer_to_6c326bed_fk_branches_id` FOREIGN KEY (`transfer_to`) REFERENCES `branches` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transerfer_items`
--

LOCK TABLES `transerfer_items` WRITE;
/*!40000 ALTER TABLE `transerfer_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `transerfer_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transfer_creation`
--

DROP TABLE IF EXISTS `transfer_creation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transfer_creation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `refference_number` varchar(50) NOT NULL,
  `total_gross_weight` double NOT NULL,
  `total_net_weight` double NOT NULL,
  `total_dust_weight` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `branch_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `metal_id` bigint NOT NULL,
  `smith_id` bigint NOT NULL,
  `transfer_category_id` bigint NOT NULL,
  `transfer_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `refference_number` (`refference_number`),
  KEY `transfer_creation_transfer_type_id_907c9925_fk_transfer_` (`transfer_type_id`),
  KEY `transfer_creation_branch_id_483e6f8e_fk_branches_id` (`branch_id`),
  KEY `transfer_creation_created_by_id_c74070a3_fk_users_id` (`created_by_id`),
  KEY `transfer_creation_metal_id_25a57033_fk_metals_id` (`metal_id`),
  KEY `transfer_creation_smith_id_2840f252_fk_account_head_id` (`smith_id`),
  KEY `transfer_creation_transfer_category_id_da95b5fb_fk_old_metal` (`transfer_category_id`),
  CONSTRAINT `transfer_creation_branch_id_483e6f8e_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `transfer_creation_created_by_id_c74070a3_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `transfer_creation_metal_id_25a57033_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `transfer_creation_smith_id_2840f252_fk_account_head_id` FOREIGN KEY (`smith_id`) REFERENCES `account_head` (`id`),
  CONSTRAINT `transfer_creation_transfer_category_id_da95b5fb_fk_old_metal` FOREIGN KEY (`transfer_category_id`) REFERENCES `old_metal_category` (`id`),
  CONSTRAINT `transfer_creation_transfer_type_id_907c9925_fk_transfer_` FOREIGN KEY (`transfer_type_id`) REFERENCES `transfer_creation_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transfer_creation`
--

LOCK TABLES `transfer_creation` WRITE;
/*!40000 ALTER TABLE `transfer_creation` DISABLE KEYS */;
/*!40000 ALTER TABLE `transfer_creation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transfer_creation_item`
--

DROP TABLE IF EXISTS `transfer_creation_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transfer_creation_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `old_gold_id` int DEFAULT NULL,
  `old_gold_number` varchar(50) NOT NULL,
  `refference_number` varchar(50) NOT NULL,
  `received_date` date NOT NULL,
  `transfered_date` date NOT NULL,
  `gross_weight` double DEFAULT NULL,
  `net_weight` double DEFAULT NULL,
  `dust_weight` double DEFAULT NULL,
  `old_gold_type_id` bigint NOT NULL,
  `old_metal_id` bigint NOT NULL,
  `transfet_creation_details_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `transfer_creation_it_old_gold_type_id_f2436a53_fk_old_gold_` (`old_gold_type_id`),
  KEY `transfer_creation_item_old_metal_id_6a54a4a9_fk_metals_id` (`old_metal_id`),
  KEY `transfer_creation_it_transfet_creation_de_fc7ff460_fk_transfer_` (`transfet_creation_details_id`),
  CONSTRAINT `transfer_creation_it_old_gold_type_id_f2436a53_fk_old_gold_` FOREIGN KEY (`old_gold_type_id`) REFERENCES `old_gold_type` (`id`),
  CONSTRAINT `transfer_creation_it_transfet_creation_de_fc7ff460_fk_transfer_` FOREIGN KEY (`transfet_creation_details_id`) REFERENCES `transfer_creation` (`id`),
  CONSTRAINT `transfer_creation_item_old_metal_id_6a54a4a9_fk_metals_id` FOREIGN KEY (`old_metal_id`) REFERENCES `metals` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transfer_creation_item`
--

LOCK TABLES `transfer_creation_item` WRITE;
/*!40000 ALTER TABLE `transfer_creation_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `transfer_creation_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transfer_creation_type`
--

DROP TABLE IF EXISTS `transfer_creation_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transfer_creation_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type_name` (`type_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transfer_creation_type`
--

LOCK TABLES `transfer_creation_type` WRITE;
/*!40000 ALTER TABLE `transfer_creation_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `transfer_creation_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transfer_type`
--

DROP TABLE IF EXISTS `transfer_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transfer_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status_name` varchar(50) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `transfer_type_created_by_id_c4b30370_fk_users_id` (`created_by_id`),
  CONSTRAINT `transfer_type_created_by_id_c4b30370_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transfer_type`
--

LOCK TABLES `transfer_type` WRITE;
/*!40000 ALTER TABLE `transfer_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `transfer_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transferitem_details`
--

DROP TABLE IF EXISTS `transferitem_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transferitem_details` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_number` varchar(255) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `tagitems_id_id` bigint NOT NULL,
  `transfer_itemid` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `transferitem_details_created_by_id_91966da4_fk_users_id` (`created_by_id`),
  KEY `transferitem_details_tagitems_id_id_6eaf0569_fk_tagged_item_id` (`tagitems_id_id`),
  KEY `transferitem_details_transfer_itemid_06dc5c74_fk_transerfe` (`transfer_itemid`),
  CONSTRAINT `transferitem_details_created_by_id_91966da4_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `transferitem_details_tagitems_id_id_6eaf0569_fk_tagged_item_id` FOREIGN KEY (`tagitems_id_id`) REFERENCES `tagged_item` (`id`),
  CONSTRAINT `transferitem_details_transfer_itemid_06dc5c74_fk_transerfe` FOREIGN KEY (`transfer_itemid`) REFERENCES `transerfer_items` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transferitem_details`
--

LOCK TABLES `transferitem_details` WRITE;
/*!40000 ALTER TABLE `transferitem_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `transferitem_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transferstatus`
--

DROP TABLE IF EXISTS `transferstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transferstatus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status_name` varchar(50) NOT NULL,
  `status_comments` varchar(50) NOT NULL,
  `status_bgcolor` varchar(255) DEFAULT NULL,
  `status_color` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` int DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `transferstatus_created_by_id_d8b3f969_fk_users_id` (`created_by_id`),
  CONSTRAINT `transferstatus_created_by_id_d8b3f969_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transferstatus`
--

LOCK TABLES `transferstatus` WRITE;
/*!40000 ALTER TABLE `transferstatus` DISABLE KEYS */;
/*!40000 ALTER TABLE `transferstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_roles`
--

DROP TABLE IF EXISTS `user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_roles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_roles`
--

LOCK TABLES `user_roles` WRITE;
/*!40000 ALTER TABLE `user_roles` DISABLE KEYS */;
INSERT INTO `user_roles` VALUES (1,'Super Admin',1,1,'2024-07-03 05:48:44.000000',NULL),(2,'admin',1,0,'2024-07-03 06:21:40.164403',NULL);
/*!40000 ALTER TABLE `user_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `email` varchar(60) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_loggedin` tinyint(1) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `created_by` varchar(50) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `deleted_at` datetime(6) DEFAULT NULL,
  `deleted_by` varchar(50) DEFAULT NULL,
  `branch_id` bigint DEFAULT NULL,
  `role_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  KEY `users_branch_id_d1b397ca_fk_branches_id` (`branch_id`),
  KEY `users_role_id_1900a745_fk_user_roles_id` (`role_id`),
  CONSTRAINT `users_branch_id_d1b397ca_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `users_role_id_1900a745_fk_user_roles_id` FOREIGN KEY (`role_id`) REFERENCES `user_roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'pbkdf2_sha256$600000$stmpe1GoCQkYQLXVmBwzeZ$suDCGpRTDjazw7Ec68a9kV6cqcsQs+t9D+1JPdbOQnw=','admin@atts.in','9677826365',1,0,'2024-07-03 06:14:30.990703',1,1,0,'2024-07-03 05:49:45.000000','1',NULL,NULL,NULL,NULL,1,1),(2,'pbkdf2_sha256$600000$YR85KFtZLkoN4gjwws7RTs$EQTRcCvZyqOj/4A1HNzjKj5/kNFujcUzKlLDiyreOmw=','boopathi@atts.in','9677826398',1,1,'2024-07-03 06:21:07.750481',0,1,0,'2024-07-03 06:19:55.619681','1',NULL,NULL,NULL,NULL,1,1),(3,'pbkdf2_sha256$600000$prGY2ZNg1aoAeevbR840z0$lpq7oN7YWsXVJv7IT1XDecWo7dF5YVgccN3ClXmfknM=','dhinagaran@atts.in','7305685960',1,1,'2024-07-03 06:21:56.989279',0,1,0,'2024-07-03 06:20:26.099700','1',NULL,NULL,NULL,NULL,1,1),(4,'pbkdf2_sha256$600000$1b5nB5Z5wK30D4CGvoEYgc$UTzUg8QR/5wzTWm4KLogUdnWm1mTdY14lOKFkwe8204=','jeyasekar@atts.in','9677826379',1,0,NULL,0,1,0,'2024-07-03 06:21:16.535906','1',NULL,NULL,NULL,NULL,1,1),(5,'pbkdf2_sha256$600000$LF90N0QJrqPo2Mf6WgbhPy$A3SpvYUp7WgK6Loybp43cNIxHRqPrkM+avWM122nQE4=','gokul@atts.in','6589654125',1,0,NULL,0,1,0,'2024-07-03 06:21:40.156401','1',NULL,NULL,NULL,NULL,1,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `value_addition_customer`
--

DROP TABLE IF EXISTS `value_addition_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `value_addition_customer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `from_weight` double NOT NULL,
  `to_weight` double NOT NULL,
  `max_fixed_rate` double DEFAULT NULL,
  `max_wastage_percent` double DEFAULT NULL,
  `max_flat_wastage` double DEFAULT NULL,
  `max_making_charge_gram` double DEFAULT NULL,
  `max_flat_making_charge` double DEFAULT NULL,
  `max_per_gram_rate` double DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `calculation_type_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  `metal_id` bigint NOT NULL,
  `stock_type_id` bigint NOT NULL,
  `sub_item_details_id` bigint NOT NULL,
  `tag_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `value_addition_custo_calculation_type_id_637f7c1f_fk_calculati` (`calculation_type_id`),
  KEY `value_addition_customer_created_by_id_ce43a6d8_fk_users_id` (`created_by_id`),
  KEY `value_addition_customer_metal_id_b2ba17e9_fk_metals_id` (`metal_id`),
  KEY `value_addition_customer_stock_type_id_ac694621_fk_stock_type_id` (`stock_type_id`),
  KEY `value_addition_custo_sub_item_details_id_61db99a9_fk_sub_item_` (`sub_item_details_id`),
  KEY `value_addition_customer_tag_type_id_edff24ba_fk_tag_type_id` (`tag_type_id`),
  CONSTRAINT `value_addition_custo_calculation_type_id_637f7c1f_fk_calculati` FOREIGN KEY (`calculation_type_id`) REFERENCES `calculation_type` (`id`),
  CONSTRAINT `value_addition_custo_sub_item_details_id_61db99a9_fk_sub_item_` FOREIGN KEY (`sub_item_details_id`) REFERENCES `sub_item_detail` (`id`),
  CONSTRAINT `value_addition_customer_created_by_id_ce43a6d8_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `value_addition_customer_metal_id_b2ba17e9_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `value_addition_customer_stock_type_id_ac694621_fk_stock_type_id` FOREIGN KEY (`stock_type_id`) REFERENCES `stock_type` (`id`),
  CONSTRAINT `value_addition_customer_tag_type_id_edff24ba_fk_tag_type_id` FOREIGN KEY (`tag_type_id`) REFERENCES `tag_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `value_addition_customer`
--

LOCK TABLES `value_addition_customer` WRITE;
/*!40000 ALTER TABLE `value_addition_customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `value_addition_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `value_addition_designer`
--

DROP TABLE IF EXISTS `value_addition_designer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `value_addition_designer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `purchase_touch` double DEFAULT NULL,
  `purchase_wastage_percent` double DEFAULT NULL,
  `purchase_flat_wastage` double DEFAULT NULL,
  `purchase_making_charge_gram` double DEFAULT NULL,
  `purchase_flat_making_charge` double DEFAULT NULL,
  `retail_touch` double DEFAULT NULL,
  `retail_wastage_percent` double DEFAULT NULL,
  `retail_flat_wastage` double DEFAULT NULL,
  `retail_making_charge_gram` double DEFAULT NULL,
  `retail_flat_making_charge` double DEFAULT NULL,
  `vip_touch` double DEFAULT NULL,
  `vip_wastage_percent` double DEFAULT NULL,
  `vip_flat_wastage` double DEFAULT NULL,
  `vip_making_charge_gram` double DEFAULT NULL,
  `vip_flat_making_charge` double DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `designer_name_id` bigint DEFAULT NULL,
  `item_name_id` bigint NOT NULL,
  `metal_name_id` bigint NOT NULL,
  `sub_item_name_id` bigint NOT NULL,
  `tag_type_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `value_addition_designer_created_by_id_da459e3a_fk_users_id` (`created_by_id`),
  KEY `value_addition_desig_designer_name_id_81c2a92f_fk_account_h` (`designer_name_id`),
  KEY `value_addition_designer_item_name_id_8d37dafd_fk_item_detail_id` (`item_name_id`),
  KEY `value_addition_designer_metal_name_id_750619ca_fk_metals_id` (`metal_name_id`),
  KEY `value_addition_desig_sub_item_name_id_01fd1630_fk_sub_item_` (`sub_item_name_id`),
  KEY `value_addition_designer_tag_type_id_635cde2d_fk_tag_type_id` (`tag_type_id`),
  CONSTRAINT `value_addition_desig_designer_name_id_81c2a92f_fk_account_h` FOREIGN KEY (`designer_name_id`) REFERENCES `account_head` (`id`),
  CONSTRAINT `value_addition_desig_sub_item_name_id_01fd1630_fk_sub_item_` FOREIGN KEY (`sub_item_name_id`) REFERENCES `sub_item_detail` (`id`),
  CONSTRAINT `value_addition_designer_created_by_id_da459e3a_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `value_addition_designer_item_name_id_8d37dafd_fk_item_detail_id` FOREIGN KEY (`item_name_id`) REFERENCES `item_detail` (`id`),
  CONSTRAINT `value_addition_designer_metal_name_id_750619ca_fk_metals_id` FOREIGN KEY (`metal_name_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `value_addition_designer_tag_type_id_635cde2d_fk_tag_type_id` FOREIGN KEY (`tag_type_id`) REFERENCES `tag_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `value_addition_designer`
--

LOCK TABLES `value_addition_designer` WRITE;
/*!40000 ALTER TABLE `value_addition_designer` DISABLE KEYS */;
/*!40000 ALTER TABLE `value_addition_designer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor_amountsettle`
--

DROP TABLE IF EXISTS `vendor_amountsettle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor_amountsettle` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_bill_no` varchar(20) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `purchase_order` varchar(50) DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `discount` double DEFAULT NULL,
  `cash_receivable` tinyint(1) DEFAULT NULL,
  `metal_receivable` tinyint(1) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `branch_id` bigint DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `designer_name_id` bigint DEFAULT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vendor_amountsettle_branch_id_fc3dcf75_fk_branches_id` (`branch_id`),
  KEY `vendor_amountsettle_created_by_id_a6963e94_fk_users_id` (`created_by_id`),
  KEY `vendor_amountsettle_designer_name_id_74caf38c_fk_account_head_id` (`designer_name_id`),
  KEY `vendor_amountsettle_modified_by_id_134af71d_fk_users_id` (`modified_by_id`),
  CONSTRAINT `vendor_amountsettle_branch_id_fc3dcf75_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `vendor_amountsettle_created_by_id_a6963e94_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `vendor_amountsettle_designer_name_id_74caf38c_fk_account_head_id` FOREIGN KEY (`designer_name_id`) REFERENCES `account_head` (`id`),
  CONSTRAINT `vendor_amountsettle_modified_by_id_134af71d_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor_amountsettle`
--

LOCK TABLES `vendor_amountsettle` WRITE;
/*!40000 ALTER TABLE `vendor_amountsettle` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendor_amountsettle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendorcash_rate_cut`
--

DROP TABLE IF EXISTS `vendorcash_rate_cut`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendorcash_rate_cut` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_bill_no` varchar(20) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `purchase_order` varchar(50) DEFAULT NULL,
  `pure_weight` double DEFAULT NULL,
  `rate` double DEFAULT NULL,
  `rate_cut` double DEFAULT NULL,
  `discount` double DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `branch_id` bigint DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `designer_name_id` bigint DEFAULT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vendorcash_rate_cut_branch_id_499b0432_fk_branches_id` (`branch_id`),
  KEY `vendorcash_rate_cut_created_by_id_90531ee3_fk_users_id` (`created_by_id`),
  KEY `vendorcash_rate_cut_designer_name_id_bead176a_fk_account_head_id` (`designer_name_id`),
  KEY `vendorcash_rate_cut_modified_by_id_62f2f107_fk_users_id` (`modified_by_id`),
  CONSTRAINT `vendorcash_rate_cut_branch_id_499b0432_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `vendorcash_rate_cut_created_by_id_90531ee3_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `vendorcash_rate_cut_designer_name_id_bead176a_fk_account_head_id` FOREIGN KEY (`designer_name_id`) REFERENCES `account_head` (`id`),
  CONSTRAINT `vendorcash_rate_cut_modified_by_id_62f2f107_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendorcash_rate_cut`
--

LOCK TABLES `vendorcash_rate_cut` WRITE;
/*!40000 ALTER TABLE `vendorcash_rate_cut` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendorcash_rate_cut` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendormetal_rate_cut`
--

DROP TABLE IF EXISTS `vendormetal_rate_cut`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendormetal_rate_cut` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_bill_no` varchar(20) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `purchase_order` varchar(20) DEFAULT NULL,
  `metal_weight` double DEFAULT NULL,
  `pure_calculation` double DEFAULT NULL,
  `pure_weight` double DEFAULT NULL,
  `discount` double DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `branch_id` bigint DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `designer_name_id` bigint DEFAULT NULL,
  `metal_id` bigint DEFAULT NULL,
  `modified_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vendormetal_rate_cut_branch_id_411d6a82_fk_branches_id` (`branch_id`),
  KEY `vendormetal_rate_cut_created_by_id_7c4852cf_fk_users_id` (`created_by_id`),
  KEY `vendormetal_rate_cut_designer_name_id_08cea50f_fk_account_h` (`designer_name_id`),
  KEY `vendormetal_rate_cut_metal_id_6b9cd1da_fk_metals_id` (`metal_id`),
  KEY `vendormetal_rate_cut_modified_by_id_d4631bd9_fk_users_id` (`modified_by_id`),
  CONSTRAINT `vendormetal_rate_cut_branch_id_411d6a82_fk_branches_id` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `vendormetal_rate_cut_created_by_id_7c4852cf_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `vendormetal_rate_cut_designer_name_id_08cea50f_fk_account_h` FOREIGN KEY (`designer_name_id`) REFERENCES `account_head` (`id`),
  CONSTRAINT `vendormetal_rate_cut_metal_id_6b9cd1da_fk_metals_id` FOREIGN KEY (`metal_id`) REFERENCES `metals` (`id`),
  CONSTRAINT `vendormetal_rate_cut_modified_by_id_d4631bd9_fk_users_id` FOREIGN KEY (`modified_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendormetal_rate_cut`
--

LOCK TABLES `vendormetal_rate_cut` WRITE;
/*!40000 ALTER TABLE `vendormetal_rate_cut` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendormetal_rate_cut` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voucher_type`
--

DROP TABLE IF EXISTS `voucher_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `voucher_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `voucher_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `voucher_name` (`voucher_name`),
  KEY `voucher_type_created_by_id_6e96f0b4_fk_users_id` (`created_by_id`),
  CONSTRAINT `voucher_type_created_by_id_6e96f0b4_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voucher_type`
--

LOCK TABLES `voucher_type` WRITE;
/*!40000 ALTER TABLE `voucher_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `voucher_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weight_calculation`
--

DROP TABLE IF EXISTS `weight_calculation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weight_calculation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `wastage_percent` double NOT NULL,
  `flat_wastage` double NOT NULL,
  `making_charge_gram` double NOT NULL,
  `flat_making_charge` double NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `item_details_id` bigint NOT NULL,
  `making_charge_calculation_id` bigint NOT NULL,
  `wastage_calculation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `weight_calculation_created_by_id_c32fa434_fk_users_id` (`created_by_id`),
  KEY `weight_calculation_item_details_id_f5a0f315_fk_item_detail_id` (`item_details_id`),
  KEY `weight_calculation_making_charge_calcul_4b823c5f_fk_weight_ty` (`making_charge_calculation_id`),
  KEY `weight_calculation_wastage_calculation__19de4dcd_fk_weight_ty` (`wastage_calculation_id`),
  CONSTRAINT `weight_calculation_created_by_id_c32fa434_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `weight_calculation_item_details_id_f5a0f315_fk_item_detail_id` FOREIGN KEY (`item_details_id`) REFERENCES `item_detail` (`id`),
  CONSTRAINT `weight_calculation_making_charge_calcul_4b823c5f_fk_weight_ty` FOREIGN KEY (`making_charge_calculation_id`) REFERENCES `weight_type` (`id`),
  CONSTRAINT `weight_calculation_wastage_calculation__19de4dcd_fk_weight_ty` FOREIGN KEY (`wastage_calculation_id`) REFERENCES `weight_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weight_calculation`
--

LOCK TABLES `weight_calculation` WRITE;
/*!40000 ALTER TABLE `weight_calculation` DISABLE KEYS */;
/*!40000 ALTER TABLE `weight_calculation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weight_type`
--

DROP TABLE IF EXISTS `weight_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weight_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `weight_name` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `modified_at` datetime(6) DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `weight_name` (`weight_name`),
  KEY `weight_type_created_by_id_85d12e01_fk_users_id` (`created_by_id`),
  CONSTRAINT `weight_type_created_by_id_85d12e01_fk_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weight_type`
--

LOCK TABLES `weight_type` WRITE;
/*!40000 ALTER TABLE `weight_type` DISABLE KEYS */;
INSERT INTO `weight_type` VALUES (1,'Gross Weight',1,NULL,NULL,NULL,NULL),(2,'Net Weight',1,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `weight_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-03 11:52:22
