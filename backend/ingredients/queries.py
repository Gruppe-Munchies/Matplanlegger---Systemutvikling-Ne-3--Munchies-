from sqlalchemy.orm import Query
from sqlalchemy import and_

from local_db.session import loadSession

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup

# TODO: fetch_ingredient_in_current_weekly_menu # Postponed unitil weekly menu done
# TODO: Queries for report # Will be addressed in separate issue regarding reports

#####################################################
# OBS RETURTYPER ER AV OBJEKT QUERY                 #
# Bruk .<kolonnenavn> på retur for å få ut verdier  #
#####################################################

session = loadSession()


def insert_to_ingredients(name: str):
    ingredient = Ingredient(ingredientName=name)
    session.add(ingredient)
    session.commit()


def fetch_ingredients_from_all_user_groups_where_ingredient_name_equals(ingredient) -> Ingredient:
    return session.query(Ingredient).where(Ingredient.ingredientName == ingredient).first()


def fetch_all_ingredients_from_all_usergroups() -> list:
    return session.query(Ingredient).all()


def fetch_ingredients_where_usergroup_and_ingredientName_equals(usergroup_id, ingredient_name):
    return session.query(Ingredient, UsergroupHasIngredient).join(UsergroupHasIngredient, and_(
        Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
        Ingredient.ingredientName == ingredient_name,
        UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id)).scalar()

def fetch_all_ingredients_where_usergroup_equals(usergroup_id):
    return session.query(Ingredient, UsergroupHasIngredient).join(UsergroupHasIngredient, and_(
        Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
        UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id)).all()

    # if __name__ == '__main__':
    #     ingredienser = fetch_all_ingredients_where_usergroup_equals(1)
    #     for ap in ingredienser:
    #         print(f"{ap[0].ingredientName} {round(ap[1].quantity, 2)} {ap[1].unit} {round(ap[1].price, 2)}")


def fetch_ingredients_where_usergroup_and_unit_equals(usergroup_id: int, unit: str):
    return session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.unit == unit))


def fetch_ingredients_in_usergroup_where_price_equals(usergroup_id, price: int):
    return session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.price == price))


def fetch_ingredients_where_price_is_greater_than(usergroup_id, price):
    return session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.price > price))


def fetch_ingredients_where_price_is_less_than(usergroup_id, price):
    return session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.price < price))


def fetch_ingredients_where_quantity_and_groupid_equals(usergroup_id, quantity: int):
    return session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.quantity == quantity))


def fetch_ingredients_where_group_id_equals_and_quantity_less_than(usergroup_id, quantity: int):
    return session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.quantity < quantity))


def fetch_ingredients_where_group_id_equals_and_quantity_greater_than(usergroup_id, quantity: int):
    return session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.quantity > quantity))


# TODO: IKKE OK  NOEN SOM KAN REGEX? :(((((
def fetch_ingredients_where_name_contains_and_group_equals(usergroup_id: int, name: str, ):
    return session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               Ingredient.name == "REGEX"))  # REGEX HER?
