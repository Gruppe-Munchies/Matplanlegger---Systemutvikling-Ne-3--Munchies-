from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

import local_db.insert_to_db as db

from backend.auth.forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('index.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data #TODO Check if username is taken
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        password = form.password.data #TODO Hash password
        usergroup = form.usergroup.data #TODO Import usergroups from DB
        usertype = form.usertype.data #TODO Import usertypes from DB

        db.insert_to_user(username, email, firstname, lastname, password, usergroup, usertype)

        flash('Registreringen var vellykket!')
        return redirect(url_for("auth.login"))

    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}", "danger")

    return render_template('register.html', form=form)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc