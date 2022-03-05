from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

import local_db.test_queries
from backend.auth.forms import LoginForm, RegisterForm

route = Blueprint('auth', __name__, url_prefix="/auth")

@route.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        if username:
            flash("Brukernavn er allerede tatt", "danger")
            return render_template('register.html', form=form)
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        password = form.password.data #TODO Hash password
        usergroup = form.usergroup.data #TODO Import usergroups from DB
        usertype = form.usertype.data #TODO Import usertypes from DB

        local_db.test_queries.insert_to_user(username, email, firstname, lastname, password, usergroup, usertype)

