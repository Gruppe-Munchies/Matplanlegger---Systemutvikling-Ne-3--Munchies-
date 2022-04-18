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

def fetch_recipesNameQyantity_where_weeklymenu_id(menu_id):
    return session.query(RecipeHasWeeklyMenu.recipe_idRecipe, Recipe.name,
                         RecipeHasWeeklyMenu.expectedConsumption).join(
        RecipeHasWeeklyMenu, RecipeHasWeeklyMenu.recipe_idRecipe == Recipe.idRecipe).filter(
        RecipeHasWeeklyMenu.weeklyMenu_idWeeklyMenu == menu_id).all()

def fetch_recipes_where_weeklymenu_id(menu_id):
    return session.query(RecipeHasWeeklyMenu.recipe_idRecipe, RecipeHasWeeklyMenu.expectedConsumption).where(
        RecipeHasWeeklyMenu.weeklyMenu_idWeeklyMenu == menu_id).all()


def fetch_ingrdients_where_recipe_id(recipe_id):
    return session.query(RecipeHasIngredient.quantity, Ingredient.ingredientName, Ingredient.idingredient).join(
        RecipeHasIngredient,
        RecipeHasIngredient.ingredient_idingredient == Ingredient.idingredient).filter(
        RecipeHasIngredient.recipe_idRecipe == recipe_id).all()


# ikke en query, funksjon som bruker queries, kan sikkert flyttes til der den skal brukes
def get_all_ingredients_and_quantities_in_weeklymenu(menu_id):
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


# if __name__ == '__main__':
#     rec = get_all_ingredients_and_quantities_in_weeklymenu(27)
#     for r in rec:
#         print(r[0])
#         print(r[1])
#         print(r[2])
#         print("\n")
