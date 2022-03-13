from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
import backend.auth.queries as auth_queries

from backend.auth.forms import LoginForm, RegisterForm
from backend.auth.queries import * #fetchAllUserGroups, fetchUser, fetchUserGroup

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('index.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    formA = RegisterForm(request.form)
    user_group = fetchAllUserGroups()
    all_users = fetchAllUsers()
    if request.method == 'POST' and formA.validate():
        username = formA.username.data
        bruker = fetchUser(username)
        if bruker:
            flash("Brukernavn er allerede tatt", "danger")
            return render_template('register.html', form=formA, heading="Registrer ny bruker")
        email = formA.email.data
        firstname = formA.firstname.data
        lastname = formA.lastname.data
        password = formA.password.data #TODO Hash password
        usergroup = formA.usergroup.data
        usertype = formA.usertype.data

        #TODO ENDRING_FRA_A Usertype should be 1 (admin) as standard when usergroup is created, else 2 (normal user)

        #Insert user to database
        auth_queries.insert_to_user(username, email, firstname, lastname, password)
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
        return redirect(url_for("auth.register"))

    for fieldName, error_messages in formA.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}", "danger")

    return render_template('register.html', form=formA, ug=user_group, users=all_users)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def metode_fra_a(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
