from local_db.session import loadSession

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup


#Add ingredient
def insert_to_ingredients(name):
    session = loadSession()
    ingredient = Ingredient(ingredientName=name)
    session.add(ingredient)
    session.commit()