# noinspection SpellCheckingInspectionForFile @ any/"munchbase"

#################
# CREATE TABLES #
#################


CREATE TABLE munchbase.ingredient
(
    idingredient     int         NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `ingredientName` varchar(45) NOT NULL,
    CONSTRAINT `idingredient_UNIQUE` UNIQUE (idingredient),
    CONSTRAINT `ingredientName_UNIQUE` UNIQUE (`ingredientName`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 10
  DEFAULT CHARSET = utf8mb3;



CREATE TABLE munchbase.`recipeAvailability`
(
    `idrecipeAvailability` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `avilableFor`          varchar(45)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb3;



CREATE TABLE munchbase.`user`
(
    id        int          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username  varchar(45)  NOT NULL,
    email     varchar(100) NOT NULL,
    firstname varchar(45)  NOT NULL,
    lastname  varchar(45)  NOT NULL,
    password  varchar(128) NOT NULL,
    CONSTRAINT `userId_UNIQUE` UNIQUE (id),
    CONSTRAINT `username_UNIQUE` UNIQUE (username)
) ENGINE = InnoDB
  AUTO_INCREMENT = 6
  DEFAULT CHARSET = utf8mb3;



CREATE TABLE munchbase.`userGroup`
(
    `iduserGroup` int         NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `groupName`   varchar(45) NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb3;



CREATE TABLE munchbase.`userGroup_has_ingredient`
(
    `userGroup_iduserGroup` int NOT NULL,
    ingredient_idingredient int NOT NULL,
    price                   decimal(7, 2),
    unit                    varchar(8),
    quantity                decimal(7, 2) DEFAULT 0,
    CONSTRAINT pk_usergroup_has_ingredient PRIMARY KEY (`userGroup_iduserGroup`, ingredient_idingredient),
    CONSTRAINT `fk_userGroup_has_ingredient_ingredient` FOREIGN KEY (ingredient_idingredient)
        REFERENCES munchbase.ingredient (idingredient) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT `fk_userGroup_has_ingredient_userGroup` FOREIGN KEY (`userGroup_iduserGroup`)
        REFERENCES munchbase.`userGroup` (`iduserGroup`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb3;



CREATE TABLE munchbase.`userType`
(
    `iduserType`   int         NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `userTypeName` varchar(45) NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb3;



CREATE TABLE `munchbase`.`memberStatus`
(
    `idStatus`   INT         NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `statusName` VARCHAR(45) NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb3;

CREATE TABLE munchbase.`user_has_userGroup`
(
    `user_userId`           int NOT NULL,
    `userGroup_iduserGroup` int NOT NULL,
    `userType_iduserType`   int NOT NULL,
    `memberStatus_idStatus` int not null,
    CONSTRAINT pk_user_has_usergroup PRIMARY KEY (`user_userId`, `userGroup_iduserGroup`),
    CONSTRAINT fk_user_has_usergroup_user FOREIGN KEY (`user_userId`)
        REFERENCES munchbase.`user` (id) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT fk_user_has_usergroup_usergroup FOREIGN KEY (`userGroup_iduserGroup`)
        REFERENCES munchbase.`userGroup` (`iduserGroup`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT fk_user_has_usergroup_usertype FOREIGN KEY (`userType_iduserType`)
        REFERENCES munchbase.`userType` (`iduserType`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT fk_user_has_usergroup_status FOREIGN KEY (`memberStatus_idStatus`)
        REFERENCES munchbase.`memberStatus` (`idStatus`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb3;


CREATE TABLE munchbase.weeklyMenu
(
    `idWeeklyMenu`          int         NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `userGroup_iduserGroup` int         NOT NULL,
    `name`                  varchar(45) NOT NULL,
    `description`           varchar(250),
    CONSTRAINT `fk_weeklyMenu_userGroup` FOREIGN KEY (`userGroup_iduserGroup`)
        REFERENCES munchbase.`userGroup` (`iduserGroup`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb3;


CREATE TABLE munchbase.recipe
(
    `idRecipe`                                int         NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name                                      varchar(45) NOT NULL,
    `shortDescription`                        varchar(100),
    description                               varchar(500),
    image                                     varchar(200),
    `userGroup_iduserGroup`                   int         NOT NULL,
    `recipeAvailability_idrecipeAvailability` int         NOT NULL,
    `weeklyMenu_idweeklyMenu`                 int,
    CONSTRAINT `fk_recipe_recipeAvailability` FOREIGN KEY (`recipeAvailability_idrecipeAvailability`)
        REFERENCES munchbase.`recipeAvailability` (`idrecipeAvailability`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb3;


CREATE TABLE munchbase.recipe_has_ingredient
(
    `recipe_idRecipe`       int NOT NULL,
    ingredient_idingredient int NOT NULL,
    quantity                double,
    CONSTRAINT pk_recipe_has_ingredient PRIMARY KEY (`recipe_idRecipe`, ingredient_idingredient),
    CONSTRAINT fk_recipe_has_ingredient_ingredient FOREIGN KEY (ingredient_idingredient)
        REFERENCES munchbase.ingredient (idingredient) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT fk_recipe_has_ingredient_recipe FOREIGN KEY (`recipe_idRecipe`)
        REFERENCES munchbase.recipe (`idRecipe`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb3;



CREATE TABLE munchbase.recipe_has_weeklyMenu
(
    `weeklyMenu_idWeeklyMenu` int           NOT NULL,
    `recipe_idRecipe`         int           NOT NULL,
    `expectedConsumption`     decimal(4, 2) NOT NULL,
    CONSTRAINT pk_recipe_has_weeklymenu PRIMARY KEY (`recipe_idRecipe`, weeklyMenu_idWeeklyMenu),
    CONSTRAINT `fk_recipe_has_weeklyMenu_recipe` FOREIGN KEY (`recipe_idRecipe`)
        REFERENCES munchbase.recipe (`idRecipe`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT `fk_weeklymenu_has_recipe` FOREIGN KEY (`weeklyMenu_idWeeklyMenu`)
        REFERENCES munchbase.weeklyMenu (`idWeeklyMenu`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb3;

CREATE TABLE munchbase.recipeConsumption
(
    recipeConsumption_id int NOT NULL PRIMARY KEY,
    recipe_id            int NOT NULL,
    menu_date_id         int NOT NULL,
    actualConsumption    int,
    CONSTRAINT `fk_recipeId_recipeConsumption` FOREIGN KEY (`recipe_id`)
        REFERENCES munchbase.recipe (`idRecipe`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT `fk_menuDate_recipeConsumption` FOREIGN KEY (`menu_date_id`)
        REFERENCES munchbase.weekly_menu_date (`id_weekly_menu_date`) ON DELETE NO ACTION ON UPDATE NO ACTION

) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb3;

CREATE TABLE munchbase.weekly_menu_date
(
    `id_weekly_menu_date` int NOT NULL PRIMARY KEY,
    `weeklyMenu_id`       int NOT NULL,
    `year`                int NOT NULL,
    `weekNumber`          int NOT NULL,
    CONSTRAINT `fk_weeklyMenu_menuDate` FOREIGN KEY (`weeklyMenu_id`)
        REFERENCES munchbase.weeklyMenu (`idWeeklyMenu`) ON DELETE NO ACTION ON UPDATE NO ACTION

) ENGINE = InnoDB
  DEFAULT CHAR SET = utf8mb3;


##################
# CREATE INDEXES #
##################

CREATE INDEX `fk_userGroup_has_ingredient_ingredient_idx` ON munchbase.`userGroup_has_ingredient` (ingredient_idingredient);

CREATE INDEX `fk_menuDate_recipeConsumption` ON munchbase.`weekly_menu_date` (id_weekly_menu_date);

CREATE INDEX `fk_weeklyMenu_menuDate` ON munchbase.`weekly_menu_date` (weeklyMenu_id);

CREATE INDEX `fk_userGroup_has_ingredient_userGroup_idx` ON munchbase.`userGroup_has_ingredient` (`userGroup_iduserGroup`);

CREATE INDEX `fk_user_has_userGroup_userGroup_idx` ON munchbase.`user_has_userGroup` (`userGroup_iduserGroup`);

CREATE INDEX `fk_user_has_userGroup_user_idx` ON munchbase.`user_has_userGroup` (`user_userId`);

CREATE INDEX `fk_user_has_userGroup_userType_idx` ON munchbase.`user_has_userGroup` (`userType_iduserType`);

CREATE INDEX `fk_weeklyMenu_userGroup_idx` ON munchbase.`weeklyMenu` (`userGroup_iduserGroup`);

CREATE INDEX `fk_recipe_userGroup_idx` ON munchbase.recipe (`userGroup_iduserGroup`);

CREATE INDEX `fk_recipe_recipeAvailability_idx` ON munchbase.recipe (`recipeAvailability_idrecipeAvailability`);

CREATE INDEX fk_recipe_has_ingredient_ingredient_idx ON munchbase.recipe_has_ingredient (ingredient_idingredient);

CREATE INDEX fk_recipe_has_ingredient_recipe_idx ON munchbase.recipe_has_ingredient (`recipe_idRecipe`);

CREATE INDEX `fk_recipe_has_weeklyMenu_recipe_idx` ON munchbase.`recipe_has_weeklyMenu` (`recipe_idRecipe`);



###############
# INSERT DATA #
###############


# Legg til globale ingredienser
INSERT INTO munchbase.ingredient(`idingredient`, `ingredientName`)
VALUES (1, 'Agurk'),
       (2, 'Egg'),
       (3, 'Fløte'),
       (4, 'Mel'),
       (5, 'Tomat'),
       (6, 'Melk');



INSERT INTO munchbase.`recipeAvailability`(`idrecipeAvailability`, `avilableFor`)
VALUES (1, 'All'),
       (2, 'Group'),
       (3, 'User');


# Legg til bruker
INSERT INTO munchbase.`user`(id, username, email, firstname, lastname, password)
VALUES (1, 'Bob', 'bob@burger.no', 'Bob', 'Bobsen', 'passord'),
       (2, 'testebruker', 'test@test.no', 'Test', 'Bruker', 'hemmeligegreier');


# Legg til usergroups
INSERT INTO munchbase.`userGroup`(`iduserGroup`, `groupName`)
VALUES (1, 'MatMons'),
       (2, 'Familien Hansen');


# Legg til ingredienser til usergroup 1
INSERT INTO munchbase.`userGroup_has_ingredient`(`userGroup_iduserGroup`, ingredient_idingredient, price, unit,
                                                 quantity)
VALUES (1, 1, 15.0, 'stk', 10),
       (1, 2, 30.0, 'stk', 5),
       (1, 3, 30.0, 'liter', 2),
       (1, 4, 30.0, 'kg', 20),
       (1, 5, 30.0, 'stk', 2),
       (1, 6, 30.0, 'liter', 49);


# Legg til ingredienser til usergroup 2
INSERT INTO munchbase.`userGroup_has_ingredient`(`userGroup_iduserGroup`, ingredient_idingredient, price, unit,
                                                 quantity)
VALUES (2, 1, 100.0, 'stk', 2),
       (2, 2, 120.0, 'liter', 4),
       (2, 5, 150.0, 'liter', 8);


# Legg til usertype
INSERT INTO munchbase.`userType`(`iduserType`, `userTypeName`)
VALUES (1, 'Admin'),
       (2, 'Bruker');


INSERT INTO munchbase.`memberStatus`(`idStatus`, `statusName`)
VALUES (1, 'Invitert'),
       (2, 'Medlem'),
       (3, 'Avslått');


INSERT INTO munchbase.`user_has_userGroup`(`user_userId`, `userGroup_iduserGroup`, `userType_iduserType`,
                                           `memberStatus_idStatus`)
VALUES (1, 1, 1, 2),
       (2, 2, 1, 2);


# Legg til weekly menus
INSERT INTO munchbase.`weeklyMenu`(name, description, `userGroup_iduserGroup`)
VALUES ('Rulleuke', 'En uke full av ruller', 1);


# Legg til oppskrifter
INSERT INTO munchbase.recipe(`idRecipe`, name, `shortDescription`, description, image, `userGroup_iduserGroup`,
                             `recipeAvailability_idrecipeAvailability`, `weeklyMenu_idweeklyMenu`)
VALUES (1, 'Vårruller', 'Digge ruller', 'Ikke så mye å skrive her', 'test', 1, 1, 1);



INSERT INTO munchbase.recipe_has_ingredient(`recipe_idRecipe`, ingredient_idingredient, quantity)
VALUES (1, 1, 2.0),
       (1, 2, 4.0),
       (1, 3, 1.0);



INSERT INTO munchbase.`recipe_has_weeklyMenu`(`weeklyMenu_idWeeklyMenu`, `recipe_idRecipe`,
                                              `expectedConsumption`)
VALUES (0, 1, 20);
