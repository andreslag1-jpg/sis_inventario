CREATE DATABASE  IF NOT EXISTS `tienda_online` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `tienda_online`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: tienda_online
-- ------------------------------------------------------
-- Server version	9.2.0

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
-- Table structure for table `detalle_orden`
--

DROP TABLE IF EXISTS `detalle_orden`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_orden` (
  `id_detalle` int NOT NULL AUTO_INCREMENT,
  `id_orden` int NOT NULL,
  `id_producto` int NOT NULL,
  `cantidad` int DEFAULT NULL,
  `subtotal` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_detalle`),
  KEY `idx_detalle_orden` (`id_orden`),
  KEY `idx_detalle_producto` (`id_producto`),
  CONSTRAINT `detalle_orden_ibfk_1` FOREIGN KEY (`id_orden`) REFERENCES `orden` (`id_orden`),
  CONSTRAINT `detalle_orden_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_orden`
--

LOCK TABLES `detalle_orden` WRITE;
/*!40000 ALTER TABLE `detalle_orden` DISABLE KEYS */;
INSERT INTO `detalle_orden` VALUES (1,1,3,1,165000.00),(2,2,1,1,45000.00),(3,2,4,1,85000.00),(4,3,1,1,45000.00),(5,4,4,1,85000.00),(6,5,2,1,120000.00),(7,6,2,2,240000.00),(8,6,1,1,45000.00),(9,7,3,1,165000.00),(10,8,4,2,170000.00);
/*!40000 ALTER TABLE `detalle_orden` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario`
--

DROP TABLE IF EXISTS `inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario` (
  `id_inventario` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `cantidad` int DEFAULT NULL,
  `ubicacion_bodega` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_inventario`),
  KEY `idx_inventario_producto` (`id_producto`),
  CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario`
--

LOCK TABLES `inventario` WRITE;
/*!40000 ALTER TABLE `inventario` DISABLE KEYS */;
INSERT INTO `inventario` VALUES (5,1,50,'Bodega Central'),(6,2,30,'Bodega Norte'),(7,3,25,'Bodega Sur'),(8,4,40,'Bodega Central'),(9,1,50,'Bodega Central'),(10,2,80,'Bodega Norte'),(11,3,40,'Bodega Sur'),(16,8,29,'Bodega Central'),(17,5,25,'Bodega Norte');
/*!40000 ALTER TABLE `inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orden`
--

DROP TABLE IF EXISTS `orden`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orden` (
  `id_orden` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `fecha` date DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `envio` varchar(100) DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_orden`),
  KEY `idx_orden_usuario` (`id_usuario`),
  CONSTRAINT `orden_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orden`
--

LOCK TABLES `orden` WRITE;
/*!40000 ALTER TABLE `orden` DISABLE KEYS */;
INSERT INTO `orden` VALUES (1,1,'2025-07-10',165000.00,'Servientrega','Completado'),(2,2,'2025-07-13',125000.00,'Coordinadora','Pendiente'),(3,1,'2023-02-15',45000.00,'Servientrega','Completado'),(4,2,'2023-06-10',85000.00,'Servientrega','Completado'),(5,1,'2024-01-20',120000.00,'Coordinadora','Pendiente'),(6,2,'2024-05-05',285000.00,'Servientrega','Completado'),(7,1,'2025-03-10',165000.00,'Coordinadora','Pendiente'),(8,2,'2025-07-13',200000.00,'Coordinadora','Completado');
/*!40000 ALTER TABLE `orden` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orden_particionada`
--

DROP TABLE IF EXISTS `orden_particionada`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orden_particionada` (
  `id_orden` int NOT NULL,
  `id_usuario` int NOT NULL,
  `fecha` date NOT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `envio` varchar(100) DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_orden`,`fecha`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
/*!50100 PARTITION BY RANGE (year(`fecha`))
(PARTITION p2023 VALUES LESS THAN (2024) ENGINE = InnoDB,
 PARTITION p2024 VALUES LESS THAN (2025) ENGINE = InnoDB,
 PARTITION p2025 VALUES LESS THAN (2026) ENGINE = InnoDB,
 PARTITION pmax VALUES LESS THAN MAXVALUE ENGINE = InnoDB) */;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orden_particionada`
--

LOCK TABLES `orden_particionada` WRITE;
/*!40000 ALTER TABLE `orden_particionada` DISABLE KEYS */;
INSERT INTO `orden_particionada` VALUES (3,1,'2023-02-15',45000.00,'Servientrega','Completado'),(4,2,'2023-06-10',85000.00,'Servientrega','Completado'),(5,1,'2024-01-20',120000.00,'Coordinadora','Pendiente'),(6,2,'2024-05-05',285000.00,'Servientrega','Completado'),(1,1,'2025-07-10',165000.00,'Servientrega','Completado'),(2,2,'2025-07-13',125000.00,'Coordinadora','Pendiente'),(7,1,'2025-03-10',165000.00,'Coordinadora','Pendiente'),(8,2,'2025-07-13',200000.00,'Coordinadora','Completado');
/*!40000 ALTER TABLE `orden_particionada` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pago`
--

