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


def fetch_all_ingredients() -> Ingredient:
    return session.query(Ingredient).all()


def fetch_usergroup_has_ingredient_where_unit_equals(unit: str):
    return session.query(UsergroupHasIngredient).where(UsergroupHasIngredient.unit == unit).all()


def fetch_ingredient_where_id_equals(ingredient_id: int) -> Ingredient:
    return session.query(Ingredient.ingredientName).where(Ingredient.idingredient == ingredient_id).first()


def fetch_ingredient_where_unit_equals(unit) -> list:
    usergroup_rows = fetch_usergroup_has_ingredient_where_unit_equals(unit)
    ingredients = []
    for usergoup_row in usergroup_rows:
        ingredient_id: int = usergoup_row.ingredient_idingredient
        ingredient: Ingredient = fetch_ingredient_where_id_equals(ingredient_id)[0]
        ingredients.append(ingredient)
    return ingredients


# method testing
if __name__ == '__main__':
    ape = fetch_ingredient_where_unit_equals("kg")
    for ing in ape:
        print(ing)


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
