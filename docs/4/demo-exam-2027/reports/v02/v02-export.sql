/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.16-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: dkip2027_v02
-- ------------------------------------------------------
-- Server version	10.11.16-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `counterparty`
--

DROP TABLE IF EXISTS `counterparty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `counterparty` (
  `id` varchar(32) NOT NULL,
  `name` varchar(255) NOT NULL,
  `inn` varchar(20) NOT NULL DEFAULT '',
  `address` varchar(500) NOT NULL,
  `phone` varchar(64) NOT NULL,
  `party_type` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `counterparty`
--

LOCK TABLES `counterparty` WRITE;
/*!40000 ALTER TABLE `counterparty` DISABLE KEYS */;
INSERT INTO `counterparty` VALUES
('002000001','Магазин «Колос-1»','','Учебный город, улица Производственная, 2, офис 1','+79990020001','Покупатель'),
('002000002','Торговый дом «Колос-2»','','Учебный город, улица Производственная, 2, офис 2','+79990020002','Покупатель'),
('002000003','Студия «Колос-3»','','Учебный город, улица Производственная, 2, офис 3','+79990020003','Покупатель'),
('002000004','Магазин подарков «Колос-4»','','Учебный город, улица Производственная, 2, офис 4','+79990020004','Покупатель'),
('002000005','Мастерская «Колос-5»','','Учебный город, улица Производственная, 2, офис 5','+79990020005','Покупатель'),
('002000006','Оптовый склад «Колос-6»','','Учебный город, улица Производственная, 2, офис 6','+79990020006','Покупатель'),
('V02-MAKER','Пекарня «Колос»','','Учебный город, улица Производственная, 2','+79990020000','Изготовитель');
/*!40000 ALTER TABLE `counterparty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_order`
--

DROP TABLE IF EXISTS `customer_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doc_no` varchar(64) NOT NULL,
  `doc_date` date NOT NULL,
  `due_date` date NOT NULL,
  `customer_id` varchar(32) NOT NULL,
  `executor_id` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_order_no` (`doc_no`),
  KEY `fk_order_customer` (`customer_id`),
  KEY `fk_order_executor` (`executor_id`),
  CONSTRAINT `fk_order_customer` FOREIGN KEY (`customer_id`) REFERENCES `counterparty` (`id`),
  CONSTRAINT `fk_order_executor` FOREIGN KEY (`executor_id`) REFERENCES `counterparty` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_order`
--

LOCK TABLES `customer_order` WRITE;
/*!40000 ALTER TABLE `customer_order` DISABLE KEYS */;
INSERT INTO `customer_order` VALUES
(1,'V02-01','2027-03-15','2027-03-22','002000001','V02-MAKER');
/*!40000 ALTER TABLE `customer_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_order_line`
--

DROP TABLE IF EXISTS `customer_order_line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_order_line` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `qty` decimal(14,3) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_line_order` (`order_id`),
  KEY `fk_line_product` (`product_id`),
  CONSTRAINT `fk_line_order` FOREIGN KEY (`order_id`) REFERENCES `customer_order` (`id`),
  CONSTRAINT `fk_line_product` FOREIGN KEY (`product_id`) REFERENCES `item` (`id`),
  CONSTRAINT `ck_line_qty` CHECK (`qty` > 0)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_order_line`
--

LOCK TABLES `customer_order_line` WRITE;
/*!40000 ALTER TABLE `customer_order_line` DISABLE KEYS */;
INSERT INTO `customer_order_line` VALUES
(1,1,1,40.000);
/*!40000 ALTER TABLE `customer_order_line` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(64) NOT NULL,
  `name` varchar(255) NOT NULL,
  `kind` varchar(16) NOT NULL,
  `unit` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_item_code` (`code`),
  CONSTRAINT `ck_item_kind` CHECK (`kind` in ('product','material','operation'))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES
