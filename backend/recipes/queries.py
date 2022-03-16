from local_db.session import loadSession

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup

session = loadSession()


# Add default values to recipe availability
def insert_to_recipeavalilability():
    avail1 = RecipeAvailability(avilableFor="All")
    avail2 = RecipeAvailability(avilableFor="Group")
    avail3 = RecipeAvailability(avilableFor="User")
    session.add_all([avail1, avail2, avail3])
    session.commit()


# Add recipe
def insert_to_recipe(name, shortDescription, description, image, userGroup, recipeAvailability, weeklymenu):
    new_recipe = Recipe(name=name, shortDescription=shortDescription, description=description, image=image,
                        userGroup_iduserGroup=userGroup, recipeAvailability_idrecipeAvailability=recipeAvailability,
                        weeklyMenu_idweeklyMenu=weeklymenu)
    session.add(new_recipe)
    session.commit()


# Add to recipe_has_ingredient
def insert_to_recipe_has_ingredient(recipe, ingredient, quantity):
    new_recipeIngredient = RecipeHasIngredient(recipe_idRecipe=recipe, ingredient_idingredient=ingredient,
                                               quantity=quantity)
    session.add(new_recipeIngredient)
    session.commit()


# Add to recipe_has_weeklyMenu
def insert_to_recipe_has_weeklymenu(recipe, year, week, expectedConsumption, actualConsumption):
    new_recipeWeeklymenu = RecipeHasWeeklyMenu(recipe_idRecipe=recipe, weeklyMenu_year=year, weeklyMenu_weekNum=week,
                                               expectedConsumption=expectedConsumption,
                                               actualConsumption=actualConsumption)
    session.add(new_recipeWeeklymenu)
    session.commit()


def fetch_all_recipes():
    return session.query(Recipe).all()

