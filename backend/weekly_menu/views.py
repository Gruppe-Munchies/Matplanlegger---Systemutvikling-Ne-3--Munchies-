import flask
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, session
import backend.weekly_menu.queries as weekly
from backend.weekly_menu.forms import RegisterWeeklymenuForm

weeklyMenu = Blueprint('weeklyMenu', __name__, template_folder='templates')


@weeklyMenu.route('/legg_til_ukesmeny',  methods=['POST', 'GET'])
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

