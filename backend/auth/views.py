from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
import backend.auth.queries as auth_queries

from backend.auth.forms import LoginForm, RegisterForm, InviteForm
from backend.auth.queries import * #fetchAllUserGroups, fetchUser, fetchUserGroup

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('index.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    user_group = fetchAllUserGroups()
    all_users = fetchAllUsers()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        bruker = fetchUser(username)
        if bruker:
            flash("Brukernavn er allerede tatt", "danger")
            return render_template('register.html', form=form, heading="Registrer ny bruker")
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        password = form.password.data
        usergroup = form.usergroup.data
        #Check if creating usergroup. If not, set group to "ingen" and usertype to 2 (not admin)
        if (usergroup == ""):
            usertype = 2
            usergroup = "ingen"
        else:
            usertype = 1

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

    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}", "danger")

    return render_template('register.html', form=form, ug=user_group, users=all_users)

#INVITE USER TO USERGROUP
@auth.route('/invite', methods=['GET', 'POST'])
def invite():
    form = InviteForm(request.form)
    users_in_group = fetchAllUsers()  # Fetch users in group

    if request.method == 'POST' and form.validate():
        user_to_invite = fetchUser(form.username.data)  # Fetch user to invite
        usergroup = fetchUserGroup(form.usergroup.data)  # Fetch usergroup
        usertype = fetchUserType(form.usertype.data)  # Fetch usertype

        #Check if user exists
        if not user_to_invite:
            print("Brukeren finnes ikke")
            flash("Brukeren finnes ikke.", "danger")
            return render_template('usergroup-administration.html', form=form, usergroup=users_in_group, heading="Inviter bruker")

        #User exists, add to group
        #TODO: Adds withouth asking user. Should be an invite.

        userId = user_to_invite.userId
        userGroupId = usergroup.iduserGroup
        usertypeId = usertype.iduserType

        print(userId)
        print(userGroupId)
        print(usertypeId)

        auth_queries.insert_to_user_has_userGroup(int(userId), int(userGroupId), int(usertypeId))

        flash('Brukeren ble lagt til!')
        return redirect(url_for("auth.invite"))

    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}", "danger")

    return render_template('usergroup-administration.html', form=form, usergroup=users_in_group, heading="Inviter bruker")



def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc