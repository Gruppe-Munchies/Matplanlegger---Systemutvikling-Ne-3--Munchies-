import flask
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, session
import backend.weekly_menu.queries as weekly
from backend.weekly_menu.forms import RegisterWeeklymenuForm, WeeklyMenuSelector

weeklyMenu = Blueprint('weeklyMenu', __name__, template_folder='templates')


@weeklyMenu.route('/ukesmeny', methods=['POST', 'GET'])
def ukesmeny():
    if weekly.check_first_weeklymenu_where_groupId(session.get('group_to_use')) != None:
    # if not flask.session.get('menuID'):
    #    session['menuID'] = weekly.fetch_first_weeklymenu_where_groupId(session.get('group_to_use'))
        group_id = flask.session.get('group_to_use', 'not set')
        weekly_menu = weekly.fetch_all_weeklymenu_where_groupId(session['group_to_use'])
        recipes_weeklymenu = weekly.fetch_recipesNameQyantity_where_weeklymenu_id(weekly_menu[0].idWeeklyMenu)

        # hent ut i liste alle recepies i den gitte ukesmenyen.  hardkod ukesmenyen først.
        group_recipes = weekly.fetch_recipes_where_usergroupid(flask.session.get('group_to_use'))

        weeklyMenus = weekly.fetch_weeklymenu_recipes_where_name_usergroupid(flask.session.get('menuID'))
        activeMenu = weekly.fetch_weeklymenu_where_usergroupid(flask.session.get('group_to_use'))
        dishes = [i.name for i in weeklyMenus]

        form = RegisterWeeklymenuForm(request.form)
        formSelector = WeeklyMenuSelector(request.form)
        choice = []

        for i in weekly_menu:
            choice.append((i.idWeeklyMenu, i.name))
        for i in choice:
            if i[0] == int(flask.session.get('menuID')):
                choice.remove(i)
                choice.insert(0, i)


        formSelector.weeklyIdName.choices = choice

        if request.method == 'POST':
            if formSelector.weeklyIdName.data != None:
                session['menuID'] = formSelector.weeklyIdName.data
                formSelector.weeklyIdName.data = session['menuID']

                return redirect(request.referrer)

            if form.weekly_name.data != None:
                weeklymanu_name = form.weekly_name.data
                weeklymenu_desc = form.weekly_desc.data

                # Do group already have menu with same name?
                if not weekly.fetch_weeklymenu_where_name_and_usergroupid(group_id, weeklymanu_name):

                    weekly.insert_to_weeklymenu(weeklymanu_name, weeklymenu_desc, group_id)

                    # TODO: Legg til oppskrifter ---RECIPES

                    flash("Meny lagt til!", "success")
                    return redirect(url_for("weeklyMenu.ukesmeny"))
                else:
                    flash("Dere har allerede en meny med dette navnet", "warning")


        weeklyMenus = weekly.fetch_weeklymenu_recipes_where_name_usergroupid(flask.session.get('menuID'))

        return render_template('ukesmeny.html', recipes=group_recipes, weeklyMenus=weeklyMenus, activeMenu=activeMenu,
                           dishes=dishes, form=form, formSelect=formSelector, menuID=flask.session.get('menuID'))
    else:
        return redirect('/legg_til_ukesmeny')

@weeklyMenu.route('/legg_til_ukesmeny', methods=['POST', 'GET'])
def legg_til_ukesmeny():
    form = RegisterWeeklymenuForm(request.form)

    if request.method == 'POST':
        weeklymanu_name = form.weekly_name.data
        weeklymenu_desc = form.weekly_desc.data

        # Do group already have menu with same name?
        if not weekly.fetch_weeklymenu_where_name_and_usergroupid(flask.session.get('group_to_use'), weeklymanu_name):

            weekly.insert_to_weeklymenu(weeklymanu_name, weeklymenu_desc, flask.session.get('group_to_use'))

            # TODO: Legg til oppskrifter ---RECIPES

            flash("Meny lagt til!", "success")
            return redirect(url_for("index"))
        else:
            flash("Dere har allerede en meny med dette navnet", "warning")

    return render_template('newWeeklyMenu.html', form=form)


@weeklyMenu.route('/weekly_menu/<array>/update', methods=["GET", "POST"])
def updateRecipeHasIngrediens(array: str):
    return redirect(url_for("recipes.oppskrifter"))


@weeklyMenu.route('/weekly_menu/<recipe_id>/<quantity>/add', methods=["GET", "POST"])
def addRecipeToWeeklyMenu(recipe_id: int, quantity: int):
    menuID = flask.session.get('menuID')
    weekly.insert_to_recipe_has_weeklymenu(menuID, recipe_id, quantity)
    return redirect('/ukesmeny')


@weeklyMenu.route('/weekly_menu/<recipe_id>/<menu_ID>/delete', methods=["GET", "POST"])
def RemoveRecipeFromWeeklyMenu(recipe_id: int,menu_ID: int):
    weekly.remove_from_RecipeHasWeeklyMenu(recipe_id, menu_ID)
    return redirect('/ukesmeny')
