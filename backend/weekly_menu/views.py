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

            flash("Meny lagt til!", "success")
            return redirect(url_for("ukesmeny"))
        else:
            flash("Dere har allerede en meny med dette navnet", "warning")

    return render_template('newWeeklyMenu.html', form=form)
