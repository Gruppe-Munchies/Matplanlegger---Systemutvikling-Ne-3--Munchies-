from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
import backend.auth.queries as auth_queries
from sqlalchemy import Column

from backend.auth.forms import LoginForm, RegisterForm
from backend.auth.queries import * #fetchAllUserGroups, fetchUser, fetchUserGroup

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('index.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    user_group_A = fetchAllUserGroups()
    some_users = fetchAllUsers()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        bruker = fetchUser(username)
        if bruker:
            flash("Brukernavn er allerede tatt", "danger")
            return render_template('register.html', form=form, heading="Registrer ny bruker")
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        password = form.password.data #TODO Hash password
        usergroup = form.usergroup.data
        usertype = form.usertype.data

        #TODO Usertype should be 1 (admin) as standard when usergroup is created, else 2 (normal user)

        #Insert user to database
        #Insert userGroup to database
        auth_queries.insert_to_usergroup(usergroup)


        #Get userID from newly inserted user
        fetchedUser = fetchUser(username)
        userID = fetchedUser.userId
        #Fetch userGroupID from newly inserted usergroup
        fetchedUserGroup = fetchUserGroup(usergroup)
        userGroupId = fetchedUserGroup.iduserGroup

        #Insert userID, userGroupID and userType to "user_has_userGroup"
        auth_queries.insert_to_user_has_userGroup(int(userID), int(userGroupId), int(usertype))

        flash('Registreringen var vellykket!')
        # endring fra A
        return redirect(url_for("auth.register"))

    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}", "danger")

    # return render_template('register.html', form=form, ug=user_group, users=all_users)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def metode_fra_a(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
