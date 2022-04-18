import flask
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, session
import backend.weekly_menu.queries as weekly
from backend.weekly_menu.forms import RegisterWeeklymenuForm, WeeklyMenuSelector

weeklyMenu = Blueprint('weeklyMenu', __name__, template_folder='templates')


@weeklyMenu.route('/ukesmeny', methods=['POST', 'GET'])
def ukesmeny():
    weekly_menu = weekly.fetch_all_weeklymenu_where_groupId(session['group_to_use'])

    if not session['menu_id']:
        session['menu_id'] = weekly_menu[0].idWeeklyMenu

    form = WeeklyMenuSelector(request.form)
    choice = []

    for i in weekly_menu:
        choice.append((i.idWeeklyMenu, i.name))

    form.weeklyIdName.choices = choice

    if request.method == 'POST' and form.validate():
        selectFieldGroup = form.weeklyIdName.data

        session['menu_id'] = selectFieldGroup
        return redirect(request.referrer)

    form.weeklyIdName.data = session.get('menu_id', 0)

    recipes_weeklymenu = weekly.fetch_recipesNameQyantity_where_weeklymenu_id(session['menu_id'])
    manu_name = weekly.fetch_menu_name_where_menu_id(session['menu_id'])

    return render_template('ukesmeny.html', recipes=recipes_weeklymenu, name=manu_name, id=session['menu_id'], form=form)


# @weeklyMenu.route('/ukesmeny/addTocalendar', methods=['POST', 'GET'])
# def legg_ukesmenu_til_uke():


@weeklyMenu.route('/legg_til_ukesmeny', methods=['POST', 'GET'])
def legg_til_ukesmeny():
    group_id = flask.session.get('group_to_use', 'not set')

    # This variable contains all recipes of the group ---RECIPES
    group_recipes = weekly.fetch_recipes_where_usergroupid(group_id)

    form = RegisterWeeklymenuForm(request.form)

    # TODO: Validering av form?
    if request.method == 'POST':
        weeklymanu_name = form.weekly_name.data
        weeklymenu_desc = form.weekly_desc.data

        # Do group already have menu with same name?
        if not weekly.fetch_weeklymenu_where_name_and_usergroupid(group_id, weeklymanu_name):

            weekly.insert_to_weeklymenu(weeklymanu_name, weeklymenu_desc, group_id)

            # TODO: Legg til oppskrifter ---RECIPES

            flash("Meny lagt til!")
            return redirect(url_for("ukesmeny"))
        else:
            flash("Dere har allerede en meny med dette navnet")

    return render_template('newWeeklyMenu.html', form=form)
