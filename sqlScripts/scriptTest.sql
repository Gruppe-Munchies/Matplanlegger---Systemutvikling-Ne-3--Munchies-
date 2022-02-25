-- MySQL Script generated by MySQL Workbench
-- Thu Feb 24 13:38:45 2022
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema munchbase
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `munchbase` ;

-- -----------------------------------------------------
-- Schema munchbase
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `munchbase` DEFAULT CHARACTER SET utf8 ;
USE `munchbase` ;

-- -----------------------------------------------------
-- Table `munchbase`.`userType`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `munchbase`.`userType` ;

CREATE TABLE IF NOT EXISTS `munchbase`.`userType` (
  `iduserType` INT NOT NULL,
  `userTypeName` VARCHAR(45) NULL,
  PRIMARY KEY (`iduserType`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`userGroup`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `munchbase`.`userGroup` ;

CREATE TABLE IF NOT EXISTS `munchbase`.`userGroup` (
  `iduserGroup` INT NOT NULL,
  `groupName` VARCHAR(45) NULL,
  PRIMARY KEY (`iduserGroup`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `munchbase`.`user` ;

CREATE TABLE IF NOT EXISTS `munchbase`.`user` (
  `userId` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `password` VARCHAR(75) NOT NULL,
  `userType_iduserType` INT NOT NULL,
  `userGroup_iduserGroup` INT NOT NULL,
  PRIMARY KEY (`userId`),
  UNIQUE INDEX `userId_UNIQUE` (`userId` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  INDEX `fk_user_userType_idx` (`userType_iduserType` ASC) VISIBLE,
  INDEX `fk_user_userGroup1_idx` (`userGroup_iduserGroup` ASC) VISIBLE,
  CONSTRAINT `fk_user_userType`
    FOREIGN KEY (`userType_iduserType`)
    REFERENCES `munchbase`.`userType` (`iduserType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_userGroup1`
    FOREIGN KEY (`userGroup_iduserGroup`)
    REFERENCES `munchbase`.`userGroup` (`iduserGroup`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`ingredient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `munchbase`.`ingredient` ;

CREATE TABLE IF NOT EXISTS `munchbase`.`ingredient` (
  `idingredient` INT NOT NULL AUTO_INCREMENT,
  `ingredientName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idingredient`),
  UNIQUE INDEX `idingredient_UNIQUE` (`idingredient` ASC) VISIBLE,
  UNIQUE INDEX `ingredientName_UNIQUE` (`ingredientName` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`recipeAvailability`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `munchbase`.`recipeAvailability` ;

CREATE TABLE IF NOT EXISTS `munchbase`.`recipeAvailability` (
  `idrecipeAvailability` INT NOT NULL,
  `avilableFor` VARCHAR(45) NULL,
  PRIMARY KEY (`idrecipeAvailability`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`recipe`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `munchbase`.`recipe` ;

CREATE TABLE IF NOT EXISTS `munchbase`.`recipe` (
  `idRecipe` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `shortDescription` VARCHAR(100) NULL,
  `description` LONGBLOB NULL,
  `image` LONGBLOB NULL,
  `userGroup_iduserGroup` INT NOT NULL,
  `recipeAvailability_idrecipeAvailability` INT NOT NULL,
  `weeklyMenu_idweeklyMenu` INT NOT NULL,
  PRIMARY KEY (`idRecipe`),
  INDEX `fk_recipe_userGroup1_idx` (`userGroup_iduserGroup` ASC) VISIBLE,
  INDEX `fk_recipe_recipeAvailability1_idx` (`recipeAvailability_idrecipeAvailability` ASC) VISIBLE,
  CONSTRAINT `fk_recipe_userGroup1`
    FOREIGN KEY (`userGroup_iduserGroup`)
    REFERENCES `munchbase`.`userGroup` (`iduserGroup`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_recipe_recipeAvailability1`
    FOREIGN KEY (`recipeAvailability_idrecipeAvailability`)
    REFERENCES `munchbase`.`recipeAvailability` (`idrecipeAvailability`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`weeklyMenu`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `munchbase`.`weeklyMenu` ;

CREATE TABLE IF NOT EXISTS `munchbase`.`weeklyMenu` (
  `year` INT NOT NULL,
  `weekNum` INT NOT NULL,
  `day` INT NULL,
  `name` VARCHAR(45) NULL,
  `description` VARCHAR(250) NULL,
  PRIMARY KEY (`year`, `weekNum`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`userGroup_has_ingredient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `munchbase`.`userGroup_has_ingredient` ;

CREATE TABLE IF NOT EXISTS `munchbase`.`userGroup_has_ingredient` (
  `userGroup_iduserGroup` INT NOT NULL,
  `ingredient_idingredient` INT NOT NULL,
  `price` DECIMAL(6,2) NULL,
  `unit` VARCHAR(45) NULL,
  PRIMARY KEY (`userGroup_iduserGroup`, `ingredient_idingredient`),
  INDEX `fk_userGroup_has_ingredient_ingredient1_idx` (`ingredient_idingredient` ASC) VISIBLE,
  INDEX `fk_userGroup_has_ingredient_userGroup1_idx` (`userGroup_iduserGroup` ASC) VISIBLE,
  CONSTRAINT `fk_userGroup_has_ingredient_userGroup1`
    FOREIGN KEY (`userGroup_iduserGroup`)
    REFERENCES `munchbase`.`userGroup` (`iduserGroup`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_userGroup_has_ingredient_ingredient1`
    FOREIGN KEY (`ingredient_idingredient`)
    REFERENCES `munchbase`.`ingredient` (`idingredient`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`recipe_has_ingredient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `munchbase`.`recipe_has_ingredient` ;

CREATE TABLE IF NOT EXISTS `munchbase`.`recipe_has_ingredient` (
  `recipe_idRecipe` INT NOT NULL,
  `ingredient_idingredient` INT NOT NULL,
  `quantity` DECIMAL(4,2) NULL,
  PRIMARY KEY (`recipe_idRecipe`, `ingredient_idingredient`),
  INDEX `fk_recipe_has_ingredient_ingredient1_idx` (`ingredient_idingredient` ASC) VISIBLE,
  INDEX `fk_recipe_has_ingredient_recipe1_idx` (`recipe_idRecipe` ASC) VISIBLE,
  CONSTRAINT `fk_recipe_has_ingredient_recipe1`
    FOREIGN KEY (`recipe_idRecipe`)
    REFERENCES `munchbase`.`recipe` (`idRecipe`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_recipe_has_ingredient_ingredient1`
    FOREIGN KEY (`ingredient_idingredient`)
    REFERENCES `munchbase`.`ingredient` (`idingredient`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`recipe_has_weeklyMenu`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `munchbase`.`recipe_has_weeklyMenu` ;

CREATE TABLE IF NOT EXISTS `munchbase`.`recipe_has_weeklyMenu` (
  `recipe_idRecipe` INT NOT NULL,
  `weeklyMenu_year` INT NOT NULL,
  `weeklyMenu_weekNum` INT NOT NULL,
  `expectedConsumption` DECIMAL(4,2) NOT NULL,
  `actualConsumption` DECIMAL(4,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`recipe_idRecipe`, `weeklyMenu_year`, `weeklyMenu_weekNum`),
  INDEX `fk_recipe_has_weeklyMenu_weeklyMenu1_idx` (`weeklyMenu_year` ASC, `weeklyMenu_weekNum` ASC) VISIBLE,
  INDEX `fk_recipe_has_weeklyMenu_recipe1_idx` (`recipe_idRecipe` ASC) VISIBLE,
  CONSTRAINT `fk_recipe_has_weeklyMenu_recipe1`
    FOREIGN KEY (`recipe_idRecipe`)
    REFERENCES `munchbase`.`recipe` (`idRecipe`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_recipe_has_weeklyMenu_weeklyMenu1`
    FOREIGN KEY (`weeklyMenu_year` , `weeklyMenu_weekNum`)
    REFERENCES `munchbase`.`weeklyMenu` (`year` , `weekNum`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;