(1,'V02-P01','Хлеб ржаной 500 г','product','ед.'),
(2,'V02-M01','Мука ржаная','material','кг'),
(3,'V02-M02','Закваска','material','кг'),
(4,'V02-M03','Пакет','material','шт'),
(5,'V02-O01','Замес и формование','operation','ч'),
(6,'V02-O02','Выпечка','operation','ч');
/*!40000 ALTER TABLE `item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `price`
--

DROP TABLE IF EXISTS `price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `price` (
  `item_id` int(11) NOT NULL,
  `valid_from` date NOT NULL,
  `amount` decimal(14,2) NOT NULL,
  PRIMARY KEY (`item_id`,`valid_from`),
  CONSTRAINT `fk_price_item` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
  CONSTRAINT `ck_price_amount` CHECK (`amount` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `price`
--

LOCK TABLES `price` WRITE;
/*!40000 ALTER TABLE `price` DISABLE KEYS */;
INSERT INTO `price` VALUES
(2,'2027-03-01',65.00),
(3,'2027-03-01',100.00),
(4,'2027-03-01',4.00),
(5,'2027-03-01',500.00),
(6,'2027-03-01',700.00);
/*!40000 ALTER TABLE `price` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `production_order`
--

DROP TABLE IF EXISTS `production_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `production_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doc_no` varchar(64) NOT NULL,
  `order_id` int(11) NOT NULL,
  `launch_date` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_production_no` (`doc_no`),
  KEY `fk_prod_order` (`order_id`),
  CONSTRAINT `fk_prod_order` FOREIGN KEY (`order_id`) REFERENCES `customer_order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `production_order`
--

LOCK TABLES `production_order` WRITE;
/*!40000 ALTER TABLE `production_order` DISABLE KEYS */;
INSERT INTO `production_order` VALUES
(1,'V02-P01',1,'2027-03-16');
/*!40000 ALTER TABLE `production_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `production_product`
--

DROP TABLE IF EXISTS `production_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `production_product` (
  `production_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `qty` decimal(14,3) NOT NULL,
  PRIMARY KEY (`production_id`,`product_id`),
  KEY `fk_pp_item` (`product_id`),
  CONSTRAINT `fk_pp_item` FOREIGN KEY (`product_id`) REFERENCES `item` (`id`),
  CONSTRAINT `fk_pp_prod` FOREIGN KEY (`production_id`) REFERENCES `production_order` (`id`),
  CONSTRAINT `ck_pp_qty` CHECK (`qty` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `production_product`
--

LOCK TABLES `production_product` WRITE;
/*!40000 ALTER TABLE `production_product` DISABLE KEYS */;
INSERT INTO `production_product` VALUES
(1,1,40.000);
/*!40000 ALTER TABLE `production_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `production_resource`
--

DROP TABLE IF EXISTS `production_resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `production_resource` (
  `production_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `qty` decimal(14,3) NOT NULL,
  PRIMARY KEY (`production_id`,`item_id`),
  KEY `fk_pr_item` (`item_id`),
  CONSTRAINT `fk_pr_item` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
  CONSTRAINT `fk_pr_prod` FOREIGN KEY (`production_id`) REFERENCES `production_order` (`id`),
  CONSTRAINT `ck_pr_qty` CHECK (`qty` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `production_resource`
--

LOCK TABLES `production_resource` WRITE;
/*!40000 ALTER TABLE `production_resource` DISABLE KEYS */;
INSERT INTO `production_resource` VALUES
(1,2,12.800),
(1,3,3.200),
(1,4,40.000),
(1,5,1.600),
(1,6,0.800);
/*!40000 ALTER TABLE `production_resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `specification`
--

DROP TABLE IF EXISTS `specification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `specification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `output_qty` decimal(14,3) NOT NULL,
  `manufacturer_id` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_spec_product` (`product_id`),
  KEY `fk_spec_maker` (`manufacturer_id`),
  CONSTRAINT `fk_spec_maker` FOREIGN KEY (`manufacturer_id`) REFERENCES `counterparty` (`id`),
  CONSTRAINT `fk_spec_product` FOREIGN KEY (`product_id`) REFERENCES `item` (`id`),
  CONSTRAINT `ck_spec_output` CHECK (`output_qty` > 0)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `specification`
--

LOCK TABLES `specification` WRITE;
/*!40000 ALTER TABLE `specification` DISABLE KEYS */;
INSERT INTO `specification` VALUES
(1,1,'Хлеб ржаной 500 г',1.000,'V02-MAKER');
/*!40000 ALTER TABLE `specification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `specification_component`
--

DROP TABLE IF EXISTS `specification_component`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `specification_component` (
  `specification_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `qty` decimal(14,3) NOT NULL,
  `time_norm` decimal(14,4) DEFAULT NULL,
  PRIMARY KEY (`specification_id`,`item_id`),
  KEY `fk_comp_item` (`item_id`),
  CONSTRAINT `fk_comp_item` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
  CONSTRAINT `fk_comp_spec` FOREIGN KEY (`specification_id`) REFERENCES `specification` (`id`),
  CONSTRAINT `ck_comp_qty` CHECK (`qty` > 0),
  CONSTRAINT `ck_comp_time` CHECK (`time_norm` is null or `time_norm` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `specification_component`
--

LOCK TABLES `specification_component` WRITE;
/*!40000 ALTER TABLE `specification_component` DISABLE KEYS */;
INSERT INTO `specification_component` VALUES
(1,2,0.320,NULL),
(1,3,0.080,NULL),
(1,4,1.000,NULL),
(1,5,1.000,0.0400),
(1,6,1.000,0.0200);
/*!40000 ALTER TABLE `specification_component` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'dkip2027_v02'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07  9:21:17
