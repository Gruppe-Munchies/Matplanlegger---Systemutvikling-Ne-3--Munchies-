from sqlalchemy.orm import Query
from sqlalchemy import and_

from local_db.session import loadSession

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup

# OBS RETURTYPER ER AV OBJEKT QUERY
# Bruk .<kolonnenavn> på retur for å få ut verdier

# TODO: fetch_ingredient_in_current_weekly_menu # Postponed unitil weekly menu done
# TODO: Queries for report # Will be addressed in separate issue regarding reports

session = loadSession()


# KANSKJE OK (TESTET AV CARLOS 🐶)
def insert_to_ingredients(name: str):
    ingredient = Ingredient(ingredientName=name)
    session.add(ingredient)
    session.commit()


# OK (TESTET AV CARLOS 🐶)
def fetch_ingredients_from_all_user_groups_where_name_equals(ingredient) -> Ingredient:
    return session.query(Ingredient).where(Ingredient.ingredientName == ingredient).first()


# OK (TESTET AV CARLOS 🐶)
def fetch_all_ingredients_from_all_usergroups() -> list:
    return session.query(Ingredient).all()


# OK (TESTET AV CARLOS 🐶)
def fetch_all_ingredients_where_usergroup_equals(usergroup_id):
    return session.query(Ingredient).join(UsergroupHasIngredient, and_(
        Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
        UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id))


# OK (TESTET AV CARLOS 🐶)
def fetch_ingredients_where_usergroup_and_unit_equals(usergroup_id: int, unit: str):
    return session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.unit == unit))


# OK (TESTET AV CARLOS 🐶)
def fetch_ingredients_in_usergroup_where_price_equals(usergroup_id, price: int):
    return session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.price == price))


# OK (TESTET AV CARLOS 🐶)
def fetch_ingredients_where_price_is_greater_than(usergroup_id, price):
    return session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.price > price))


# OK (TESTET AV CARLOS 🐶)
def fetch_ingredients_where_price_is_less_than(usergroup_id, price):
    return session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               UsergroupHasIngredient.price < price))


# IKKE OK (TESTET AV CARLOS 🐶) NOEN SOM KAN REGEX? :(
def fetch_ingredients_where_name_contains_and_group_equals(usergroup_id: int, name: str, ):
    return session.query(Ingredient).join(UsergroupHasIngredient,
                                          and_(UsergroupHasIngredient.userGroup_iduserGroup == usergroup_id,
                                               Ingredient.idingredient == UsergroupHasIngredient.ingredient_idingredient,
                                               Ingredient.name == "REGEX"))  # REGEX HER?


if __name__ == '__main__':
    ape = fetch_ingredients_where_price_is_less_than(2, 200)
    print(type(ape))
    for i in ape:
        # print(type(i))
        print(i.ingredientName)

# n ingredients må legges til i databasen før spørringer etter disse kan legges inn
# def fetch_ingredients_where_n_ingredients_is_greater_than(n_ingredients):
#     pass
#
#
# def fetch_ingredients_where_n_ingredients_is_less_than(n_ingredients):
#     pass

# def fetch_ingredients_where_n_ingredients_equals(usergroup_id, n_ingredients: int):
#     pass
