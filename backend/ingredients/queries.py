from local_db.session import loadSession

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup

# TODO: fetch_ingredient_in_current_weekly_menu # Postponed unitil weekly menu done
# TODO: Queries for report # Will be addressed in separate issue regarding reports

# Add ingredient
def insert_to_ingredients(name):
    session = loadSession()
    ingredient = Ingredient(ingredientName=name)
    session.add(ingredient)
    session.commit()


def fetchIngredient(ingredient):
    session = loadSession()
    res = session.query(Ingredient).where(Ingredient.ingredientName == ingredient).first()
    # res = session.query(User).filter_by(username=user_name).values(text("userId"))
    return res

def fetch_all_ingredients():
    pass


def fetch_ingredients_where_exact_name_equals(name: str):
    pass


def fetch_ingredients_where_unit_equals(unit: str):
    pass


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



