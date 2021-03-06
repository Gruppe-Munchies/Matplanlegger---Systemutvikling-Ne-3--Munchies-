from numpy import double

from local_db.session import loadSession
from local_db.orm import Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, \
    UsergroupHasIngredient, WeeklyMenu, WeeklyMenuDate
from sqlalchemy import and_

session = loadSession()


def insert_to_weeklymenu(name, description, usergroup):
    session = loadSession()
    new_weeklyMenu = WeeklyMenu(name=name, description=description, userGroup_iduserGroup=usergroup)
    session.add(new_weeklyMenu)
    session.commit()
    session.close()


# def insert_to_recipe_has_weeklymenu(menu_id, recipe_id, quantity):
#     session = loadSession()
#     new_weekly_menu_recipe = RecipeHasWeeklyMenu(weeklyMenu_idWeeklyMenu=menu_id, recipe_idRecipe=recipe_id,
#                                                  expectedConsumption=quantity)
#     session.add(new_weekly_menu_recipe)
#     session.commit()
#     session.close()


def insert_to_weekly_menu_date(menu_id, year, week):
    session = loadSession()
    new_week_for_weeklyMenu = WeeklyMenuDate(weeklyMenu_id=menu_id, year=year, weekNumber=week)
    session.add(new_week_for_weeklyMenu)
    session.commit()
    session.close()


def fetch_all_weeklymenu_where_groupId(group_id):
    session = loadSession()
    res = session.query(WeeklyMenu).where(WeeklyMenu.userGroup_iduserGroup == group_id).all()
    session.close()
    return


def fetch_recipes_where_usergroupid(usergroupId):
    session = loadSession()
    res = session.query(Recipe).where(Recipe.userGroup_iduserGroup == usergroupId).all()
    session.close()
    return res


def insert_to_recipe_has_weeklymenu(menu_id, recipe_id, quantity):
    session = loadSession()
    new_weekly_menu_recipe = RecipeHasWeeklyMenu(weeklyMenu_idWeeklyMenu=menu_id, recipe_idRecipe=recipe_id,
                                                 expectedConsumption=quantity)
    session.add(new_weekly_menu_recipe)
    session.commit()
    session.close()


def fetch_weeklymenu_where_name_and_usergroupid(usergroup_id, menu_name):
    session = loadSession()
    res = session.query(WeeklyMenu).filter(
        and_(WeeklyMenu.userGroup_iduserGroup == usergroup_id, WeeklyMenu.name == menu_name)).all()
    session.close()
    return res


def fetch_menu_name_where_menu_id(menu_id):
    session = loadSession()
    res = session.query(WeeklyMenu.name).where(WeeklyMenu.idWeeklyMenu == menu_id).scalar()
    session.close()
    return res


def fetch_recipesNameQyantity_where_weeklymenu_id(menu_id):
    session = loadSession()
    res = session.query(RecipeHasWeeklyMenu.recipe_idRecipe, Recipe.name,
                        RecipeHasWeeklyMenu.expectedConsumption).join(
        RecipeHasWeeklyMenu, RecipeHasWeeklyMenu.recipe_idRecipe == Recipe.idRecipe).filter(
        RecipeHasWeeklyMenu.weeklyMenu_idWeeklyMenu == menu_id).all()
    session.close()
    return res


def fetch_recipes_where_weeklymenu_id(menu_id):
    session = loadSession()
    res = session.query(RecipeHasWeeklyMenu.recipe_idRecipe, RecipeHasWeeklyMenu.expectedConsumption).where(
        RecipeHasWeeklyMenu.weeklyMenu_idWeeklyMenu == menu_id).all()
    session.close()
    return res


def fetch_ingrdients_where_recipe_id(recipe_id):
    session = loadSession()
    res = session.query(RecipeHasIngredient.quantity, Ingredient.ingredientName, Ingredient.idingredient).join(
        RecipeHasIngredient,
        RecipeHasIngredient.ingredient_idingredient == Ingredient.idingredient).filter(
        RecipeHasIngredient.recipe_idRecipe == recipe_id).all()
    session.close()
    return res


def fetch_ingrdients_with_costs_where_recipe_id(recipe_id, usergroup_id):
    session = loadSession()
    res = session.query(RecipeHasIngredient.quantity, Ingredient.ingredientName, Ingredient.idingredient,
                        UsergroupHasIngredient.price, UsergroupHasIngredient.unit,
                        UsergroupHasIngredient.quantity).join(RecipeHasIngredient,
                                                              RecipeHasIngredient.ingredient_idingredient == Ingredient.idingredient).join(
        UsergroupHasIngredient, UsergroupHasIngredient.ingredient_idingredient == Ingredient.idingredient).filter(
        RecipeHasIngredient.recipe_idRecipe == recipe_id).filter(
        UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id).all()
    session.close()
    return res


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
    session.close()
    return ingredientsList


