from flask import Blueprint, render_template, session, request, redirect
from flask_login import current_user


from backend.auth.forms import LoginForm, UserGroupSelector
from backend.auth.queries import fetchAllUserGroupsUserHas

mainpage = Blueprint('mainpage', __name__, static_folder="static", template_folder="templates")


@mainpage.route('/')
def index():
    form = LoginForm()
    # print(f"current user: {current_user}")
    is_logged_in = False

    return render_template('index.html', form=form)

