import flask
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, session
import backend.weekly_menu.queries as weekly
from backend.weekly_menu.forms import RegisterWeeklymenuForm

weeklyMenu = Blueprint('weeklyMenu', __name__, template_folder='templates')


@weeklyMenu.route('/ukesmeny', methods=['POST', 'GET'])
def ukesmeny():
    # hent ut i liste alle recepies i den gitte ukesmenyen.  hardkod ukesmenyen først.

    MENY_ID = 27
    recipes_weeklymenu = weekly.fetch_recipesNameQyantity_where_weeklymenu_id(MENY_ID)
    manu_name = weekly.fetch_menu_name_where_menu_id(MENY_ID)
    # prints names
    for r in recipes_weeklymenu:
        print(r[1])

    return render_template('ukesmeny.html', recipes=recipes_weeklymenu, name=manu_name)


@weeklyMenu.route('/legg_til_ukesmeny', methods=['POST', 'GET'])
def legg_til_ukesmeny():
    group_id = flask.session.get('group_to_use', 'not set')
    group_recipes = weekly.fetch_recipes_where_usergroupid(flask.session.get('group_to_use'))
    weeklyMenus = weekly.fetch_weeklymenu_recipes_where_name_usergroupid()
    activeMenu = weekly.fetch_weeklymenu_where_usergroupid(flask.session.get('group_to_use'))
    dishes = [i.name for i in weeklyMenus]


    return render_template('newWeeklyMenu.html', recipes=group_recipes, weeklyMenus=weeklyMenus, activeMenu=activeMenu, dishes=dishes)


@weeklyMenu.route('/weekly_menu/<array>/update', methods=["GET", "POST"])
def updateRecipeHasIngrediens(array: str):


    return redirect(url_for("recipes.oppskrifter"))


@weeklyMenu.route('/weekly_menu/<recipe_id>/<quantity>/add', methods=["GET", "POST"])
def addRecipeToWeeklyMenu(recipe_id: int, quantity: int):
    weekly.insert_to_recipe_has_weeklymenu(1, recipe_id, quantity)
    return redirect('/legg_til_ukesmeny')


@weeklyMenu.route('/weekly_menu/<recipe_id>/delete', methods=["GET", "POST"])
def RemoveRecipeFromWeeklyMenu(recipe_id: int):
    weekly.remove_from_RecipeHasWeeklyMenu(recipe_id)
    return redirect('/legg_til_ukesmeny')