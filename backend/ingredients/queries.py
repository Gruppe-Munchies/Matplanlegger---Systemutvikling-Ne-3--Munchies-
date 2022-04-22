from sqlalchemy.orm import Query
from sqlalchemy import and_

from local_db.session import loadSession

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup

# TODO: fetch_ingredient_in_current_weekly_menu # Postponed unitil menu_queries menu done
# TODO: Queries for report # Will be addressed in separate issue regarding reports

#####################################################
# OBS RETURTYPER ER AV OBJEKT QUERY                 #
# Bruk .<kolonnenavn> på retur for å få ut verdier  #
#####################################################


def insert_to_ingredients(name: str):
    session = loadSession()
    ingredient = Ingredient(ingredientName=name)
    session.add(ingredient)
    session.commit()
    session.close()

def insert_to_usergroup_has_ingredient(userGroup, ingredient, price, unit):
    session = loadSession()
    new_userGroupIngredient = UsergroupHasIngredient(userGroup_iduserGroup=userGroup,
                                                     ingredient_idingredient=ingredient, price=price, unit=unit)
    session.add(new_userGroupIngredient)
    session.commit()
    session.close()


def fetch_ingredients_from_all_user_groups_where_ingredient_name_equals(ingredient) -> Ingredient:
    session = loadSession()
    res = session.query(Ingredient).where(Ingredient.ingredientName == ingredient).first()
    session.close()
    return res

def fetch_all_ingredients_from_all_usergroups() -> list:
    session = loadSession()
    res = session.query(Ingredient).all()
    session.close()
    return res

def fetch_ingredients_from_all_usergroups_where_name_is(name):
    session = loadSession()
    res = session.query(Ingredient.idingredient).where(Ingredient.ingredientName == name).first()
    session.close()
    return res


def fetch_ingredients_where_usergroup_and_ingredientName_equals(usergroup_id, ingredient_name):
    session = loadSession()
    res = session.query(Ingredient, UsergroupHasIngredient).join(UsergroupHasIngredient, and_(
        Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
        Ingredient.ingredientName == ingredient_name,
        UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id)).scalar()
    session.close()
    return  res

def fetch_all_ingredients_where_usergroup_equals(usergroup_id):
    session = loadSession()
    res = session.query(Ingredient, UsergroupHasIngredient).join(UsergroupHasIngredient, and_(
        Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
        UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id)).all()
    session.close()
    return res

    # if __name__ == '__main__':
    #     ingredienser = fetch_all_ingredients_where_usergroup_equals(1)
    #     for ap in ingredienser:
    #         print(f"{ap[0].ingredientName} {round(ap[1].quantity, 2)} {ap[1].unit} {round(ap[1].price, 2)}")


def fetch_ingredients_where_usergroup_and_unit_equals(usergroup_id: int, unit: str):
    session = loadSession()
    res = session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.unit == unit))
    session.close()
    return res


def fetch_ingredients_in_usergroup_where_price_equals(usergroup_id, price: int):
    session = loadSession()
    res = session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.price == price))
    session.close()
    return res


def fetch_ingredients_where_price_is_greater_than(usergroup_id, price):
    session = loadSession()
    res = session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.price > price))
    session.close()
    return res


def fetch_ingredients_where_price_is_less_than(usergroup_id, price):
    session = loadSession()
    res = session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.price < price))
    session.close()
    return res


def fetch_ingredients_where_quantity_and_groupid_equals(usergroup_id, quantity: int):
    session = loadSession()
    res = session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.quantity == quantity))
    session.close()
    return res


def fetch_ingredients_where_group_id_equals_and_quantity_less_than(usergroup_id, quantity: int):
    session = loadSession()
    res = session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.quantity < quantity))
    session.close()
    return res


def fetch_ingredients_where_group_id_equals_and_quantity_greater_than(usergroup_id, quantity: int):
    session = loadSession()
    res = session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.quantity > quantity))
    session.close()
    return res


# TODO: IKKE OK  NOEN SOM KAN REGEX? :(((((
def fetch_ingredients_where_name_contains_and_group_equals(usergroup_id: int, name: str, ):
    session = loadSession()
    res = session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               Ingredient.name == "REGEX"))  # REGEX HER?
    session.close()
    return res



def fetch_all_ingredients_where_recipeID_equals(recipe_id, group):
    session = loadSession()
    res = session.query(RecipeHasIngredient.quantity, Ingredient.ingredientName, UsergroupHasIngredient.price, UsergroupHasIngredient.unit, RecipeHasIngredient.ingredient_idingredient)\
        .join(Ingredient, RecipeHasIngredient.ingredient_idingredient == Ingredient.idingredient)\
        .join(UsergroupHasIngredient, RecipeHasIngredient.ingredient_idingredient == UsergroupHasIngredient.ingredient_idingredient)\
        .filter(RecipeHasIngredient.recipe_idRecipe == recipe_id, UsergroupHasIngredient.userGroup_iduserGroup == group)\
        .all()
    session.close()
    return res



def editIngredientInRecipe(recipeID,ingredient_id,value):
    session = loadSession()
    field = session.query(RecipeHasIngredient).filter(
        and_(RecipeHasIngredient.recipe_idRecipe == recipeID, RecipeHasIngredient.ingredient_idingredient == ingredient_id)).first()
    field.quantity = value
    session.commit()
    session.close()

def editIngredient(userGroup,ingredient_id,quantity,price):
    session = loadSession()
    field = session.query(UsergroupHasIngredient).filter(
        and_(UsergroupHasIngredient.userGroup_iduserGroup == userGroup, UsergroupHasIngredient.ingredient_idingredient == ingredient_id)).first()
    field.quantity = quantity
    field.price = price
    session.commit()
    session.close()

if __name__ == '__main__':
    editIngredient(1, 1, 34, 34)