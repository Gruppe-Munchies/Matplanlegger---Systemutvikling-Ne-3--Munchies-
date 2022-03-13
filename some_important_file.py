from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
import backend.auth.queries as auth_queries

from backend.auth.forms import LoginForm, RegisterForm
from backend.auth.queries import *  # fetchAllUserGroups, fetchUser, fetchUserGroup

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('index.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    formB = RegisterForm(request.form)
    user_group = fetchAllUserGroups()
    all_users = fetchAllUsers()
    if request.method == 'POST' and formB.validate():
        username = formB.username.data
        bruker = fetchUser(username)
        if bruker:
            flash("Brukernavn er allerede tatt", "danger")
            return render_template('register.html', form=formB, heading="Registrer ny bruker")
        email = formB.email.data
        firstname = formB.firstname.data
        lastname = formB.lastname.data
        password = formB.password.data  # TODO Hash password
        usergroup = formB.usergroup.data
        usertype = formB.usertype.data

        # TODO Usertype should be 1 (admin) as standard when usergroup is created, else 2 (normal user)

        # Get userID from newly inserted user
        fetchedUser = fetchUser(username)
        userID = fetchedUser.userId
        # Fetch userGroupID from newly inserted usergroup
        fetchedUserGroup = fetchUserGroup(usergroup)
        userGroupId = fetchedUserGroup.iduserGroup

        # Insert userID, userGroupID and userType to "user_has_userGroup"
        auth_queries.insert_to_user_has_userGroup(int(userID), int(userGroupId), int(usertype))

        flash('Registreringen var vellykket!')
        return redirect(url_for("auth.register"))

    for fieldName, error_messages in formB.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}", "danger")

    return render_template('register.html', form=formB, ug=user_group, users=all_users)
    # Kommentar fra B


def is_safe_url(tesco):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, tesco))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
