from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, session
from flask_login import login_required, login_user, logout_user
import backend.recipes.queries as ingr_queries
import backend.recipes.queries as recipes
from backend import recipes
from backend.ingredients.queries import *

#from backend.recipes.forms import RegisterForm
from backend.recipes.forms import RegisterRecipeForm
from backend.recipes.queries import *

#recipes = Blueprint('recipes', __name__, template_folder='templates', url_prefix='/oppskrift')
recipes = Blueprint('recipes', __name__, template_folder='templates')

@recipes.route('/oppskrifter')
def oppskrifter():



    recipes = ingr_queries.fetch_all_recipes()

    return render_template('oppskrifter.html', recipes=recipes)


@recipes.route('/oppskrift/<recipe_id>', methods=["GET", "POST"])
def oppskrift(recipe_id: int):
    #fetch_recipe_where_recipeId_equals
    rec = fetch_recipe_where_recipeId_equals(recipe_id)

    return render_template('oppskrift.html', rec=rec)


@recipes.route('/legg-til-rett',  methods=["GET", "POST"])
def legg_til_rett():
    group_ingredients = fetch_all_ingredients_where_usergroup_equals(1)
    form = RegisterRecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        dish = form.dish.data
        short_desc = form.short_desc.data
        long_desc = form.long_desc.data
        print("hallo")
        print(dish)


    # TODO ta inn ting fra form..
    # TODO når man legger inn ingrediens, må det også komme mulighet for å legge til en til
    #TODO legge til til rett bruker.

    return render_template('legg-til-rett.html', form=form, ingredients=group_ingredients)

@recipes.route('/legg-til-rett/<navn>/<mengde>/<enhet>', methods=["GET", "POST"])
def slettOppslag(navn: str,mengde: str, enhet: str):
    print(mengde)
    print(navn)
    print(enhet)
    # TODO: Legg til i databasemetode her:
    return redirect(request.referrer)


# Spørring som fungerte i Workbench. (hente ingrediens er pr oppskrift)

#SELECT i.`ingredientName`, uhi.price, uhi.unit, uhi.quantity
#FROM munchbase.recipe r
#	INNER JOIN munchbase.recipe_has_ingredient rhi ON ( r.`idRecipe` = rhi.`recipe_idRecipe`  )
#	INNER JOIN munchbase.ingredient i ON ( rhi.ingredient_idingredient = i.idingredient  )
#	INNER JOIN munchbase.`userGroup_has_ingredient` uhi ON ( i.idingredient = uhi.ingredient_idingredient  )
#WHERE r.`idRecipe` = 1 AND
#	uhi.`userGroup_iduserGroup` = 1
#GROUP BY i.idingredient



