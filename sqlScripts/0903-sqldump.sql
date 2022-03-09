-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema munchbase
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema munchbase
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `munchbase` DEFAULT CHARACTER SET utf8 ;
USE `munchbase` ;

-- -----------------------------------------------------
-- Table `munchbase`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `munchbase`.`user` (
  `userId` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `firstname` VARCHAR(45) NOT NULL,
  `lastname` VARCHAR(45) NOT NULL,
  `password` VARCHAR(75) NOT NULL,
  PRIMARY KEY (`userId`),
  UNIQUE INDEX `userId_UNIQUE` (`userId` ASC),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`ingredient`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `munchbase`.`ingredient` (
  `idingredient` INT NOT NULL AUTO_INCREMENT,
  `ingredientName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idingredient`),
  UNIQUE INDEX `idingredient_UNIQUE` (`idingredient` ASC),
  UNIQUE INDEX `ingredientName_UNIQUE` (`ingredientName` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`userGroup`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `munchbase`.`userGroup` (
  `iduserGroup` INT NOT NULL AUTO_INCREMENT,
  `groupName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`iduserGroup`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`recipeAvailability`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `munchbase`.`recipeAvailability` (
  `idrecipeAvailability` INT NOT NULL AUTO_INCREMENT,
  `avilableFor` VARCHAR(45) NULL,
  PRIMARY KEY (`idrecipeAvailability`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`recipe`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `munchbase`.`recipe` (
  `idRecipe` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `shortDescription` VARCHAR(100) NULL,
  `description` VARCHAR(500) NULL,
  `image` VARCHAR(200) NULL,
  `userGroup_iduserGroup` INT NOT NULL,
  `recipeAvailability_idrecipeAvailability` INT NOT NULL,
  `weeklyMenu_idweeklyMenu` INT NULL,
  PRIMARY KEY (`idRecipe`),
  INDEX `fk_recipe_userGroup1_idx` (`userGroup_iduserGroup` ASC),
  INDEX `fk_recipe_recipeAvailability1_idx` (`recipeAvailability_idrecipeAvailability` ASC),
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
CREATE TABLE IF NOT EXISTS `munchbase`.`weeklyMenu` (
  `year` INT NOT NULL AUTO_INCREMENT,
  `weekNum` INT NOT NULL,
  `day` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(250) NULL,
  `userGroup_iduserGroup` INT NOT NULL,
  PRIMARY KEY (`year`, `weekNum`),
  INDEX `fk_weeklyMenu_userGroup1_idx` (`userGroup_iduserGroup` ASC),
  CONSTRAINT `fk_weeklyMenu_userGroup1`
    FOREIGN KEY (`userGroup_iduserGroup`)
    REFERENCES `munchbase`.`userGroup` (`iduserGroup`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`userType`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `munchbase`.`userType` (
  `iduserType` INT NOT NULL AUTO_INCREMENT,
  `userTypeName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`iduserType`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `munchbase`.`userGroup_has_ingredient`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `munchbase`.`userGroup_has_ingredient` (
  `userGroup_iduserGroup` INT NOT NULL,
  `ingredient_idingredient` INT NOT NULL,
  `price` DOUBLE NULL,
  `unit` VARCHAR(8) NULL,
  PRIMARY KEY (`userGroup_iduserGroup`, `ingredient_idingredient`),
  INDEX `fk_userGroup_has_ingredient_ingredient1_idx` (`ingredient_idingredient` ASC),
  INDEX `fk_userGroup_has_ingredient_userGroup1_idx` (`userGroup_iduserGroup` ASC),
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
CREATE TABLE IF NOT EXISTS `munchbase`.`recipe_has_ingredient` (
  `recipe_idRecipe` INT NOT NULL,
  `ingredient_idingredient` INT NOT NULL,
  `quantity` DOUBLE NULL,
  PRIMARY KEY (`recipe_idRecipe`, `ingredient_idingredient`),
  INDEX `fk_recipe_has_ingredient_ingredient1_idx` (`ingredient_idingredient` ASC),
  INDEX `fk_recipe_has_ingredient_recipe1_idx` (`recipe_idRecipe` ASC),
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
CREATE TABLE IF NOT EXISTS `munchbase`.`recipe_has_weeklyMenu` (
  `recipe_idRecipe` INT NOT NULL,
  `weeklyMenu_year` INT NOT NULL,
  `weeklyMenu_weekNum` INT NOT NULL,
  `expectedConsumption` DECIMAL(4,2) NOT NULL,
  `actualConsumption` DECIMAL(4,2) NULL DEFAULT 0.00,
  PRIMARY KEY (`recipe_idRecipe`, `weeklyMenu_year`, `weeklyMenu_weekNum`),
  INDEX `fk_recipe_has_weeklyMenu_weeklyMenu1_idx` (`weeklyMenu_year` ASC, `weeklyMenu_weekNum` ASC),
  INDEX `fk_recipe_has_weeklyMenu_recipe1_idx` (`recipe_idRecipe` ASC),
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


-- -----------------------------------------------------
-- Table `munchbase`.`user_has_userGroup`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `munchbase`.`user_has_userGroup` (
  `user_userId` INT NOT NULL,
  `userGroup_iduserGroup` INT NOT NULL,
  `userType_iduserType` INT NOT NULL,
  PRIMARY KEY (`user_userId`, `userGroup_iduserGroup`),
  INDEX `fk_user_has_userGroup_userGroup1_idx` (`userGroup_iduserGroup` ASC),
  INDEX `fk_user_has_userGroup_user1_idx` (`user_userId` ASC),
  INDEX `fk_user_has_userGroup_userType1_idx` (`userType_iduserType` ASC),
  CONSTRAINT `fk_user_has_userGroup_user1`
    FOREIGN KEY (`user_userId`)
    REFERENCES `munchbase`.`user` (`userId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_has_userGroup_userGroup1`
    FOREIGN KEY (`userGroup_iduserGroup`)
    REFERENCES `munchbase`.`userGroup` (`iduserGroup`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_has_userGroup_userType1`
    FOREIGN KEY (`userType_iduserType`)
    REFERENCES `munchbase`.`userType` (`iduserType`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
