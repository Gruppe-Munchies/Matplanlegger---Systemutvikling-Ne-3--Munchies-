from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, session
from flask_login import login_required, login_user, logout_user
import backend.recipes.queries as ingr_queries
import backend.recipes.queries as recipes
from backend import recipes
import flask
from backend.ingredients.queries import *
import re

#from backend.recipes.forms import RegisterForm
from backend.recipes.forms import RegisterRecipeForm, EditIngredientInDish
from backend.recipes.queries import *

#recipes = Blueprint('recipes', __name__, template_folder='templates', url_prefix='/oppskrift')
recipes = Blueprint('recipes', __name__, template_folder='templates')

@recipes.route('/oppskrifter')
def oppskrifter():

    recipes = fetch_all_recipes_to_group(flask.session.get('group_to_use'))

    return render_template('oppskrifter.html', recipes=recipes)


@recipes.route('/oppskrift/<recipe_id>', methods=["GET", "POST"])
def oppskrift(recipe_id: int):
    #fetch_recipe_where_recipeId_equals
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
    return render_template('oppskrift.html', rec=rec, ingredients=ingredients, id=recipe_id, ingredientsInStock=ingredientsInStock)


@recipes.route('/oppskrift/<recipe_id>/<ingrediens_id>/delete', methods=["GET", "POST"])
def removeFromRecipeHasIngrediens(recipe_id: int, ingrediens_id: int):
    #fetch_recipe_where_recipeId_equals
    remove_from_recipe_has_ingredient(recipe_id, ingrediens_id)

    return redirect('/oppskrift/'+ str(recipe_id))


@recipes.route('/oppskrift/<recipe_id>/<ingrediens_id>/<value>/update', methods=["GET", "POST"])
def updateRecipeHasIngrediens(recipe_id: int, ingrediens_id: int,value: int):
    editIngredientInRecipe(recipe_id, ingrediens_id, value)

    return redirect('/oppskrift/'+ str(recipe_id))


@recipes.route('/oppskrift/<recipe_id>/<ingrediens_id>/<quantity>/add', methods=["GET", "POST"])
def addIngredientToRecipe(recipe_id: int, ingrediens_id: int,quantity: int):
    ingr_queries.insert_to_recipe_has_ingredient(recipe_id, ingrediens_id, quantity)

    return redirect('/oppskrift/'+ str(recipe_id))

@recipes.route('/legg-til-rett',  methods=["GET", "POST"])
def legg_til_rett():
    group_id = flask.session.get('group_to_use')
    group_ingredients = fetch_all_ingredients_where_usergroup_equals(group_id)
    # for i in group_ingredients:
    #     print(i[0].ingredientName, i[0].idingredient )
    #     print(i)
    #     print(i[1].userGroup_iduserGroup, i[1].unit)
    form = RegisterRecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        #dishId = form.dish.data
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
            # print(recipeID[0])
            for k in ingrediensLst:
                ingredId = fetch_ingredients_from_all_usergroups_where_name_is(k[0])
                ingr_queries.insert_to_recipe_has_ingredient(str(recipeID[0]), str(ingredId[0]), str(k[1]))

            return redirect(url_for("recipes.oppskrifter"))


        else:
            flash("Retten er allerede registrert", "warning")





    # TODO ta inn ting fra form..
    # TODO når man legger inn ingrediens, må det også komme mulighet for å legge til en til
    #TODO legge til til rett bruker.

    return render_template('legg-til-rett.html', form=form, ingredients=group_ingredients)



# Spørring som fungerte i Workbench. (hente ingrediens er pr oppskrift)

#SELECT i.`ingredientName`, uhi.price, uhi.unit, uhi.quantity
#FROM munchbase.recipe r
#	INNER JOIN munchbase.recipe_has_ingredient rhi ON ( r.`idRecipe` = rhi.`recipe_idRecipe`  )
#	INNER JOIN munchbase.ingredient i ON ( rhi.ingredient_idingredient = i.idingredient  )
#	INNER JOIN munchbase.`userGroup_has_ingredient` uhi ON ( i.idingredient = uhi.ingredient_idingredient  )
#WHERE r.`idRecipe` = 1 AND
#	uhi.`userGroup_iduserGroup` = 1
#GROUP BY i.idingredient



