from local_db.session import loadSession
from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup
from sqlalchemy import and_

session = loadSession()


def insert_to_weeklymenu(name, description, usergroup):
    session = loadSession()
    new_weeklyMenu = WeeklyMenu(name=name, description=description, userGroup_iduserGroup=usergroup)
    session.add(new_weeklyMenu)
    session.commit()


def fetch_recipes_where_usergroupid(usergroupId):
    return session.query(Recipe).where(Recipe.userGroup_iduserGroup == usergroupId).all()


def fetch_weeklymenu_where_name_and_usergroupid(usergroup_id, menu_name):
    return session.query(WeeklyMenu).filter(
        and_(WeeklyMenu.userGroup_iduserGroup == usergroup_id, WeeklyMenu.name == menu_name)).all()
