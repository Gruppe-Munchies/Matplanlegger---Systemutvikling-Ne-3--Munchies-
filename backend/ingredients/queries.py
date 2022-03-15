from local_db.session import loadSession

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup

# Queries returnerer objekter av rader
# Man må derfor kalle på kolonner når man skal hente data
# Eksempelvis:
# egg_object = fetch_ingredient_by_name("Egg")
# egg_name = egg.ingredientName
# egg_id = egg.idingredient

# TODO: fetch_ingredient_in_current_weekly_menu # Postponed unitil weekly menu done
# TODO: Queries for report # Will be addressed in separate issue regarding reports

session = loadSession()


# Add ingredient
def insert_to_ingredients(name: str):
    # name = name.lower().capitalize() #Endrer navn til stor forbokstav. Kan fikses i html med js?
    ingredient = Ingredient(ingredientName=name)
    session.add(ingredient)
    session.commit()


def fetch_ingredient_by_exact_name(ingredient) -> Ingredient:
    # res = session.query(User).filter_by(username=user_name).values(text("userId"))
    return session.query(Ingredient).where(Ingredient.ingredientName == ingredient).first()


def fetch_ingredient_ID_where_name_equals(ingredient_name):
    return session.query(Ingredient.idingredient).where(Ingredient.ingredientName == ingredient_name).first()


def fetch_all_ingredients():
    return session.query(Ingredient).all()


def fetch_ingredients_where_unit_equals(unit: str):
    idingredient_by_query = session.query(UsergroupHasIngredient.ingredient_idingredient).where(
        UsergroupHasIngredient.unit == unit)
    return session.query(Ingredient).where(Ingredient.idingredient == idingredient_by_query.label('id_ingredient'))
    # usikker på hvorfor .label må være med men får warning ellers


# method testing
if __name__ == '__main__':
    ape = fetch_ingredients_where_unit_equals("stk")
    for ing in ape:
        print(ing.ingredientName)


def fetch_ingredients_where_n_ingredients_equals(n_ingredients: int):
    pass


def fetch_ingredients_where_price_equals(price: int):
    pass


def fetch_ingredients_where_usergroup_equals(usergroup):
    pass


def fetch_ingredients_where_name_contains(name):
    pass


def fetch_ingredients_where_n_ingredients_is_greater_than(n_ingredients):
    pass


def fetch_ingredients_where_n_ingredients_is_less_than(n_ingredients):
    pass


def fetch_ingredients_where_price_is_greater_than(n_ingredients):
    pass


def fetch_ingredients_where_price_is_less_than(n_ingredients):
    pass
