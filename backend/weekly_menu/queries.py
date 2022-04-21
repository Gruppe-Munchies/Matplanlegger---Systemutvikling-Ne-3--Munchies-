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
    session.close()


def insert_to_recipe_has_weeklymenu(menu_id, recipe_id, quantity):
    session = loadSession()
    new_weekly_menu_recipe = RecipeHasWeeklyMenu(weeklyMenu_idWeeklyMenu=menu_id, recipe_idRecipe=recipe_id,
                                                 expectedConsumption=quantity)
    session.add(new_weekly_menu_recipe)
    session.commit()
    session.close()


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


def fetch_ingrdients_with_costs_where_recipe_id(recipe_id):
    session = loadSession()
    res = session.query(RecipeHasIngredient.quantity, Ingredient.ingredientName, Ingredient.idingredient,
                        UsergroupHasIngredient.price, UsergroupHasIngredient.unit,
                        UsergroupHasIngredient.quantity).join(RecipeHasIngredient,
                                                              RecipeHasIngredient.ingredient_idingredient == Ingredient.idingredient).join(
        UsergroupHasIngredient, UsergroupHasIngredient.ingredient_idingredient == Ingredient.idingredient).filter(
        RecipeHasIngredient.recipe_idRecipe == recipe_id).all()
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
    # index: 0-ingredientID, 1-ingredientName, 2-Quantity of ingredient in menu_queries menu
    session.close()
    return ingredientsList


# ikke en query, funksjon som bruker queries, kan sikkert flyttes til der den skal brukes
def get_all_ingredients_and_quantities_cost_etc_shopping_in_weeklymenu(menu_id):
    recipes = fetch_recipes_where_weeklymenu_id(menu_id)
    ingredientsList = []
    for recipe in recipes:
        resQuantity = recipe[1]
        ingredients = fetch_ingrdients_with_costs_where_recipe_id(recipe[0])

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
                cost = quantity * ingredient[3]
                ingredientsList[index][2] += ingredient[0] * resQuantity
                print(ingredientsList[index][4])
                print(cost)
                print(ingredientsList[index][4] + cost)
                ingredientsList[index][4] += cost
                print(ingredientsList[index][4])
            else:
                quantity = (ingredient[0] * resQuantity) - ingredient[5]
                # print("QUANTITY")
                # print(ingredient[0])
                # print(resQuantity)
                # print(ingredient[5])
                # print(quantity)
                price = ingredient[3]
                unit = ingredient[4]
                id = ingredient[2]
                name = ingredient[1]
                cost = quantity * ingredient[3]
                # print("COST")
                # print(ingredient[3])
                # print(cost)
                ingredientsList.append([id, name, round(quantity), unit, cost, price])

    # index: 0-ingredientID, 1-ingredientName, 2-Quantity of ingredient in menu_queries menu, 3-unit, 4-totIngredientCost, 5-unit price
    return ingredientsList


def fetch_menu_id_where_name(menu_name):
    session = loadSession()
    res = session.query(WeeklyMenu.idWeeklyMenu).where(WeeklyMenu.name == menu_name).first()
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


if __name__ == '__main__':
    rec = get_all_ingredients_and_quantities_cost_etc_shopping_in_weeklymenu(3)
    for r in rec:
        print(r[0])
        print(r[1])
        print(r[2])
        print(r[3])
        print(r[4])

    # insert_to_weekly_menu_date(2, 2022, 15)
    # rec = fetch_menu_name_where_menu_id(27)
    # print(rec)
    #     rec = get_all_ingredients_and_quantities_in_weeklymenu(27)
    #     for r in rec:
    #         print(r[0])
    #         print(r[1])
    #         print(r[2])
    #         print("\n")


def fetch_menus_with_dates_by_group_id(group_id):
    session = loadSession()
    res = session.query(WeeklyMenu).join(WeeklyMenuDate,
                                         WeeklyMenu.idWeeklyMenu == WeeklyMenuDate.weeklyMenu_id).filter(
        WeeklyMenu.userGroup_iduserGroup == group_id).all()
    session.close()
    return res


if __name__ == '__main__':
    # ape = fetch_weeklymenu_where_usergroupid(5)
    # for i in ape:
    #     print(i.idWeeklyMenu)
    ape = fetch_menus_with_dates_by_group_id(5)
    for i in ape:
        print(ape[0].name)
