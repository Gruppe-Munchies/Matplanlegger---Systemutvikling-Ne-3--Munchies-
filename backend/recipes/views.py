import re
import flask
from flask import Blueprint, flash, redirect, render_template, request, url_for

import backend.recipes.queries as ingr_queries
from backend.ingredients.queries import *
from backend.recipes.forms import RegisterRecipeForm
from backend.recipes.queries import *

recipes = Blueprint('recipes', __name__, template_folder='templates')


@recipes.route('/oppskrifter')
def oppskrifter():
    recipes = fetch_all_recipes_to_group(flask.session.get('group_to_use'))

    return render_template('oppskrifter.html', recipes=recipes)


@recipes.route('/oppskrift/<recipe_id>', methods=["GET", "POST"])
def oppskrift(recipe_id: int):
    rec = fetch_recipe_where_recipeId_equals(recipe_id)
    group = flask.session.get('group_to_use')
    group_ingredients = fetch_all_ingredients_where_usergroup_equals(group)

    ingredients = fetch_all_ingredients_where_recipeID_equals(recipe_id, group)
    ingredientInRecipe = []
    ingredientsInStock = []

    for item in ingredients:
        ingredientInRecipe.append(item.ingredientName)

    for item in group_ingredients:
        if item[0].ingredientName not in ingredientInRecipe:
            ingredientsInStock.append(item)
    return render_template('oppskrift.html', rec=rec, ingredients=ingredients, id=recipe_id,
                           ingredientsInStock=ingredientsInStock)


@recipes.route('/oppskrift/<recipe_id>/<ingrediens_id>/delete', methods=["GET", "POST"])
def removeFromRecipeHasIngrediens(recipe_id: int, ingrediens_id: int):
    remove_from_recipe_has_ingredient(recipe_id, ingrediens_id)

    return redirect('/oppskrift/' + str(recipe_id))


@recipes.route('/oppskrift/<recipe_id>/<ingrediens_id>/<value>/update', methods=["GET", "POST"])
def updateRecipeHasIngrediens(recipe_id: int, ingrediens_id: int, value: int):
    editIngredientInRecipe(recipe_id, ingrediens_id, value)

    return redirect('/oppskrift/' + str(recipe_id))


@recipes.route('/oppskrift/<recipe_id>/<ingrediens_id>/<quantity>/add', methods=["GET", "POST"])
def addIngredientToRecipe(recipe_id: int, ingrediens_id: int, quantity: int):
    ingr_queries.insert_to_recipe_has_ingredient(recipe_id, ingrediens_id, quantity)

    return redirect('/oppskrift/' + str(recipe_id))


@recipes.route('/legg-til-rett', methods=["GET", "POST"])
def legg_til_rett():
    group_id = flask.session.get('group_to_use')
    group_ingredients = fetch_all_ingredients_where_usergroup_equals(group_id)
    form = RegisterRecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        # dishId = form.dish.data
        dish = form.dish.data
        short_desc = form.short_desc.data
        long_desc = form.long_desc.data
        ingredienser = form.ingredienser.data

        # Legger til recipe i tabellen

        if fetch_recipeID_where_name_and_groupID_equals(dish, group_id) is None:
            ingr_queries.insert_to_recipe(dish, short_desc, long_desc, 'IMAGE OF DISH', group_id)

            # Henter info fra hidden field, og gjør mening ut av denne(For å få en dynamisk field)
            lst = re.sub("-.*?-", ":o:", ingredienser)

            lst = lst.split(":o:")

            ingrediensLst = []
            for i in lst:
                if i != '':
                    item = i.split(",")
                    if item[1] != '':
                        ingrediensLst.append(item)

            # Kobler ingrediens opp mot recipe
            recipeID = fetch_recipeID_where_name_equals(dish)
            for k in ingrediensLst:
                ingredId = fetch_ingredients_from_all_usergroups_where_name_is(k[0])
                ingr_queries.insert_to_recipe_has_ingredient(str(recipeID[0]), str(ingredId[0]), str(k[1]))

            return redirect(url_for("recipes.oppskrifter"))


        else:
            flash("Retten er allerede registrert", "warning")

    return render_template('legg-til-rett.html', form=form, ingredients=group_ingredients)
