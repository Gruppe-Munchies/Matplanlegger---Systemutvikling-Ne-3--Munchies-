from local_db.session import loadSession

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup

#Add to weeklyMenu
def insert_to_weeklymenu(year, weekNum, day, name, description, usergroup):
    session = loadSession()
    new_weeklyMenu = WeeklyMenu(year=year, weekNum=weekNum, day=day, name=name, description=description, userGroup_iduserGroup=usergroup)
    session.add(new_weeklyMenu)
    session.commit()