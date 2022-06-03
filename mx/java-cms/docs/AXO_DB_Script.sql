CREATE DATABASE  IF NOT EXISTS `axo` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `axo`;
-- MySQL dump 10.13  Distrib 5.1.40, for Win32 (ia32)
--
-- Host: localhost    Database: axo
-- ------------------------------------------------------
-- Server version	5.1.48-community

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `STORES`
--

DROP TABLE IF EXISTS `STORES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `STORES` (
  `id_store` int(11) NOT NULL AUTO_INCREMENT,
  `id_content_type` int(11) NOT NULL,
  `active` int(11) NOT NULL,
  `display_order` int(11) NOT NULL,
  `address1` varchar(100) NOT NULL,
  `address2` varchar(100) DEFAULT NULL,
  `name` varchar(45) NOT NULL,
  `mall` varchar(100) NOT NULL,
  `tels` varchar(60) NOT NULL,
  PRIMARY KEY (`id_store`),
  KEY `store_contenttype_fk` (`id_content_type`),
  CONSTRAINT `store_contenttype_fk` FOREIGN KEY (`id_content_type`) REFERENCES `CONTENT_TYPES` (`id_content_type`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `USERS`
--

DROP TABLE IF EXISTS `USERS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `USERS` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `first_name` varchar(80) NOT NULL,
  `secondary_last_name` varchar(80) DEFAULT NULL,
  `primary_last_name` varchar(150) NOT NULL,
  `email` varchar(80) NOT NULL,
  `role` varchar(10) NOT NULL,
  `active` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `id_user_UNIQUE` (`id_user`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USERS`
--

LOCK TABLES `USERS` WRITE;
/*!40000 ALTER TABLE `USERS` DISABLE KEYS */;
INSERT INTO `USERS` VALUES (0,'0','0','Alejandro','Puch','Aguilar','alexpuch@yahoo.com','ADMIN',1);
/*!40000 ALTER TABLE `USERS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PUBLICATION_PAGES`
--

DROP TABLE IF EXISTS `PUBLICATION_PAGES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PUBLICATION_PAGES` (
  `id_publication_page` int(11) NOT NULL AUTO_INCREMENT,
  `id_publication` int(11) NOT NULL,
  `image` longblob NOT NULL,
  `display_order` int(11) NOT NULL,
  `image_type` varchar(5) NOT NULL,
  PRIMARY KEY (`id_publication_page`),
  KEY `pubication_page_fk` (`id_publication`),
  CONSTRAINT `pubication_page_fk` FOREIGN KEY (`id_publication`) REFERENCES `PUBLICATIONS` (`id_publication`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `CONTENT_TYPE_LABELS`
--

DROP TABLE IF EXISTS `CONTENT_TYPE_LABELS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CONTENT_TYPE_LABELS` (
  `language` varchar(2) NOT NULL,
  `id_content_type` int(11) NOT NULL,
  `label` varchar(60) NOT NULL,
  PRIMARY KEY (`language`,`id_content_type`),
  KEY `id_content_type_label_FK1` (`id_content_type`),
  CONSTRAINT `id_content_type_label_FK1` FOREIGN KEY (`id_content_type`) REFERENCES `CONTENT_TYPES` (`id_content_type`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `CONTENT_TYPES`
--

DROP TABLE IF EXISTS `CONTENT_TYPES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CONTENT_TYPES` (
  `id_content_type` int(11) NOT NULL AUTO_INCREMENT,
  `content_type_name` varchar(50) NOT NULL,
  `active` int(11) NOT NULL,
  `id_content_type_parent` int(11) DEFAULT NULL,
  `display_order` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_content_type`),
  UNIQUE KEY `id_content_type_UNIQUE` (`id_content_type`),
  UNIQUE KEY `content_type_name_UNIQUE` (`content_type_name`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



DROP TABLE IF EXISTS `PUBLICATIONS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PUBLICATIONS` (
  `id_publication` int(11) NOT NULL AUTO_INCREMENT,
  `id_content_type` int(11) NOT NULL,
  `image` longblob NOT NULL,
  `active` int(11) NOT NULL,
  `display_order` int(11) NOT NULL,
  `image_type` varchar(5) NOT NULL,
  PRIMARY KEY (`id_publication`),
  KEY `publications_content_type_fk` (`id_content_type`),
  CONSTRAINT `publications_content_type_fk` FOREIGN KEY (`id_content_type`) REFERENCES `CONTENT_TYPES` (`id_content_type`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `ANIMATIONS`
--

DROP TABLE IF EXISTS `ANIMATIONS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ANIMATIONS` (
  `id_animation` int(11) NOT NULL AUTO_INCREMENT,
  `id_content` int(11) NOT NULL,
  `display_order` int(11) NOT NULL,
  `data` longblob NOT NULL,
  `extension` varchar(5) NOT NULL,
  PRIMARY KEY (`id_animation`),
  UNIQUE KEY `idimages_Slideshow_UNIQUE` (`id_animation`),
  KEY `images_slideshow_FK1` (`id_content`),
  CONSTRAINT `images_slideshow_FK1` FOREIGN KEY (`id_content`) REFERENCES `CONTENTS` (`id_content`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `CONTENTS`
--

DROP TABLE IF EXISTS `CONTENTS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CONTENTS` (
  `id_content` int(11) NOT NULL AUTO_INCREMENT,
  `id_content_type` int(11) NOT NULL,
  `language` varchar(2) NOT NULL,
  `animation_type` varchar(10) NOT NULL,
  `active` int(11) NOT NULL DEFAULT '0',
  `text` varchar(2000) NOT NULL,
  `image` longblob NOT NULL,
  `short_desc` varchar(255) NOT NULL,
  `page_title` varchar(50) NOT NULL,
  `meta_description` varchar(255) NOT NULL,
  `meta_keywords` varchar(500) NOT NULL,
  `text2` varchar(3000) DEFAULT NULL,
  PRIMARY KEY (`id_content`),
  UNIQUE KEY `id_content_UNIQUE` (`id_content`),
  KEY `content_FK1` (`id_content_type`),
  CONSTRAINT `content_FK1` FOREIGN KEY (`id_content_type`) REFERENCES `CONTENT_TYPES` (`id_content_type`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-01-17 19:40:47
