from flask import render_template
from sqlalchemy import inspect

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from flask_alchemy_db_creation.local_db_create import engine


def loadSession():
    metadata = Base.metadata  # Ikke sikker på hva denne brukes til enda, men den var med i eksempelet 😎
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# Test queries
def return_email_from_name(name):
    session = loadSession()
    res = session.query(User).where(User.firstname == name).all()
    return res

#Add default usergroups
def insert_to_usergroup():
    session = loadSession()
    usergroup1 = Usergroup(groupName="Restaurant")
    usergroup2 = Usergroup(groupName="Familie")
    session.add_all([usergroup1, usergroup2])
    session.commit()

#Add default usertypes
def insert_to_usertype():
    session = loadSession()
    usertype1 = Usertype(userTypeName="Admin")
    usertype2 = Usertype(userTypeName="Bruker")
    session.add_all([usertype1, usertype2])
    session.commit()

#Add default values to recipe availability
def insert_to_recipeavalilability():
    session = loadSession()
    avail1 = RecipeAvailability(availableFor="All")
    avail2 = RecipeAvailability(availableFor="Group")
    avail3 = RecipeAvailability(availableFor="User")
    session.add_all([avail1, avail2, avail3])
    session.commit()

#Add ingredient
def insert_to_ingredients(name):
    session = loadSession()
    ingredient = Ingredient(ingredientName=name)
    session.add(ingredient)
    session.commit()

#Add user
def insert_to_user(name, email, firstname, lastname, password, usertype, usergroup):
    session = loadSession()
    new_user = User(username=name, email=email, firstname=firstname, lastname=lastname, password=password, userType_iduserType=usertype, userGroup_iduserGroup=usergroup)
    session.add(new_user)
    session.commit()

#Add recipe
def insert_to_recipe(name, shortDescription, description, image, userGroup, recipeAvailability, weeklymenu):
    session = loadSession()
    new_recipe = Recipe(name=name, shortDescription=shortDescription, description=description, image=image, userGroup_iduserGroup=userGroup, recipeAvailability_idrecipeAvailability=recipeAvailability, weeklyMenu_idweeklyMenu=weeklymenu)
    session.add(new_recipe)
    session.commit()

#Add to weeklyMenu --- NEEDS CONNECTION TO USERGROUP
def insert_to_weeklymenu(weekNum, day, name, description):
    session = loadSession()
    new_weeklyMenu = WeeklyMenu(weekNum=weekNum, day=day, name=name, description=description)
    session.add(new_weeklyMenu)
    session.commit()

#Add to recipe_has_ingredient
def insert_to_recipe_has_ingredient(recipe, ingredient, quantity):
    session = loadSession()
    new_recipeIngredient = RecipeHasIngredient(recipe_idRecipe=recipe, ingredient_idingredient=ingredient, quantity=quantity)
    session.add(new_recipeIngredient)
    session.commit()

#Add to recipe_has_weeklyMenu
def insert_to_recipe_has_weeklymenu(recipe, year, week, expectedConsumption, actualConsumption):
    session = loadSession()
    new_recipeWeeklymenu = RecipeHasWeeklyMenu(recipe_idRecipe=recipe, weeklyMenu_year=year, weeklyMenu_weekNum=week, expectedConsumption=expectedConsumption, actualConsumption=actualConsumption)
    session.add(new_recipeWeeklymenu)
    session.commit()

#Add to usergroup_has_ingredient
def insert_to_usergroup_has_ingredient(userGroup, ingredient, price, unit):
    session = loadSession()
    new_userGroupIngredient = UsergroupHasIngredient(userGroup_iduserGroup=userGroup, ingredient_idingredient=ingredient, price=price, unit=unit)
    session.add(new_userGroupIngredient)
    session.commit()