# ikke en query, funksjon som bruker queries, kan sikkert flyttes til der den skal brukes
def get_all_ingredients_and_quantities_cost_etc_shopping_in_weeklymenu(menu_id, usergroup_id):
    recipes = fetch_recipes_where_weeklymenu_id(menu_id)
    ingredientsList = []
    for recipe in recipes:
        resQuantity = recipe[1]
        ingredients = fetch_ingrdients_with_costs_where_recipe_id(recipe[0], usergroup_id=usergroup_id)

        for ingredient in ingredients:
            exist = False
            index = -1
            quantity = 0
            for i in range(len(ingredientsList)):
                if ingredientsList[i][1] == ingredient[1]:
                    exist = True
                    index = i

            if exist:
                quantity = (ingredient[0] * resQuantity) - ingredient[5]
                if quantity > 0:
                    cost = quantity * ingredient[3]
                    ingredientsList[index][2] += round(ingredient[0] * resQuantity)
                    ingredientsList[index][4] += round(cost)
            else:
                quantity = (ingredient[0] * resQuantity) - ingredient[5]
                if quantity > 0:
                    price = ingredient[3]
                    unit = ingredient[4]
                    id = ingredient[2]
                    name = ingredient[1]
                    cost = quantity * ingredient[3]
                    ingredientsList.append([id, name, double(quantity), unit, double(cost), price])

    # index: 0-ingredientID, 1-ingredientName, 2-Quantity of ingredient in weekly menu, 3-unit, 4-totIngredientCost, 5-unit price
    return ingredientsList


def fetch_menu_id_where_name(menu_name):
    session = loadSession()
    res = session.query(WeeklyMenu.idWeeklyMenu).where(WeeklyMenu.name == menu_name).first()
    session.close()
    return res


def fetch_ingredient_quantity_where_id(ingredient_id, usergroup_id):
    session = loadSession()
    res = session.query(UsergroupHasIngredient).filter(
        and_(UsergroupHasIngredient.ingredient_idingredient == ingredient_id,
             UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id)).one()
    session.close()
    return res


def fetch_recipes_where_usergroupid(usergroupId):
    session = loadSession()
    res = session.query(Recipe).where(Recipe.userGroup_iduserGroup == usergroupId).all()
    session.close()
    return res


def fetch_weeklymenu_where_name_and_usergroupid(usergroup_id, menu_name):
    session = loadSession()
    res = session.query(WeeklyMenu).filter(
        and_(WeeklyMenu.userGroup_iduserGroup == usergroup_id, WeeklyMenu.name == menu_name)).all()
    session.close()
    return res


def fetch_weeklymenu_where_usergroupid(usergroup_id):
    session = loadSession()
    res = session.query(WeeklyMenu).filter((WeeklyMenu.userGroup_iduserGroup == usergroup_id)).all()
    session.close()
    return res


def fetch_weeklymenu_recipes_where_name_usergroupid(menuID):
    session = loadSession()
    res = session.query(Recipe.name, RecipeHasWeeklyMenu.expectedConsumption,
                        RecipeHasWeeklyMenu.recipe_idRecipe).join(RecipeHasWeeklyMenu,
                                                                  Recipe.idRecipe == RecipeHasWeeklyMenu.recipe_idRecipe).filter(
        RecipeHasWeeklyMenu.weeklyMenu_idWeeklyMenu == menuID).all()
    session.close()
    return res


def fetch_all_weeklymenu_where_groupId(group_id):
    session = loadSession()
    res = session.query(WeeklyMenu).where(WeeklyMenu.userGroup_iduserGroup == group_id).all()
    session.close()
    return res


def fetch_first_weeklymenu_where_groupId(group_id):
    session = loadSession()
    res = session.query(WeeklyMenu.idWeeklyMenu).where(WeeklyMenu.userGroup_iduserGroup == group_id).first()[0]
    session.close()
    return res


def remove_from_RecipeHasWeeklyMenu(recipeID, MenuID):
    session = loadSession()
    session.query(RecipeHasWeeklyMenu).filter(and_(RecipeHasWeeklyMenu.recipe_idRecipe == recipeID,
                                                   RecipeHasWeeklyMenu.weeklyMenu_idWeeklyMenu == MenuID)).delete(
        synchronize_session=False)
    session.commit()
    session.close()


def check_first_weeklymenu_where_groupId(group_id):
    session = loadSession()
    res = session.query(WeeklyMenu.userGroup_iduserGroup, WeeklyMenu.idWeeklyMenu).where(
        WeeklyMenu.userGroup_iduserGroup == group_id).first()
    session.close()
    return res


def editIngredientShopping(userGroup, ingredient_id, quantity):
    currentQuantity = fetch_ingredient_quantity_where_id(ingredient_id, userGroup)
    print(type(currentQuantity))
    session = loadSession()
    field = session.query(UsergroupHasIngredient).filter(
        and_(UsergroupHasIngredient.userGroup_iduserGroup == userGroup,
             UsergroupHasIngredient.ingredient_idingredient == ingredient_id)).first()
    field.quantity = double(currentQuantity.quantity) + double(quantity)
    session.commit()
    session.close()


def fetch_menus_with_dates_by_group_id(group_id):
    session = loadSession()
    res = session.query(WeeklyMenu, WeeklyMenuDate).join(WeeklyMenuDate,
                                                         WeeklyMenu.idWeeklyMenu == WeeklyMenuDate.weeklyMenu_id).filter(
        WeeklyMenu.userGroup_iduserGroup == group_id)
    session.close()
    return res
