from local_db.session import loadSession

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup
from sqlalchemy import *

# Queries needed:
    # Per week
        # Ingredients used, totalt and per dish
        # Costs, total and per dish

    # Per month (if possible)
        # Ingredients used, total and per dish
        # Costs, total and per dish


# Ingredients used per week
def ingredients_used_per_week_total(groupId, weeknum):
    session = loadSession()

def ingredients_user_per_week_per_dish(groupId, weeknum):
    session = loadSession()

