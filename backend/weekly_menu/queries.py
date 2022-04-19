from local_db.session import loadSession
from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup, WeeklyMenuDate
from sqlalchemy import and_

session = loadSession()


def insert_to_weeklymenu(name, description, usergroup):
    session = loadSession()
    new_weeklyMenu = WeeklyMenu(name=name, description=description, userGroup_iduserGroup=usergroup)
    session.add(new_weeklyMenu)
    session.commit()

def insert_to_recipe_has_weeklymenu(menu_id, recipe_id, quantity):
    session = loadSession()
    new_weekly_menu_recipe = RecipeHasWeeklyMenu(weeklyMenu_idWeeklyMenu=menu_id, recipe_idRecipe=recipe_id,
                                                 expectedConsumption=quantity)
    session.add(new_weekly_menu_recipe)
    session.commit()


def insert_to_weekly_menu_date(menu_id, year, week):
    session = loadSession()
    new_week_for_weeklyMenu = WeeklyMenuDate(weeklyMenu_id=menu_id, year=year, weekNumber=week)
    session.add(new_week_for_weeklyMenu)
    session.commit()


def fetch_all_weeklymenu_where_groupId(group_id):
    return session.query(WeeklyMenu).where(WeeklyMenu.userGroup_iduserGroup == group_id).all()


def fetch_recipes_where_usergroupid(usergroupId):
    session = loadSession()
    return session.query(Recipe).where(Recipe.userGroup_iduserGroup == usergroupId).all()

def insert_to_recipe_has_weeklymenu(menu_id, recipe_id, quantity):
    session = loadSession()
    new_weekly_menu_recipe = RecipeHasWeeklyMenu(weeklyMenu_idWeeklyMenu=menu_id, recipe_idRecipe=recipe_id,
                                                 expectedConsumption=quantity)
    session.add(new_weekly_menu_recipe)
    session.commit()

def fetch_weeklymenu_where_name_and_usergroupid(usergroup_id, menu_name):
    session = loadSession()
    return session.query(WeeklyMenu).filter(
        and_(WeeklyMenu.userGroup_iduserGroup == usergroup_id, WeeklyMenu.name == menu_name)).all()


def fetch_menu_name_where_menu_id(menu_id):
    session = loadSession()
    return session.query(WeeklyMenu.name).where(WeeklyMenu.idWeeklyMenu == menu_id).scalar()


def fetch_recipesNameQyantity_where_weeklymenu_id(menu_id):
    session = loadSession()
    return session.query(RecipeHasWeeklyMenu.recipe_idRecipe, Recipe.name,
                         RecipeHasWeeklyMenu.expectedConsumption).join(
        RecipeHasWeeklyMenu, RecipeHasWeeklyMenu.recipe_idRecipe == Recipe.idRecipe).filter(
        RecipeHasWeeklyMenu.weeklyMenu_idWeeklyMenu == menu_id).all()


def fetch_recipes_where_weeklymenu_id(menu_id):
    session = loadSession()
    return session.query(RecipeHasWeeklyMenu.recipe_idRecipe, RecipeHasWeeklyMenu.expectedConsumption).where(
        RecipeHasWeeklyMenu.weeklyMenu_idWeeklyMenu == menu_id).all()


def fetch_ingrdients_where_recipe_id(recipe_id):
    session = loadSession()
    return session.query(RecipeHasIngredient.quantity, Ingredient.ingredientName, Ingredient.idingredient).join(
        RecipeHasIngredient,
        RecipeHasIngredient.ingredient_idingredient == Ingredient.idingredient).filter(
        RecipeHasIngredient.recipe_idRecipe == recipe_id).all()


# ikke en query, funksjon som bruker queries, kan sikkert flyttes til der den skal brukes
def get_all_ingredients_and_quantities_in_weeklymenu(menu_id):
    session = loadSession()
    recipes = fetch_recipes_where_weeklymenu_id(menu_id)
    ingredientsList = []
    for recipe in recipes:
        resQuantity = recipe[1]
        ingredients = fetch_ingrdients_where_recipe_id(recipe[0])

        for ingredient in ingredients:
            exist = False
            index = -1
            for i in range(len(ingredientsList)):
                if ingredientsList[i][1] == ingredient[1]:
                    exist = True
                    index = i

            if exist:
                ingredientsList[index][2] += ingredient[0] * resQuantity
            else:
                ingredientsList.append([ingredient[2], ingredient[1], ingredient[0] * resQuantity])
    # index: 0-ingredientID, 1-ingredientName, 2-Quantity of ingredient in weekly menu
    return ingredientsList

def fetch_menu_id_where_name(menu_name):
    session = loadSession()
    return session.query(WeeklyMenu.idWeeklyMenu).where(WeeklyMenu.name == menu_name).first()


def fetch_recipes_where_usergroupid(usergroupId):
    session = loadSession()
    return session.query(Recipe).where(Recipe.userGroup_iduserGroup == usergroupId).all()


def fetch_weeklymenu_where_name_and_usergroupid(usergroup_id, menu_name):
    session = loadSession()
    return session.query(WeeklyMenu).filter(
        and_(WeeklyMenu.userGroup_iduserGroup == usergroup_id, WeeklyMenu.name == menu_name)).all()

def fetch_weeklymenu_where_usergroupid(usergroup_id):
    session = loadSession()
    return session.query(WeeklyMenu).filter((WeeklyMenu.userGroup_iduserGroup == usergroup_id)).all()

def fetch_weeklymenu_recipes_where_name_usergroupid():
    session = loadSession()
    return session.query(Recipe.name ,RecipeHasWeeklyMenu.expectedConsumption, RecipeHasWeeklyMenu.recipe_idRecipe).join(RecipeHasWeeklyMenu, Recipe.idRecipe == RecipeHasWeeklyMenu.recipe_idRecipe).all()



def remove_from_RecipeHasWeeklyMenu(recipeID):
    session = loadSession()
    session.query(RecipeHasWeeklyMenu).filter(RecipeHasWeeklyMenu.recipe_idRecipe == recipeID).delete(synchronize_session=False)
    session.commit()

if __name__ == '__main__':
    insert_to_weekly_menu_date(2, 2022, 15)
    # rec = fetch_menu_name_where_menu_id(27)
    # print(rec)
#     rec = get_all_ingredients_and_quantities_in_weeklymenu(27)
#     for r in rec:
#         print(r[0])
#         print(r[1])
#         print(r[2])
#         print("\n")
