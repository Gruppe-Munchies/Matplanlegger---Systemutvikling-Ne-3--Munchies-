from local_db.session import loadSession

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup, WeeklyMenuDate
from sqlalchemy import *

# Queries needed:
    # Per week
        # Ingredients used, totalt and per dish
        # Costs, total and per dish


# Ingredients used per week
def ingredients_used_per_week_total(groupId, year, weeknum):
    session = loadSession()

    res = session.query(WeeklyMenuDate.id_weekly_menu_date, WeeklyMenu.name.label("Ukemeny"),
                        Usergroup.groupName.label("Gruppe"), RecipeHasWeeklyMenu.weeklyMenu_idWeeklyMenu,
                        func.sum(RecipeHasWeeklyMenu.expectedConsumption).label("Antall retter"), Recipe.name.label("Oppskrift"),
                        RecipeHasIngredient.recipe_idRecipe, Ingredient.ingredientName.label("Ingrediens"), UsergroupHasIngredient.unit.label("Enhet"),
                        UsergroupHasIngredient.price.label("Pris"), func.sum(RecipeHasIngredient.quantity).label("Mengde"),
                        func.sum(RecipeHasWeeklyMenu.expectedConsumption * RecipeHasIngredient.quantity).label("SumMengde"),
                        (UsergroupHasIngredient.price * func.sum(RecipeHasWeeklyMenu.expectedConsumption * RecipeHasIngredient.quantity)).label("SumBelop"),
                        func.sum('SumBelop').label("SumTotal"))\
        .join(WeeklyMenu, WeeklyMenuDate.id_weekly_menu_date == WeeklyMenu.idWeeklyMenu)\
        .join(Usergroup, WeeklyMenu.userGroup_iduserGroup == Usergroup.iduserGroup)\
        .join(RecipeHasWeeklyMenu, RecipeHasWeeklyMenu.weeklyMenu_idWeeklyMenu == WeeklyMenu.idWeeklyMenu)\
        .join(Recipe, Recipe.idRecipe == RecipeHasWeeklyMenu.recipe_idRecipe)\
        .join(RecipeHasIngredient, RecipeHasIngredient.recipe_idRecipe == Recipe.idRecipe)\
        .join(Ingredient, Ingredient.idingredient == RecipeHasIngredient.ingredient_idingredient)\
        .join(UsergroupHasIngredient, UsergroupHasIngredient.ingredient_idingredient == Ingredient.idingredient)\
        .where(WeeklyMenuDate.year == year, WeeklyMenuDate.weekNumber == weeknum, WeeklyMenu.userGroup_iduserGroup == groupId)\
        .group_by(Usergroup.iduserGroup, Ingredient.idingredient)

    session.close()
    return res


def ingredients_used_per_week_per_dish(groupId, year, weeknum):
    session = loadSession()

    res = session.query(WeeklyMenuDate.id_weekly_menu_date, WeeklyMenu.name.label("Ukemeny"), Usergroup.groupName.label("Gruppe"),
                        RecipeHasWeeklyMenu.weeklyMenu_idWeeklyMenu, RecipeHasWeeklyMenu.expectedConsumption.label("Prognose"),
                        Recipe.name.label("Oppskrift"), RecipeHasIngredient.recipe_idRecipe, Ingredient.ingredientName.label("Ingrediens"),
                        UsergroupHasIngredient.unit.label("Enhet"), RecipeHasIngredient.quantity.label("Mengde"),
                        (RecipeHasWeeklyMenu.expectedConsumption * RecipeHasIngredient.quantity).label("SumMengde"))\
        .join(WeeklyMenu, WeeklyMenuDate.id_weekly_menu_date == WeeklyMenu.idWeeklyMenu)\
        .join(Usergroup, WeeklyMenu.userGroup_iduserGroup == Usergroup.iduserGroup)\
        .join(RecipeHasWeeklyMenu, RecipeHasWeeklyMenu.weeklyMenu_idWeeklyMenu == WeeklyMenu.idWeeklyMenu)\
        .join(Recipe, Recipe.idRecipe == RecipeHasWeeklyMenu.recipe_idRecipe)\
        .join(RecipeHasIngredient, RecipeHasIngredient.recipe_idRecipe == Recipe.idRecipe)\
        .join(Ingredient, Ingredient.idingredient == RecipeHasIngredient.ingredient_idingredient) \
        .join(UsergroupHasIngredient, UsergroupHasIngredient.ingredient_idingredient == Ingredient.idingredient) \
        .where(WeeklyMenuDate.year == year, WeeklyMenuDate.weekNumber == weeknum, WeeklyMenu.userGroup_iduserGroup == groupId)

    session.close()
    return res

def fetch_weekly_menus_for_group(groupId):
    session = loadSession()

    res = session.query(WeeklyMenu, WeeklyMenuDate)\
        .join(WeeklyMenu, WeeklyMenuDate.weeklyMenu_id == WeeklyMenu.idWeeklyMenu)\
        .where(WeeklyMenu.userGroup_iduserGroup == groupId)

    session.close()
    return res