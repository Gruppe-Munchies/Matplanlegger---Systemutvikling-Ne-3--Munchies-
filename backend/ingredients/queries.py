from local_db.session import loadSession

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup


# Queries needed for current issue
# fetch_all_ingredients
# fetch_ingredient_where
    # exact_name_equals(exact_name),
    # unit_equals(unit)=,
    # n_ingredients_equal(n_ingredients),
    # price_equals(price)
    #ingredients_where_usergroup_equals(usergroup),
    #ingredients_where_name_contains(name)
        # greater than & less than for unit, n_ingredients, price

# Queries needed for future issues
# fetch_ingredient_in_current_weekly_menu # Postponed unitil weekly menu done
# Queries for report # Will be addressed in separate issue regarding reports

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
