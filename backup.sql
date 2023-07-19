-- MySQL dump 10.13  Distrib 8.0.26, for Linux (x86_64)
--
-- Host: localhost    Database: SUPPLY_CHAIN
-- ------------------------------------------------------
-- Server version	8.0.26-0ubuntu0.21.04.3

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
-- Table structure for table `CUSTOMERS`
--

DROP TABLE IF EXISTS `CUSTOMERS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CUSTOMERS` (
  `CUSTOMER_ID` int NOT NULL,
  `F_NAME` varchar(15) NOT NULL,
  `M_NAME` varchar(15) DEFAULT NULL,
  `L_NAME` varchar(15) NOT NULL,
  `ADDRESS` varchar(30) DEFAULT NULL,
  `PHONE_NO` char(10) DEFAULT NULL,
  `EMAIL_ID` varchar(20) DEFAULT NULL,
  `PASSWORD` varchar(20) NOT NULL,
  PRIMARY KEY (`CUSTOMER_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CUSTOMERS`
--

LOCK TABLES `CUSTOMERS` WRITE;
/*!40000 ALTER TABLE `CUSTOMERS` DISABLE KEYS */;
INSERT INTO `CUSTOMERS` VALUES (101,'Rakesh','Kumar','Tripathi','13/A RK Nagar Delhi','9125567874','rkt@gm.com','123rkt'),(102,'Mukesh',NULL,'Gupta','13/C DK Nagar Delhi','9123367874','mt@gm.com','123mt'),(103,'Raj',NULL,'Dutta','99/Z DK Nagar Chennai','9123367868','rd@gm.com','123rd'),(104,'Mahendra','Singh','Raina','1/A Ram Nagar Panji','9125567875','msr@gm.com','123msr');
/*!40000 ALTER TABLE `CUSTOMERS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CUSTOMER_HAS_LOGINSESSION`
--

DROP TABLE IF EXISTS `CUSTOMER_HAS_LOGINSESSION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CUSTOMER_HAS_LOGINSESSION` (
  `LOGIN_TIME` datetime NOT NULL,
  `LOGOUT_TIME` datetime NOT NULL,
  `CUSTOMER_ID` int NOT NULL,
  `TIME_SPENT` int NOT NULL,
  PRIMARY KEY (`LOGIN_TIME`,`LOGOUT_TIME`),
  KEY `CUSTOMER_ID` (`CUSTOMER_ID`),
  CONSTRAINT `CUSTOMER_HAS_LOGINSESSION_ibfk_1` FOREIGN KEY (`CUSTOMER_ID`) REFERENCES `CUSTOMERS` (`CUSTOMER_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CUSTOMER_HAS_LOGINSESSION`
--

LOCK TABLES `CUSTOMER_HAS_LOGINSESSION` WRITE;
/*!40000 ALTER TABLE `CUSTOMER_HAS_LOGINSESSION` DISABLE KEYS */;
INSERT INTO `CUSTOMER_HAS_LOGINSESSION` VALUES ('2021-02-05 17:45:07','2021-02-05 17:22:07',102,37),('2021-05-02 07:45:17','2021-05-02 08:17:07',103,32),('2021-05-05 07:45:37','2021-05-05 09:27:27',101,102),('2021-05-05 12:45:35','2021-05-05 13:39:54',104,54);
/*!40000 ALTER TABLE `CUSTOMER_HAS_LOGINSESSION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FACTORY`
--

DROP TABLE IF EXISTS `FACTORY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FACTORY` (
  `FACTORY_ID` int NOT NULL,
  `FACTORY_NAME` varchar(50) NOT NULL,
  `PHONE_NO` char(10) DEFAULT NULL,
  `ADDRESS` varchar(50) DEFAULT NULL,
  `PASSWORD` varchar(20) NOT NULL,
  PRIMARY KEY (`FACTORY_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FACTORY`
--

LOCK TABLES `FACTORY` WRITE;
/*!40000 ALTER TABLE `FACTORY` DISABLE KEYS */;
INSERT INTO `FACTORY` VALUES (201,'AK_BIRLA Factory','9067452311','AK_BIRLA Factory Vigyan Nagar New Delhi','factory1'),(202,'JK_LAL Factory','9067452312','AK_LAL Factory Chand Nagar Mumbai','factory2'),(203,'SK & SONS Pharmaceuticals','9067452313','Street-10 Surya Vihar Patna','factory3'),(204,'LAKME_COSMETICS','9674523124','Lakme Cosmetics Jam Nagar Mumbai','factory4'),(205,'CHOCOLATE_KINGDOM','9674523125','East Block Chandra Vihar Jaipur','factory5');
/*!40000 ALTER TABLE `FACTORY` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER`
--

DROP TABLE IF EXISTS `FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER` (
  `SUPPLIER_ID` int NOT NULL,
  `PRODUCT_ID` int NOT NULL,
  `FACTORY_ID` int NOT NULL,
  `QUANTITY` int DEFAULT NULL,
  `DATE_TIME` datetime NOT NULL,
  PRIMARY KEY (`SUPPLIER_ID`,`PRODUCT_ID`,`FACTORY_ID`,`DATE_TIME`),
  KEY `PRODUCT_ID` (`PRODUCT_ID`),
  KEY `FACTORY_ID` (`FACTORY_ID`),
  CONSTRAINT `FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER_ibfk_1` FOREIGN KEY (`SUPPLIER_ID`) REFERENCES `SUPPLIER` (`SUPPLIER_ID`) ON DELETE CASCADE,
  CONSTRAINT `FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER_ibfk_2` FOREIGN KEY (`PRODUCT_ID`) REFERENCES `PRODUCT` (`PRODUCT_ID`) ON DELETE CASCADE,
  CONSTRAINT `FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER_ibfk_3` FOREIGN KEY (`FACTORY_ID`) REFERENCES `FACTORY` (`FACTORY_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER`
--

LOCK TABLES `FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER` WRITE;
/*!40000 ALTER TABLE `FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER` DISABLE KEYS */;
INSERT INTO `FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER` VALUES (901,402,203,10,'2017-01-11 13:12:38'),(902,302,204,40,'2020-07-11 01:45:06'),(903,501,201,20,'2019-07-29 19:48:18'),(904,301,205,25,'2020-11-11 23:45:12'),(905,601,202,30,'2018-11-28 05:23:35');
/*!40000 ALTER TABLE `FACTORY_SELLS_PRODUCT_BOUGHTBY_SUPPLIER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PRODUCT`
--

DROP TABLE IF EXISTS `PRODUCT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PRODUCT` (
  `PRODUCT_ID` int NOT NULL,
  `PRODUCT_NAME` varchar(15) NOT NULL,
  `BATCH_NO` char(10) NOT NULL,
  `BEST_BEFORE` int DEFAULT NULL,
  `MFG_DATE` date NOT NULL,
  `EXPIRY_DATE` date NOT NULL,
  `IS_EXPIRED` tinyint NOT NULL,
  `PHARMACEUTICAL_FLAG` tinyint DEFAULT NULL,
  `EDIBLE_FLAG` tinyint DEFAULT NULL,
  `COSMETIC_FLAG` tinyint DEFAULT NULL,
  `BOOKS_FLAG` tinyint DEFAULT NULL,
  `PRICE` int NOT NULL,
  PRIMARY KEY (`PRODUCT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PRODUCT`
--

LOCK TABLES `PRODUCT` WRITE;
/*!40000 ALTER TABLE `PRODUCT` DISABLE KEYS */;
INSERT INTO `PRODUCT` VALUES (301,'5 Star','100',9,'2008-02-13','2008-11-13',0,0,1,0,0,10),(302,'Nail Poslish','102',22,'2007-02-13','2008-12-13',0,0,0,1,0,80),(402,'Paracetamol','102',22,'2007-02-13','2008-12-13',1,1,0,0,0,5),(501,'HC Verma','100',874,'2008-02-13','2080-11-13',0,0,0,0,1,380),(601,'Glassware Jugs','203',1000,'2020-03-15','2120-03-15',0,0,0,0,0,790);
/*!40000 ALTER TABLE `PRODUCT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PRODUCT_MADEBY_FACTORY`
--

DROP TABLE IF EXISTS `PRODUCT_MADEBY_FACTORY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PRODUCT_MADEBY_FACTORY` (
  `PRODUCT_ID` int NOT NULL,
  `FACTORY_ID` int NOT NULL,
  `QUANTITY` int DEFAULT NULL,
  PRIMARY KEY (`PRODUCT_ID`,`FACTORY_ID`),
  KEY `FACTORY_ID` (`FACTORY_ID`),
  CONSTRAINT `PRODUCT_MADEBY_FACTORY_ibfk_1` FOREIGN KEY (`PRODUCT_ID`) REFERENCES `PRODUCT` (`PRODUCT_ID`) ON DELETE CASCADE,
  CONSTRAINT `PRODUCT_MADEBY_FACTORY_ibfk_2` FOREIGN KEY (`FACTORY_ID`) REFERENCES `FACTORY` (`FACTORY_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PRODUCT_MADEBY_FACTORY`
--

LOCK TABLES `PRODUCT_MADEBY_FACTORY` WRITE;
/*!40000 ALTER TABLE `PRODUCT_MADEBY_FACTORY` DISABLE KEYS */;
INSERT INTO `PRODUCT_MADEBY_FACTORY` VALUES (301,205,80),(302,204,50),(402,203,200),(501,201,50),(601,202,100);
/*!40000 ALTER TABLE `PRODUCT_MADEBY_FACTORY` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RETAILER`
--

DROP TABLE IF EXISTS `RETAILER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RETAILER` (
  `RETAILER_ID` int NOT NULL,
  `RETAILER_NAME` varchar(50) NOT NULL,
  `PHONE_NO` char(10) DEFAULT NULL,
  `ADDRESS` varchar(30) DEFAULT NULL,
  `PASSWORD` varchar(20) NOT NULL,
  PRIMARY KEY (`RETAILER_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RETAILER`
--

LOCK TABLES `RETAILER` WRITE;
/*!40000 ALTER TABLE `RETAILER` DISABLE KEYS */;
INSERT INTO `RETAILER` VALUES (601,'Rakesh Stores','9090909012','13/C Setcor 6 Delhi','ret1'),(602,'Mukesh Stores','9090909013','13/C Setcor 10 Delhi','ret2'),(603,'Suresh Stores','9090909014','13/C Setcor 9 Delhi','ret3'),(604,'Bhaesh Stores','9090909015','13/C Setcor 8 Delhi','ret4'),(605,'Hari Stores','9090909016','13/C Setcor 7 Delhi','ret5');
/*!40000 ALTER TABLE `RETAILER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RETAILER_HAS_PRODUCT`
--

DROP TABLE IF EXISTS `RETAILER_HAS_PRODUCT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RETAILER_HAS_PRODUCT` (
  `PRODUCT_ID` int NOT NULL,
  `RETAILER_ID` int NOT NULL,
  `QUANTITY` int DEFAULT NULL,
  PRIMARY KEY (`PRODUCT_ID`,`RETAILER_ID`),
  KEY `RETAILER_ID` (`RETAILER_ID`),
  CONSTRAINT `RETAILER_HAS_PRODUCT_ibfk_1` FOREIGN KEY (`PRODUCT_ID`) REFERENCES `PRODUCT` (`PRODUCT_ID`) ON DELETE CASCADE,
  CONSTRAINT `RETAILER_HAS_PRODUCT_ibfk_2` FOREIGN KEY (`RETAILER_ID`) REFERENCES `RETAILER` (`RETAILER_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RETAILER_HAS_PRODUCT`
--

LOCK TABLES `RETAILER_HAS_PRODUCT` WRITE;
/*!40000 ALTER TABLE `RETAILER_HAS_PRODUCT` DISABLE KEYS */;
INSERT INTO `RETAILER_HAS_PRODUCT` VALUES (301,601,18),(301,604,30),(302,603,10),(302,605,30),(402,601,20),(402,602,20),(402,603,20),(402,605,30),(501,601,20),(501,602,17);
/*!40000 ALTER TABLE `RETAILER_HAS_PRODUCT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER`
--

DROP TABLE IF EXISTS `RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER` (
  `CUSTOMER_ID` int NOT NULL,
  `PRODUCT_ID` int NOT NULL,
  `RETAILER_ID` int NOT NULL,
  `QUANTITY` int NOT NULL,
  `DATE_TIME` datetime NOT NULL,
  PRIMARY KEY (`CUSTOMER_ID`,`PRODUCT_ID`,`RETAILER_ID`,`DATE_TIME`),
  KEY `PRODUCT_ID` (`PRODUCT_ID`),
  KEY `RETAILER_ID` (`RETAILER_ID`),
  CONSTRAINT `RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER_ibfk_1` FOREIGN KEY (`CUSTOMER_ID`) REFERENCES `CUSTOMERS` (`CUSTOMER_ID`) ON DELETE CASCADE,
  CONSTRAINT `RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER_ibfk_2` FOREIGN KEY (`PRODUCT_ID`) REFERENCES `PRODUCT` (`PRODUCT_ID`) ON DELETE CASCADE,
  CONSTRAINT `RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER_ibfk_3` FOREIGN KEY (`RETAILER_ID`) REFERENCES `RETAILER` (`RETAILER_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER`
--

LOCK TABLES `RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER` WRITE;
/*!40000 ALTER TABLE `RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER` DISABLE KEYS */;
INSERT INTO `RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER` VALUES (101,301,601,2,'2021-10-26 20:50:21'),(101,301,604,3,'2020-10-20 23:54:12'),(101,302,605,3,'2019-10-18 13:27:12'),(101,402,602,7,'2020-10-20 23:45:12'),(101,501,602,11,'2020-12-31 08:37:00'),(101,501,602,4,'2021-10-26 20:15:39'),(102,302,603,2,'2017-04-20 23:54:12'),(102,302,603,9,'2021-10-26 20:56:59'),(102,402,603,1,'2020-01-20 05:54:12'),(102,501,602,11,'2018-10-20 12:54:12'),(103,402,605,4,'2020-10-17 03:34:12'),(103,501,601,8,'2020-09-20 13:54:12');
/*!40000 ALTER TABLE `RETAILER_SELLS_PRODUCT_BOUGHTBY_CUSTOMER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SUPPLIER`
--

DROP TABLE IF EXISTS `SUPPLIER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SUPPLIER` (
  `SUPPLIER_ID` int NOT NULL,
  `SUPPLIER_NAME` varchar(50) NOT NULL,
  `PHONE_NO` char(10) DEFAULT NULL,
  `ADDRESS` varchar(30) DEFAULT NULL,
  `PASSWORD` varchar(20) NOT NULL,
  PRIMARY KEY (`SUPPLIER_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SUPPLIER`
--

LOCK TABLES `SUPPLIER` WRITE;
/*!40000 ALTER TABLE `SUPPLIER` DISABLE KEYS */;
INSERT INTO `SUPPLIER` VALUES (901,'Ram Sahoo','9090123450','512 A Market New Delhi','supp901'),(902,'Lakhan Roy','9090123451','512 D Market Hyderabad','supp902'),(903,'Soham Das','9090123452','52 G Market Chennai','supp903'),(904,'Bheem Sen','9090123420','512 C Market Chandigarh','supp904'),(905,'Shyam Lal','9078565678','12 FG Rajnandgaon CG','supp905');
/*!40000 ALTER TABLE `SUPPLIER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SUPPLIER_HAS_PRODUCT`
--

DROP TABLE IF EXISTS `SUPPLIER_HAS_PRODUCT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SUPPLIER_HAS_PRODUCT` (
  `SUPPLIER_ID` int NOT NULL,
  `PRODUCT_ID` int NOT NULL,
  `QUANTITY` int DEFAULT NULL,
  PRIMARY KEY (`SUPPLIER_ID`,`PRODUCT_ID`),
  KEY `PRODUCT_ID` (`PRODUCT_ID`),
  CONSTRAINT `SUPPLIER_HAS_PRODUCT_ibfk_1` FOREIGN KEY (`SUPPLIER_ID`) REFERENCES `SUPPLIER` (`SUPPLIER_ID`) ON DELETE CASCADE,
  CONSTRAINT `SUPPLIER_HAS_PRODUCT_ibfk_2` FOREIGN KEY (`PRODUCT_ID`) REFERENCES `PRODUCT` (`PRODUCT_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SUPPLIER_HAS_PRODUCT`
--

LOCK TABLES `SUPPLIER_HAS_PRODUCT` WRITE;
/*!40000 ALTER TABLE `SUPPLIER_HAS_PRODUCT` DISABLE KEYS */;
INSERT INTO `SUPPLIER_HAS_PRODUCT` VALUES (901,402,70),(902,302,50),(903,501,60),(904,301,80),(905,601,50);
/*!40000 ALTER TABLE `SUPPLIER_HAS_PRODUCT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY`
--

DROP TABLE IF EXISTS `SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY` (
  `SUPPLIER_ID` int NOT NULL,
  `PRODUCT_ID` int NOT NULL,
  `RETAILER_ID` int NOT NULL,
  `FACTORY_ID` int NOT NULL,
  `QUANTITY` int DEFAULT NULL,
  `DATE_TIME` datetime NOT NULL,
  PRIMARY KEY (`SUPPLIER_ID`,`PRODUCT_ID`,`RETAILER_ID`,`FACTORY_ID`,`DATE_TIME`),
  KEY `PRODUCT_ID` (`PRODUCT_ID`),
  KEY `RETAILER_ID` (`RETAILER_ID`),
  KEY `FACTORY_ID` (`FACTORY_ID`),
  CONSTRAINT `SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY_ibfk_1` FOREIGN KEY (`SUPPLIER_ID`) REFERENCES `SUPPLIER` (`SUPPLIER_ID`) ON DELETE CASCADE,
  CONSTRAINT `SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY_ibfk_2` FOREIGN KEY (`PRODUCT_ID`) REFERENCES `PRODUCT` (`PRODUCT_ID`) ON DELETE CASCADE,
  CONSTRAINT `SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY_ibfk_3` FOREIGN KEY (`RETAILER_ID`) REFERENCES `RETAILER` (`RETAILER_ID`) ON DELETE CASCADE,
  CONSTRAINT `SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY_ibfk_4` FOREIGN KEY (`FACTORY_ID`) REFERENCES `FACTORY` (`FACTORY_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY`
--

LOCK TABLES `SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY` WRITE;
/*!40000 ALTER TABLE `SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY` DISABLE KEYS */;
INSERT INTO `SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY` VALUES (901,402,603,203,15,'2017-02-11 13:12:38'),(902,302,602,204,31,'2020-08-11 01:45:06'),(903,501,604,201,18,'2019-08-29 19:48:18'),(904,301,601,205,28,'2021-02-26 23:45:12'),(905,601,605,202,10,'2021-04-29 09:18:19');
/*!40000 ALTER TABLE `SUPPLIER_SELLS_PRODUCT_BOUGHTBY_RETAILER_MADEBY_FACTORY` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USER_REVIEW`
--

DROP TABLE IF EXISTS `USER_REVIEW`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USER_REVIEW` (
  `PRODUCT_ID` int NOT NULL,
  `CUSTOMER_ID` int NOT NULL,
  `USER_RATING` int NOT NULL,
  PRIMARY KEY (`PRODUCT_ID`,`CUSTOMER_ID`),
  KEY `CUSTOMER_ID` (`CUSTOMER_ID`),
  CONSTRAINT `USER_REVIEW_ibfk_1` FOREIGN KEY (`PRODUCT_ID`) REFERENCES `PRODUCT` (`PRODUCT_ID`) ON DELETE CASCADE,
  CONSTRAINT `USER_REVIEW_ibfk_2` FOREIGN KEY (`CUSTOMER_ID`) REFERENCES `CUSTOMERS` (`CUSTOMER_ID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USER_REVIEW`
--

LOCK TABLES `USER_REVIEW` WRITE;
/*!40000 ALTER TABLE `USER_REVIEW` DISABLE KEYS */;
INSERT INTO `USER_REVIEW` VALUES (301,101,5),(302,102,4),(402,101,4),(402,102,2),(402,103,3),(501,101,3),(501,102,4),(501,103,4);
/*!40000 ALTER TABLE `USER_REVIEW` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-26 15:39:40