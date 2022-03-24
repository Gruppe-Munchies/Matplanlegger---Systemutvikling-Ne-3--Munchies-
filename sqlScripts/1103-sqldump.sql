
CREATE TABLE munchbase.ingredient (
	idingredient         int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	`ingredientName`     varchar(45)  NOT NULL    ,
	CONSTRAINT `idingredient_UNIQUE` UNIQUE ( idingredient ) ,
	CONSTRAINT `ingredientName_UNIQUE` UNIQUE ( `ingredientName` )
 ) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;

CREATE TABLE munchbase.`recipeAvailability` (
	`idrecipeAvailability` int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	`avilableFor`        varchar(45)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE munchbase.`user` (
	`userId`             int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	username             varchar(45)  NOT NULL    ,
	email                varchar(100)  NOT NULL    ,
	firstname            varchar(45)  NOT NULL    ,
	lastname             varchar(45)  NOT NULL    ,
	password             varchar(128)  NOT NULL    ,
	CONSTRAINT `userId_UNIQUE` UNIQUE ( `userId` ) ,
	CONSTRAINT `username_UNIQUE` UNIQUE ( username )
 ) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;

CREATE TABLE munchbase.`userGroup` (
	`iduserGroup`        int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	`groupName`          varchar(45)  NOT NULL
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE munchbase.`userGroup_has_ingredient` (
	`userGroup_iduserGroup` int  NOT NULL    ,
	ingredient_idingredient int  NOT NULL    ,
	price                double      ,
	unit                 varchar(8)      ,
	CONSTRAINT pk_usergroup_has_ingredient PRIMARY KEY ( `userGroup_iduserGroup`, ingredient_idingredient )
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE munchbase.`userType` (
	`iduserType`         int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	`userTypeName`       varchar(45)  NOT NULL
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE munchbase.`user_has_userGroup` (
	`user_userId`        int  NOT NULL    ,
	`userGroup_iduserGroup` int  NOT NULL    ,
	`userType_iduserType` int  NOT NULL    ,
	CONSTRAINT pk_user_has_usergroup PRIMARY KEY ( `user_userId`, `userGroup_iduserGroup` )
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE munchbase.`weeklyMenu` (
	year                 int  NOT NULL  AUTO_INCREMENT  ,
	`weekNum`            int  NOT NULL    ,
	day                  int  NOT NULL    ,
	name                 varchar(45)  NOT NULL    ,
	description          varchar(250)      ,
	`userGroup_iduserGroup` int  NOT NULL    ,
	CONSTRAINT pk_weeklymenu PRIMARY KEY ( year, `weekNum` )
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE munchbase.recipe (
	`idRecipe`           int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	name                 varchar(45)  NOT NULL    ,
	`shortDescription`   varchar(100)      ,
	description          varchar(500)      ,
	image                varchar(200)      ,
	`userGroup_iduserGroup` int  NOT NULL    ,
	`recipeAvailability_idrecipeAvailability` int  NOT NULL    ,
	`weeklyMenu_idweeklyMenu` int
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE munchbase.recipe_has_ingredient (
	`recipe_idRecipe`    int  NOT NULL    ,
	ingredient_idingredient int  NOT NULL    ,
	quantity             double      ,
	CONSTRAINT pk_recipe_has_ingredient PRIMARY KEY ( `recipe_idRecipe`, ingredient_idingredient )
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE munchbase.`recipe_has_weeklyMenu` (
	`recipe_idRecipe`    int  NOT NULL    ,
	`weeklyMenu_year`    int  NOT NULL    ,
	`weeklyMenu_weekNum` int  NOT NULL    ,
	`expectedConsumption` decimal(4,2)  NOT NULL    ,
	`actualConsumption`  decimal(4,2)   DEFAULT (0.00)   ,
	CONSTRAINT pk_recipe_has_weeklymenu PRIMARY KEY ( `recipe_idRecipe`, `weeklyMenu_year`, `weeklyMenu_weekNum` )
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE INDEX `fk_userGroup_has_ingredient_ingredient1_idx` ON munchbase.`userGroup_has_ingredient` ( ingredient_idingredient );

CREATE INDEX `fk_userGroup_has_ingredient_userGroup1_idx` ON munchbase.`userGroup_has_ingredient` ( `userGroup_iduserGroup` );

CREATE INDEX `fk_user_has_userGroup_userGroup1_idx` ON munchbase.`user_has_userGroup` ( `userGroup_iduserGroup` );

CREATE INDEX `fk_user_has_userGroup_user1_idx` ON munchbase.`user_has_userGroup` ( `user_userId` );

CREATE INDEX `fk_user_has_userGroup_userType1_idx` ON munchbase.`user_has_userGroup` ( `userType_iduserType` );

CREATE INDEX `fk_weeklyMenu_userGroup1_idx` ON munchbase.`weeklyMenu` ( `userGroup_iduserGroup` );

CREATE INDEX `fk_recipe_userGroup1_idx` ON munchbase.recipe ( `userGroup_iduserGroup` );

CREATE INDEX `fk_recipe_recipeAvailability1_idx` ON munchbase.recipe ( `recipeAvailability_idrecipeAvailability` );

CREATE INDEX fk_recipe_has_ingredient_ingredient1_idx ON munchbase.recipe_has_ingredient ( ingredient_idingredient );

CREATE INDEX fk_recipe_has_ingredient_recipe1_idx ON munchbase.recipe_has_ingredient ( `recipe_idRecipe` );

CREATE INDEX `fk_recipe_has_weeklyMenu_weeklyMenu1_idx` ON munchbase.`recipe_has_weeklyMenu` ( `weeklyMenu_year`, `weeklyMenu_weekNum` );

CREATE INDEX `fk_recipe_has_weeklyMenu_recipe1_idx` ON munchbase.`recipe_has_weeklyMenu` ( `recipe_idRecipe` );

ALTER TABLE munchbase.recipe ADD CONSTRAINT `fk_recipe_recipeAvailability1` FOREIGN KEY ( `recipeAvailability_idrecipeAvailability` ) REFERENCES munchbase.`recipeAvailability`( `idrecipeAvailability` ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE munchbase.recipe ADD CONSTRAINT `fk_recipe_userGroup1` FOREIGN KEY ( `userGroup_iduserGroup` ) REFERENCES munchbase.`userGroup`( `iduserGroup` ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE munchbase.recipe_has_ingredient ADD CONSTRAINT fk_recipe_has_ingredient_ingredient1 FOREIGN KEY ( ingredient_idingredient ) REFERENCES munchbase.ingredient( idingredient ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE munchbase.recipe_has_ingredient ADD CONSTRAINT fk_recipe_has_ingredient_recipe1 FOREIGN KEY ( `recipe_idRecipe` ) REFERENCES munchbase.recipe( `idRecipe` ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE munchbase.`recipe_has_weeklyMenu` ADD CONSTRAINT `fk_recipe_has_weeklyMenu_recipe1` FOREIGN KEY ( `recipe_idRecipe` ) REFERENCES munchbase.recipe( `idRecipe` ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE munchbase.`recipe_has_weeklyMenu` ADD CONSTRAINT `fk_recipe_has_weeklyMenu_weeklyMenu1` FOREIGN KEY ( `weeklyMenu_year`, `weeklyMenu_weekNum` ) REFERENCES munchbase.`weeklyMenu`( year, `weekNum` ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE munchbase.`userGroup_has_ingredient` ADD CONSTRAINT `fk_userGroup_has_ingredient_ingredient1` FOREIGN KEY ( ingredient_idingredient ) REFERENCES munchbase.ingredient( idingredient ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE munchbase.`userGroup_has_ingredient` ADD CONSTRAINT `fk_userGroup_has_ingredient_userGroup1` FOREIGN KEY ( `userGroup_iduserGroup` ) REFERENCES munchbase.`userGroup`( `iduserGroup` ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE munchbase.`user_has_userGroup` ADD CONSTRAINT fk_user_has_usergroup_user1 FOREIGN KEY ( `user_userId` ) REFERENCES munchbase.`user`( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE munchbase.`user_has_userGroup` ADD CONSTRAINT fk_user_has_usergroup_usergroup1 FOREIGN KEY ( `userGroup_iduserGroup` ) REFERENCES munchbase.`userGroup`( `iduserGroup` ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE munchbase.`user_has_userGroup` ADD CONSTRAINT fk_user_has_usergroup_usertype1 FOREIGN KEY ( `userType_iduserType` ) REFERENCES munchbase.`userType`( `iduserType` ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE munchbase.`weeklyMenu` ADD CONSTRAINT `fk_weeklyMenu_userGroup1` FOREIGN KEY ( `userGroup_iduserGroup` ) REFERENCES munchbase.`userGroup`( `iduserGroup` ) ON DELETE NO ACTION ON UPDATE NO ACTION;

INSERT INTO munchbase.ingredient( idingredient, `ingredientName` ) VALUES ( 1, 'Agurk');
INSERT INTO munchbase.ingredient( idingredient, `ingredientName` ) VALUES ( 3, 'Egg');
INSERT INTO munchbase.ingredient( idingredient, `ingredientName` ) VALUES ( 5, 'Fløte');
INSERT INTO munchbase.ingredient( idingredient, `ingredientName` ) VALUES ( 4, 'Mel');
INSERT INTO munchbase.ingredient( idingredient, `ingredientName` ) VALUES ( 2, 'Tomat');
INSERT INTO munchbase.`recipeAvailability`( `idrecipeAvailability`, `avilableFor` ) VALUES ( 1, 'All');
INSERT INTO munchbase.`recipeAvailability`( `idrecipeAvailability`, `avilableFor` ) VALUES ( 2, 'Group');
INSERT INTO munchbase.`recipeAvailability`( `idrecipeAvailability`, `avilableFor` ) VALUES ( 3, 'User');
INSERT INTO munchbase.`user`( id, username, email, firstname, lastname, password ) VALUES ( 1, 'Bob', 'bob@burger.no', 'Bob', 'Bobsen', 'passord');
INSERT INTO munchbase.`user`( id, username, email, firstname, lastname, password ) VALUES ( 2, 'testebruker', 'test@test.no', 'Test', 'Bruker', 'hemmeligegreier');
INSERT INTO munchbase.`userGroup`( `iduserGroup`, `groupName` ) VALUES ( 1, 'MatMons');
INSERT INTO munchbase.`userGroup`( `iduserGroup`, `groupName` ) VALUES ( 2, 'Familien Hansen');
INSERT INTO munchbase.`userGroup_has_ingredient`( `userGroup_iduserGroup`, ingredient_idingredient, price, unit ) VALUES ( 1, 1, 15.0, 'stk');
INSERT INTO munchbase.`userGroup_has_ingredient`( `userGroup_iduserGroup`, ingredient_idingredient, price, unit ) VALUES ( 1, 4, 30.0, 'kg');
INSERT INTO munchbase.`userType`( `iduserType`, `userTypeName` ) VALUES ( 1, 'Admin');
INSERT INTO munchbase.`userType`( `iduserType`, `userTypeName` ) VALUES ( 2, 'Bruker');
INSERT INTO munchbase.`user_has_userGroup`( `user_userId`, `userGroup_iduserGroup`, `userType_iduserType` ) VALUES ( 1, 1, 1);
INSERT INTO munchbase.`user_has_userGroup`( `user_userId`, `userGroup_iduserGroup`, `userType_iduserType` ) VALUES ( 2, 2, 1);
INSERT INTO munchbase.`weeklyMenu`( year, `weekNum`, day, name, description, `userGroup_iduserGroup` ) VALUES ( 2022, 9, 1, 'Rulleuke', 'En uke full av ruller', 1);
INSERT INTO munchbase.recipe( `idRecipe`, name, `shortDescription`, description, image, `userGroup_iduserGroup`, `recipeAvailability_idrecipeAvailability`, `weeklyMenu_idweeklyMenu` ) VALUES ( 1, 'Vårruller', 'Digge ruller', 'Ikke så mye å skrive her', 'test', 1, 1, 1);
INSERT INTO munchbase.recipe_has_ingredient( `recipe_idRecipe`, ingredient_idingredient, quantity ) VALUES ( 1, 1, 2.0);
INSERT INTO munchbase.recipe_has_ingredient( `recipe_idRecipe`, ingredient_idingredient, quantity ) VALUES ( 1, 3, 4.0);
INSERT INTO munchbase.recipe_has_ingredient( `recipe_idRecipe`, ingredient_idingredient, quantity ) VALUES ( 1, 4, 1.0);
INSERT INTO munchbase.`recipe_has_weeklyMenu`( `recipe_idRecipe`, `weeklyMenu_year`, `weeklyMenu_weekNum`, `expectedConsumption`, `actualConsumption` ) VALUES ( 1, 2022, 9, 20, 50);
