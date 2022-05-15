from flask import Blueprint, render_template, session

import backend.weekly_menu.queries as weekly
from backend.auth.forms import LoginForm

mainpage = Blueprint('mainpage', __name__, static_folder="static", template_folder="templates")


@mainpage.route('/')
def index():
    form = LoginForm()
    if session.get('group_to_use') != 0 and weekly.check_first_weeklymenu_where_groupId(session.get('group_to_use')) != None:
        session['menuID'] = weekly.fetch_first_weeklymenu_where_groupId(session.get('group_to_use'))
    return render_template('index.html', form=form)

