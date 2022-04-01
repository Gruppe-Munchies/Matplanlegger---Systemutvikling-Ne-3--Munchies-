from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, session
import backend.auth.queries as auth_queries
import backend.auth.views
from backend.auth.forms import LoginForm, RegisterForm, InviteForm, createUserGroupForm, UserGroupSelector
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

    #adminCheck = fetchUserTypeByUserIdAndGroupId(6, 1) # Relatert til issue NR:139

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
@login_required
def createGroup():
    createUGForm = createUserGroupForm(request.form)

    if request.method == 'POST' and createUGForm.validate():
        userId = current_user.id
        if fetchUserGroup(createUGForm.usergroup.data):  # Check if usergroup already exists
            flash('Gruppen finnes allerede!')
        else:
            auth_queries.insert_to_usergroup(createUGForm.usergroup.data)
            userGroup = fetchUserGroup(createUGForm.usergroup.data)
            userGroupId = userGroup.iduserGroup
            userTypeId = 1
            auth_queries.insert_to_user_has_userGroup(int(userId), int(userGroupId), int(userTypeId))
            flash('Gruppen ble opprettet!')

    return redirect(url_for("auth.invite"))


# INVITE USER TO USERGROUP
@auth.route('/groupadmin', methods=['GET', 'POST'])
@login_required
def invite():
    form = InviteForm(request.form)
    createUGForm = createUserGroupForm(request.form)

    activeGroup = session.get('group_to_use')  # Bruk aktiv gruppe

    users_in_group = fetchUsersInUsergroupById(activeGroup)  # Fetch users in group

    # Sjekker om brukeren, i den gitte brukergruppa, har adminrettigheter.
    usertype = fetchUserTypeByUserIdAndGroupId(current_user.id, activeGroup)
    userIsAdmin = False
    if usertype == 1:
        userIsAdmin = True

    usertypes = fetchAllUserTypes()  # Fetch available usertypes to populate dropdown

    if request.method == 'POST' and form.validate():
        user_to_invite = fetchUser(form.username.data)  # Fetch user to invite
        usertypeId = form.usertype.data  # Usertype assigned to invited user

        # Check if invited user exists
        if not user_to_invite:
            flash("Brukeren finnes ikke.", "danger")
            return render_template('usergroup-administration.html', form=form, ugform=createUGForm,
                                   users=users_in_group, usertypes=usertypes,
                                   heading="Inviter bruker", userIsAdmin=userIsAdmin)

        # User exists, add to group if not already member
        # TODO: Adds withouth asking user. Should be an invite.

        if not fetch_user_in_usergroup(user_to_invite.id, activeGroup):
            if userIsAdmin:
                userId = user_to_invite.id
                userGroupId = activeGroup
                auth_queries.insert_to_user_has_userGroup(int(userId), int(userGroupId), int(usertypeId))
                flash(f'{user_to_invite.username} ble invitert!')
            else:
                flash('Krever admin-tilgang!')
        else:
            flash(f"{user_to_invite.username} er allerede medlem av gruppen!")
        return redirect(url_for("auth.invite"))

    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{error_message}", "danger")

    return render_template('usergroup-administration.html', form=form, ugform=createUGForm, users=users_in_group,
                           usertypes=usertypes, heading="Inviter bruker", userIsAdmin=userIsAdmin)


@auth.route('/profil', methods=['GET', 'POST'])
def profil():
    print(session.get('group_to_use'))
    # TODO: Må vell legge inn usertype pr group i profilsiden egentlig.
    groups = fetchAllUserGroupsUserHas(current_user.id)
    # TODO:Bør flyttes til nav

    form = UserGroupSelector(request.form)
    # choice = [(0,"Velg gruppe å samhandle som")]
    choice = []

    for i in fetchAllUserGroupsUserHas(current_user.id):
        choice.append((i.iduserGroup, i.groupName))

    form.idOgNavn.choices = choice

    if request.method == 'POST' and form.validate():
        selectFieldGroup = form.idOgNavn.data  # Får tilbake group_id her


        session['group_to_use'] = selectFieldGroup
        session['groupname_to_use'] = fetchUserGroupById(selectFieldGroup).groupName
        return redirect(request.referrer)
    #########   Slutt valg av group    #############
    form.idOgNavn.data = session.get('group_to_use', 0)  # setter standard til den aktive

    return render_template('profilepage.html', form=form, groups=groups)




@auth.route('/changeusertype', methods=['GET', 'POST'])
@login_required
def change_usertype():
    userid=request.args["userid"]
    usergroupid=request.args["usergroupid"]
    usertypeid=request.args["usertypeid"]

    usergroup_admin_update_usertypes(userid, usergroupid, usertypeid)

    return redirect(url_for("auth.invite"))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
