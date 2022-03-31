from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
import backend.auth.queries as auth_queries
from backend.auth.forms import LoginForm, RegisterForm, InviteForm, createUserGroupForm, RemoveUserFromGroup
from backend.auth.queries import *  # fetchAllUserGroups, fetchUser, fetchUserGroup
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        input_username = form.username.data
        input_password = form.password.data

        user_from_db = fetchUser(input_username)

        # Er brukeren i databasen
        if user_from_db:
            stored_hashed_password = user_from_db.password

            # Sjekker om brukernavn og hashet passord stemmer overens med databasen
            if check_password_hash(stored_hashed_password, input_password):
                flash("Login vellykket!")
                login_user(user_from_db)
                flash("Velkommen " + current_user.username)
        else:
            flash("Brukernavn eller passord er feil")
            return redirect(url_for("auth.login"))

    return render_template('index.html', form=form, current_user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    user_group = fetchAllUserGroups()
    all_users = fetchAllUsers()
    usergroup = userGroup()

    # adminCheck = fetchUserTypeByUserIdAndGroupId(6, 1) # Relatert til issue NR:139

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
        # Check if creating usergroup. If not, set group to "ingen" and usertype to 2 (not admin)
        if (usergroup == ""):
            usertype = 2
            usergroup = "ingen"
        else:
            usertype = 1

        # Insert user to database
        auth_queries.insert_to_user(username, email, firstname, lastname, password)
        # Insert userGroup to database
        auth_queries.insert_to_usergroup(usergroup)

        # Get userID from newly inserted user
        fetchedUser = fetchUser(username)
        userID = fetchedUser.id
        # Fetch userGroupID from newly inserted usergroup
        fetchedUserGroup = fetchUserGroup(usergroup)
        userGroupId = fetchedUserGroup.iduserGroup

        # Insert userID, userGroupID and userType to "user_has_userGroup"
        auth_queries.insert_to_user_has_userGroup(int(userID), int(userGroupId), int(usertype))

        flash('Registreringen var vellykket!')
        return redirect(url_for("auth.register"))

    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}", "danger")

    return render_template('register.html', form=form, ug=user_group, users=all_users)


# CREATE USERGROUP
@auth.route('/creategroup', methods=['GET', 'POST'])
def createGroup():
    createUGForm = createUserGroupForm(request.form)
    if request.method == 'POST' and createUGForm.validate():
        activeUser = "Username for innlogget bruker"  # TODO: Get username for logged in user
        user = fetchUser(activeUser)
        userId = 9  # TODO: Replace with actual "id for logged in user
        auth_queries.insert_to_usergroup(createUGForm.usergroup.data)
        userGroup = fetchUserGroup(createUGForm.usergroup.data)
        userGroupId = userGroup.iduserGroup
        userTypeId = 1
        auth_queries.insert_to_user_has_userGroup(int(userId), int(userGroupId), int(userTypeId))
        flash('Gruppen ble opprettet!')

    return redirect(url_for("auth.groupadmin"))


@auth.route('/groupadmin', methods=['GET', 'POST'])
def groupadmin():
    invite_form = InviteForm(request.form)
    createUGForm = createUserGroupForm(request.form)
    deleteForm = RemoveUserFromGroup(request.form)

    users_in_group = fetchUsersInUsergroupById(
        1)  # Fetch users in group #TODO få bort hardkoding på denne gruppa -må samhandles en plass

    # sjekker om brukeren, i den gitte brukergruppa, har adminrettigheter.
    # TODO Legg in metode for de fire neste linjene

    usertype = fetchUserTypeByUserIdAndGroupId(current_user.id, 1)  # TODO få bort hardkoding på gruppe 2!!!
    userIsAdmin = False

    if usertype == 1:
        userIsAdmin = True

    usertypes = fetchAllUserTypes()
    owner = "Username for gruppeeier"  # TODO: Get username for logged in user

    groups_with_admin = fetchGroupsWhereUserHaveAdmin(owner)

    for fieldName, error_messages in invite_form.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}", "danger")

    return render_template('usergroup-administration.html', form=invite_form, ugform=createUGForm, delform=deleteForm,
                           users=users_in_group,
                           ownedgroups=groups_with_admin, usertypes=usertypes, heading="Inviter bruker",
                           userIsAdmin=userIsAdmin)


@auth.route('/groupadmin/remove', methods=['GET', 'POST'])
def removeUserFromGroup():
    deleteForm = RemoveUserFromGroup(request.form)

    userId = deleteForm.username.data
    groupId = deleteForm.userGroupName.data

    auth_queries.remove_row_from_UserHasUsergroup(int(userId), int(groupId))

    return redirect(url_for("auth.groupadmin"))


@auth.route('/groupadmin/inviter', methods=['GET', 'POST'])
def inviteUser():
    invite_form = InviteForm(request.form)

    user_to_invite = fetchUser(invite_form.username.data)  # Fetch user to invite
    usergroup = fetchUserGroup(invite_form.usergroup.data)  # Fetch usergroup
    usertype = fetchUserType(invite_form.usertype.data)  # Fetch usertype

    userId = user_to_invite.userId
    userGroupId = usergroup.iduserGroup
    usertypeId = usertype.iduserType

    auth_queries.insert_to_user_has_userGroup(int(userId), int(userGroupId), int(usertypeId))

    flash('Brukeren ble lagt til!')
    return redirect(url_for("auth.groupadmin"))


@auth.route('/profil', methods=['GET', 'POST'])
def profil():
    user_groups = fetchAllUserGroupsUserHas(current_user.id)

    return render_template('profilepage.html', groups=user_groups)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
