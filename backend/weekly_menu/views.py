from urllib.parse import urljoin, urlparse

import flask
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, session
from flask_login import login_required, login_user, logout_user
import backend.recipes.queries as ingr_queries
import backend.recipes.queries as recipes
from backend import recipes
from backend.auth.forms import LoginForm
from backend.auth.queries import fetchUserGroupById, fetch_first_usergroups_for_user, fetchUser
from backend.ingredients.queries import *
import re
import backend.weekly_menu.queries as weekly
from backend.weekly_menu.forms import RegisterWeeklymenuForm

weeklyMenu = Blueprint('weeklyMenu', __name__, template_folder='templates')


@weeklyMenu.route('/legg_til_ukesmeny',  methods=['POST', 'GET'])
def legg_til_ukesmeny():

    group_id = flask.session.get('group_to_use', 'not set')

    # for å kunne legge til oppskrifter til gruppa
    group_recipes = weekly.fetch_recipes_where_usergroupid(group_id)

    form = RegisterWeeklymenuForm(request.form)

    if request.method == 'POST':
        weeklymanu_name = form.weekly_name.data
        weeklymenu_desc = form.weekly_desc.data

        # TODO: Legg til oppskrifter

        # legg til navn, beskrivelse og gruppe id til database
        weekly.insert_to_weeklymenu(weeklymanu_name, weeklymenu_desc, group_id)

    return render_template('newWeeklyMenu.html', form=form)
    # return redirect(url_for("weeklyMenu.legg_til_ukesmeny"))

