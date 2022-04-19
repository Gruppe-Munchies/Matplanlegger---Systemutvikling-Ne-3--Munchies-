from local_db.session import loadSession

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup, WeeklyMenuDate
from sqlalchemy import *

# Queries needed:
    # Per week
        # Ingredients used, totalt and per dish
        # Costs, total and per dish


# Ingredients used per week
def ingredients_used_per_week_total(groupId, year, weeknum):
    session = loadSession()

    res = session.query(WeeklyMenuDate, WeeklyMenu, Usergroup, Recipe)\
        .join(WeeklyMenuDate, WeeklyMenuDate.id_weekly_menu_date == WeeklyMenu.idWeeklyMenu)\
        .where(WeeklyMenuDate.year == year, WeeklyMenuDate.weekNumber == weeknum)

    session.close()
    return res

def ingredients_user_per_week_per_dish(groupId, year, weeklyMenuId):
    session = loadSession()