DROP TABLE IF EXISTS `pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pago` (
  `id_pago` int NOT NULL AUTO_INCREMENT,
  `id_orden` int NOT NULL,
  `fecha` date DEFAULT NULL,
  `monto` decimal(10,2) DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_pago`),
  KEY `idx_pago_orden` (`id_orden`),
  CONSTRAINT `pago_ibfk_1` FOREIGN KEY (`id_orden`) REFERENCES `orden` (`id_orden`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pago`
--

LOCK TABLES `pago` WRITE;
/*!40000 ALTER TABLE `pago` DISABLE KEYS */;
INSERT INTO `pago` VALUES (1,1,'2025-07-10',165000.00,'Completado'),(2,2,'2025-07-13',130000.00,'Pendiente'),(3,3,'2023-02-15',45000.00,'Completado'),(4,4,'2023-06-10',85000.00,'Completado'),(5,5,'2024-01-20',120000.00,'Pendiente'),(6,6,'2024-05-05',285000.00,'Completado'),(7,7,'2025-03-10',165000.00,'Pendiente'),(8,8,'2025-07-13',200000.00,'Completado');
/*!40000 ALTER TABLE `pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `descripcion` text,
  `precio` decimal(10,2) DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  UNIQUE KEY `uq_producto_nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'Mouse Inalámbrico Logitech M185','Mouse óptico inalámbrico con receptor USB',45000.00,'mouse_logitech.jpg'),(2,'Teclado Mecánico Redragon K552','Teclado mecánico retroiluminado para gaming',120000.00,'teclado_redragon.jpg'),(3,'Audífonos Bluetooth JBL TUNE 510BT','Audífonos inalámbricos con micrófono integrado',165000.00,'audifonos_jbl.jpg'),(4,'Webcam Full HD Nexxt Solutions','Cámara web con resolución 1080p y micrófono',85000.00,'webcam_nexxt.jpg'),(5,'Teclado Mecánico','Teclado con switches azules',120000.00,'teclado.jpg'),(6,'Mouse Inalámbrico','Mouse ergonómico 2.4G',80000.00,'mouse.jpg'),(7,'Audífonos','Audífonos over-ear con micrófono',150000.00,'audifonos.jpg'),(8,'Soporte de celular reforzado','Soporte reforzado',29900.00,NULL);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `direccion_envio` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Laura Rodríguez','laura@correo.com','Calle 123 #45-67, Bogotá'),(2,'Carlos Pérez','carlos@correo.com','Carrera 9 #10-20, Medellín'),(3,'Andrés Gómez','andres@correo.com','Calle 10 #20-30, Bogotá'),(4,'María Torres','maria@correo.com','Carrera 50 #25-90, Cali');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `id_venta` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `cantidad` int NOT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_venta`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
INSERT INTO `venta` VALUES (1,8,3,'2025-08-15 00:35:41'),(2,8,3,'2025-08-15 00:39:03');
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-15 19:57:38
