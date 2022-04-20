import flask
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, session
import backend.weekly_menu.queries as weekly
from backend.weekly_menu.forms import RegisterWeeklymenuForm, WeeklyMenuSelector

weeklyMenu = Blueprint('weeklyMenu', __name__, template_folder='templates')


@weeklyMenu.route('/ukesmeny', methods=['POST', 'GET'])
def ukesmeny():
    weekly_menu = weekly.fetch_all_weeklymenu_where_groupId(session['group_to_use'])
    MENU_ID = 1
    # if not session['menu_id']:
    #     session['menu_id'] = weekly_menu[0].idWeeklyMenu

    form = WeeklyMenuSelector(request.form)
    choice = []

    for i in weekly_menu:
        choice.append((i.idWeeklyMenu, i.name))

    form.weeklyIdName.choices = choice

    if request.method == 'POST' and form.validate():
        selectFieldGroup = form.weeklyIdName.data

        MENU_ID = selectFieldGroup
        # return redirect(url_for("ukesmeny", id=MENU_ID))

    form.weeklyIdName.data = MENU_ID

    recipes_weeklymenu = weekly.fetch_recipesNameQyantity_where_weeklymenu_id(MENU_ID)
    manu_name = weekly.fetch_menu_name_where_menu_id(MENU_ID)

    return render_template('ukesmeny.html', recipes=recipes_weeklymenu, name=manu_name, id=MENU_ID, form=form)


# @weeklyMenu.route('/ukesmeny/addTocalendar', methods=['POST', 'GET'])
# def legg_ukesmenu_til_uke():


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


@weeklyMenu.route('/handleliste', methods=["GET", "POST"])
def handleliste():
    allIngredientsFromWeekly = weekly.get_all_ingredients_and_quantities_cost_etc_shopping_in_weeklymenu(3)
    weekly_menu_name = " en konkret hardkodet ukesmeny "
    totalsum = 0
    for ingredient in allIngredientsFromWeekly:
        totalsum += ingredient[4]

    return render_template('handleliste.html',  weekly_menu_name=weekly_menu_name, totalsum=totalsum, ingredients=allIngredientsFromWeekly)