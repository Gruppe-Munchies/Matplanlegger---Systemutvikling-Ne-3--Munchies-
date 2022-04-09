from urllib.parse import urljoin, urlparse
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, session
import backend.auth.queries as auth_queries
import backend.auth.views
from backend.auth.forms import LoginForm, RegisterForm, InviteForm, createUserGroupForm, UserGroupSelector
from backend.auth.forms import LoginForm, RegisterForm, InviteForm, createUserGroupForm, RemoveUserFromGroup
from backend.auth.queries import *  # fetchAllUserGroups, fetchUser, fetchUserGroup
from flask_login import login_required, login_user, logout_user, current_user

current_group = 0

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

                if fetch_first_usergroups_for_user(user_from_db.id):
                    session['group_to_use'] = int(fetch_first_usergroups_for_user(user_from_db.id).iduserGroup)
                    session['groupname_to_use'] = fetchUserGroupById(session.get('group_to_use')).groupName
                else:
                    session['group_to_use'] = 0
                    session['groupname_to_use'] = ""

                print(session.get('group_to_use'))
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
        auth_queries.insert_to_user_has_userGroup(int(userID), int(userGroupId), int(usertype), 2) #TODO: MemberStatus er hardkodet til Accepted

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
        auth_queries.insert_to_usergroup(createUGForm.usergroup.data)
        userGroup = fetchUserGroup(createUGForm.usergroup.data)
        userGroupId = userGroup.iduserGroup
        userTypeId = 1
        auth_queries.insert_to_user_has_userGroup(int(userId), int(userGroupId), int(userTypeId), 2)
        flash('Gruppen ble opprettet!')

    return redirect(url_for("auth.groupadmin"))


@auth.route('/groupadmin', methods=['GET', 'POST'])
def groupadmin():
    if not fetch_first_usergroups_for_user(current_user.id):
        createUGForm = createUserGroupForm(request.form)
        invite_form = InviteForm(request.form)
        return render_template('usergroup-administration.html', form=invite_form, ugform=createUGForm)


    invite_form = InviteForm(request.form)
    createUGForm = createUserGroupForm(request.form)
    deleteForm = RemoveUserFromGroup(request.form)

    # TODO: get usergroup the user's currently in(in session)
    users_in_group = fetchUsersInUsergroupById(
        session.get(
            'group_to_use'))  # Fetch users in group

    # sjekker om brukeren, i den gitte brukergruppa, har adminrettigheter.
    # print("brukergruppe: "+session.get('group_to_use'))
    usertype = fetchUserTypeByUserIdAndGroupId(current_user.id,
                                               session.get('group_to_use'))

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

    # TODO: Handle error when deleting oneself or have a setup where a user can't delete remove themself from the group on the group admin page.
    if userId != current_user.id:
        auth_queries.remove_row_from_UserHasUsergroup(int(userId), int(groupId))
    else:
        flash("Kan ikke slette degselv")

    return redirect(url_for("auth.groupadmin"))


@auth.route('/groupadmin/inviter', methods=['GET', 'POST'])
def inviteUser():
    invite_form = InviteForm(request.form)
    activeGroup = session.get('group_to_use')  # Bruk aktiv gruppe


    # Sjekker om brukeren, i den gitte brukergruppa, har adminrettigheter.
    usertype = fetchUserTypeByUserIdAndGroupId(current_user.id, activeGroup)
    userIsAdmin = False
    if usertype == 1:
        userIsAdmin = True

    if request.method == 'POST' and invite_form.validate():
        user_to_invite = fetchUser(invite_form.username.data)  # Fetch user to invite
        usertypeId = invite_form.usertype.data  # Usertype assigned to invited user

        # Check if invited user exists
        if user_to_invite:
            # User exists, check if already member or invited
            if not fetch_user_in_usergroup(user_to_invite.id, activeGroup):
                #Check if Admin
                if userIsAdmin:
                    userId = user_to_invite.id
                    userGroupId = activeGroup
                    auth_queries.insert_to_user_has_userGroup(int(userId), int(userGroupId), int(usertypeId), 1)
                    flash(f'{user_to_invite.username} ble invitert!')
                else:
                    # Not Admin
                    flash('Krever admin-tilgang!')
            else:
                # User already member
                flash(f"{user_to_invite.username} er allerede invitert eller medlem av gruppen!")
        else:
            # User does not exist
            flash("Brukeren finnes ikke.", "danger")

        return redirect(url_for("auth.groupadmin"))

@auth.route('/groupadmin/inviter/response', methods=['GET', 'POST'])
def response():

    userid = current_user.id
    usergroup = request.args["usergroup"]
    response = request.args["response"]

    if response == "1":
        invitationResponse(userid, usergroup, 2)
    elif response == "2":
        invitationResponse(userid, usergroup, 3)
    else:
        return redirect(url_for("auth.profil"))

    return redirect(url_for("auth.profil"))



@auth.route('/profil', methods=['GET', 'POST'])
def profil():
    print(session.get('group_to_use'))
    # TODO: Må vell legge inn usertype pr group i profilsiden egentlig.
    groups = fetchAllUserGroupsUserHas(current_user.id)
    # TODO:Bør flyttes til nav

    #Fetch pending invitations
    invitations = fetchPendingInvitations(current_user.id)

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

    return render_template('profilepage.html', form=form, groups=groups, invitations=invitations)


@auth.route('/changeusertype', methods=['GET', 'POST'])
@login_required
def change_usertype():
    userid = request.args["userid"]
    usergroupid = request.args["usergroupid"]
    usertypeid = request.args["usertypeid"]

    usergroup_admin_update_usertypes(userid, usergroupid, usertypeid)

    return redirect(url_for("auth.groupadmin"))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
