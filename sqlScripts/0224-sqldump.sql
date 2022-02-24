-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.7.3-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for munchbase
DROP DATABASE IF EXISTS `munchbase`;
CREATE DATABASE IF NOT EXISTS `munchbase` /*!40100 DEFAULT CHARACTER SET utf8mb3 */;
USE `munchbase`;

-- Dumping structure for table munchbase.ingredient
DROP TABLE IF EXISTS `ingredient`;
CREATE TABLE IF NOT EXISTS `ingredient` (
  `idingredient` int(11) NOT NULL AUTO_INCREMENT,
  `ingredientName` varchar(45) NOT NULL,
  PRIMARY KEY (`idingredient`),
  UNIQUE KEY `idingredient_UNIQUE` (`idingredient`),
  UNIQUE KEY `ingredientName_UNIQUE` (`ingredientName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table munchbase.ingredient: ~0 rows (approximately)
DELETE FROM `ingredient`;
/*!40000 ALTER TABLE `ingredient` DISABLE KEYS */;
/*!40000 ALTER TABLE `ingredient` ENABLE KEYS */;

-- Dumping structure for table munchbase.recipe
DROP TABLE IF EXISTS `recipe`;
CREATE TABLE IF NOT EXISTS `recipe` (
  `idRecipe` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `shortDescription` varchar(100) DEFAULT NULL,
  `description` longblob DEFAULT NULL,
  `image` longblob DEFAULT NULL,
  `userGroup_iduserGroup` int(11) NOT NULL,
  `recipeAvailability_idrecipeAvailability` int(11) NOT NULL,
  `weeklyMenu_idweeklyMenu` int(11) NOT NULL,
  PRIMARY KEY (`idRecipe`),
  KEY `fk_recipe_userGroup1_idx` (`userGroup_iduserGroup`),
  KEY `fk_recipe_recipeAvailability1_idx` (`recipeAvailability_idrecipeAvailability`),
  CONSTRAINT `fk_recipe_recipeAvailability1` FOREIGN KEY (`recipeAvailability_idrecipeAvailability`) REFERENCES `recipeavailability` (`idrecipeAvailability`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_recipe_userGroup1` FOREIGN KEY (`userGroup_iduserGroup`) REFERENCES `usergroup` (`iduserGroup`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table munchbase.recipe: ~0 rows (approximately)
DELETE FROM `recipe`;
/*!40000 ALTER TABLE `recipe` DISABLE KEYS */;
/*!40000 ALTER TABLE `recipe` ENABLE KEYS */;

-- Dumping structure for table munchbase.recipeavailability
DROP TABLE IF EXISTS `recipeavailability`;
CREATE TABLE IF NOT EXISTS `recipeavailability` (
  `idrecipeAvailability` int(11) NOT NULL,
  `avilableFor` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idrecipeAvailability`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table munchbase.recipeavailability: ~0 rows (approximately)
DELETE FROM `recipeavailability`;
/*!40000 ALTER TABLE `recipeavailability` DISABLE KEYS */;
/*!40000 ALTER TABLE `recipeavailability` ENABLE KEYS */;

-- Dumping structure for table munchbase.recipe_has_ingredient
DROP TABLE IF EXISTS `recipe_has_ingredient`;
CREATE TABLE IF NOT EXISTS `recipe_has_ingredient` (
  `recipe_idRecipe` int(11) NOT NULL,
  `ingredient_idingredient` int(11) NOT NULL,
  `quantity` decimal(4,2) DEFAULT NULL,
  PRIMARY KEY (`recipe_idRecipe`,`ingredient_idingredient`),
  KEY `fk_recipe_has_ingredient_ingredient1_idx` (`ingredient_idingredient`),
  KEY `fk_recipe_has_ingredient_recipe1_idx` (`recipe_idRecipe`),
  CONSTRAINT `fk_recipe_has_ingredient_ingredient1` FOREIGN KEY (`ingredient_idingredient`) REFERENCES `ingredient` (`idingredient`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_recipe_has_ingredient_recipe1` FOREIGN KEY (`recipe_idRecipe`) REFERENCES `recipe` (`idRecipe`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table munchbase.recipe_has_ingredient: ~0 rows (approximately)
DELETE FROM `recipe_has_ingredient`;
/*!40000 ALTER TABLE `recipe_has_ingredient` DISABLE KEYS */;
/*!40000 ALTER TABLE `recipe_has_ingredient` ENABLE KEYS */;

-- Dumping structure for table munchbase.recipe_has_weeklymenu
DROP TABLE IF EXISTS `recipe_has_weeklymenu`;
CREATE TABLE IF NOT EXISTS `recipe_has_weeklymenu` (
  `recipe_idRecipe` int(11) NOT NULL,
  `weeklyMenu_year` int(11) NOT NULL,
  `weeklyMenu_weekNum` int(11) NOT NULL,
  `expectedConsumption` decimal(4,2) NOT NULL,
  `actualConsumption` decimal(4,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`recipe_idRecipe`,`weeklyMenu_year`,`weeklyMenu_weekNum`),
  KEY `fk_recipe_has_weeklyMenu_weeklyMenu1_idx` (`weeklyMenu_year`,`weeklyMenu_weekNum`),
  KEY `fk_recipe_has_weeklyMenu_recipe1_idx` (`recipe_idRecipe`),
  CONSTRAINT `fk_recipe_has_weeklyMenu_recipe1` FOREIGN KEY (`recipe_idRecipe`) REFERENCES `recipe` (`idRecipe`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_recipe_has_weeklyMenu_weeklyMenu1` FOREIGN KEY (`weeklyMenu_year`, `weeklyMenu_weekNum`) REFERENCES `weeklymenu` (`year`, `weekNum`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table munchbase.recipe_has_weeklymenu: ~0 rows (approximately)
DELETE FROM `recipe_has_weeklymenu`;
/*!40000 ALTER TABLE `recipe_has_weeklymenu` DISABLE KEYS */;
/*!40000 ALTER TABLE `recipe_has_weeklymenu` ENABLE KEYS */;

-- Dumping structure for table munchbase.user
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `userId` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `email` varchar(100) NOT NULL,
  `firstname` varchar(45) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  `password` varchar(75) NOT NULL,
  `userType_iduserType` int(11) NOT NULL,
  `userGroup_iduserGroup` int(11) NOT NULL,
  PRIMARY KEY (`userId`),
  UNIQUE KEY `userId_UNIQUE` (`userId`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  KEY `fk_user_userType_idx` (`userType_iduserType`),
  KEY `fk_user_userGroup1_idx` (`userGroup_iduserGroup`),
  CONSTRAINT `fk_user_userGroup1` FOREIGN KEY (`userGroup_iduserGroup`) REFERENCES `usergroup` (`iduserGroup`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_userType` FOREIGN KEY (`userType_iduserType`) REFERENCES `usertype` (`iduserType`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;

-- Dumping data for table munchbase.user: ~1 rows (approximately)
DELETE FROM `user`;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`userId`, `username`, `email`, `firstname`, `lastname`, `password`, `userType_iduserType`, `userGroup_iduserGroup`) VALUES
	(1, 'kingmalvin', 'malvinz@mail.com', 'Malvin', 'Khan', 'qwert', 1, 1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;

-- Dumping structure for table munchbase.usergroup
DROP TABLE IF EXISTS `usergroup`;
CREATE TABLE IF NOT EXISTS `usergroup` (
  `iduserGroup` int(11) NOT NULL,
  `groupName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`iduserGroup`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table munchbase.usergroup: ~2 rows (approximately)
DELETE FROM `usergroup`;
/*!40000 ALTER TABLE `usergroup` DISABLE KEYS */;
INSERT INTO `usergroup` (`iduserGroup`, `groupName`) VALUES
	(1, 'MatMons'),
	(2, 'Cafe Milano');
/*!40000 ALTER TABLE `usergroup` ENABLE KEYS */;

-- Dumping structure for table munchbase.usergroup_has_ingredient
DROP TABLE IF EXISTS `usergroup_has_ingredient`;
CREATE TABLE IF NOT EXISTS `usergroup_has_ingredient` (
  `userGroup_iduserGroup` int(11) NOT NULL,
  `ingredient_idingredient` int(11) NOT NULL,
  `price` decimal(6,2) DEFAULT NULL,
  `unit` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`userGroup_iduserGroup`,`ingredient_idingredient`),
  KEY `fk_userGroup_has_ingredient_ingredient1_idx` (`ingredient_idingredient`),
  KEY `fk_userGroup_has_ingredient_userGroup1_idx` (`userGroup_iduserGroup`),
  CONSTRAINT `fk_userGroup_has_ingredient_ingredient1` FOREIGN KEY (`ingredient_idingredient`) REFERENCES `ingredient` (`idingredient`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_userGroup_has_ingredient_userGroup1` FOREIGN KEY (`userGroup_iduserGroup`) REFERENCES `usergroup` (`iduserGroup`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table munchbase.usergroup_has_ingredient: ~0 rows (approximately)
DELETE FROM `usergroup_has_ingredient`;
/*!40000 ALTER TABLE `usergroup_has_ingredient` DISABLE KEYS */;
/*!40000 ALTER TABLE `usergroup_has_ingredient` ENABLE KEYS */;

-- Dumping structure for table munchbase.usertype
DROP TABLE IF EXISTS `usertype`;
CREATE TABLE IF NOT EXISTS `usertype` (
  `iduserType` int(11) NOT NULL,
  `userTypeName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`iduserType`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table munchbase.usertype: ~2 rows (approximately)
DELETE FROM `usertype`;
/*!40000 ALTER TABLE `usertype` DISABLE KEYS */;
INSERT INTO `usertype` (`iduserType`, `userTypeName`) VALUES
	(1, 'Admin'),
	(2, 'Regular');
/*!40000 ALTER TABLE `usertype` ENABLE KEYS */;

-- Dumping structure for table munchbase.weeklymenu
DROP TABLE IF EXISTS `weeklymenu`;
CREATE TABLE IF NOT EXISTS `weeklymenu` (
  `year` int(11) NOT NULL,
  `weekNum` int(11) NOT NULL,
  `day` int(11) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `description` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`year`,`weekNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Dumping data for table munchbase.weeklymenu: ~0 rows (approximately)
DELETE FROM `weeklymenu`;
/*!40000 ALTER TABLE `weeklymenu` DISABLE KEYS */;
/*!40000 ALTER TABLE `weeklymenu` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
