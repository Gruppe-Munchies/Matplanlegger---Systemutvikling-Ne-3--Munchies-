from local_db.session import loadSession
from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup
from werkzeug.security import generate_password_hash, check_password_hash

#############
#    User   #
#############

# Fetch user from username
def fetchUser(user_name):
    session = loadSession()
    res = session.query(User).where(User.username == user_name).first()
    return res

def fetchUserById(user_id):
    session = loadSession()
    res = session.query(User).where(User.id == user_id).first()
    return res

# Fetch email from username
def return_email_from_name(name):
    session = loadSession()
    res = session.query(User).where(User.firstname == name).all()
    return res


# Add user Id, name of user group, and user type in group
def insert_to_user_has_userGroup(user_id, usergroup_id, user_type_id):
    session = loadSession()
    new_insertion = UserHasUsergroup(user_userId=user_id, userGroup_iduserGroup=usergroup_id,
                                     userType_iduserType=user_type_id)
    session.add(new_insertion)
    session.commit()


# Add user
def insert_to_user(name, email, firstname, lastname, password):
    session = loadSession()
    hashedPassword = generate_password_hash(password)
    new_user = User(username=name, email=email, firstname=firstname, lastname=lastname, password=hashedPassword)
    session.add(new_user)
    session.commit()


# fetch_usergroups_associated_with_user(user_id) - to be used in ingredients
# fetch_role_in_usergroup(user_id, usergroup) - to see which role the user has in a certain group.

#fetch_firstname_user(user_id) - or should we use username? user_id is primary key. This is for showing who's logged in.
#fetch_lasttname_user(user_id)
# compare hashed password  (login)

# optional: change email, firstname, lastname, password. - one function, or many? Have to be reviewed
#this could be a form for the user to administrate own settings.
#when updated, use session.commit( values..?)




#############
# Usergroup #
#############

def userGroup():
    session = loadSession() # kobler til databasen
    res = session.query(Usergroup).all() #henter ut fra tabell Usergroup (via orm.py i local_db)
    return res #henter ut alle kolonnene i denne tabellen

def fetchAllUsers():
    session = loadSession()  # kobler til databasen
    res = session.query(User).all()  # henter ut fra tabell User (via orm.py i local_db)
    return res  # henter ut alle kolonnene i denne tabellen

def fetchAllUserGroups():
    session = loadSession()  # kobler til databasen
    res = session.query(Usergroup).all()  # henter ut fra tabell Usergroup (via orm.py i local_db)
    return res  # henter ut alle kolonnene i denne tabellen


def fetchUserGroup(group_name):
    session = loadSession()
    res = session.query(Usergroup).where(Usergroup.groupName == group_name).first()
    # res = session.query(Usergroup).filter_by(groupName=group_name).values(text("iduserGroup"))
    return res

def fetchGroupsWhereUserHaveAdmin(username, group_name):
    session = loadSession()
    res = session.query(Usergroup, User, Usertype).join(UserHasUsergroup,
                                                        Usergroup.iduserGroup == UserHasUsergroup.userGroup_iduserGroup).join(User,
                                                        User.id == UserHasUsergroup.user_userId).join(Usertype,
                                                        Usertype.iduserType == UserHasUsergroup.userType_iduserType).filter(
                                                        Usergroup.groupName == group_name).filter(
                                                        User.username == username).filter(
                                                        Usertype.userTypeName == "Admin").all()
    pass

def fetchUsersInUsergroup(group_name):
    session = loadSession()
    res = session.query(Usergroup, User, Usertype).join(UserHasUsergroup,
                                                        Usergroup.iduserGroup == UserHasUsergroup.userGroup_iduserGroup).join(User,
                                                        User.id == UserHasUsergroup.user_userId).join(Usertype,
                                                        Usertype.iduserType == UserHasUsergroup.userType_iduserType).filter(
                                                        Usergroup.groupName == group_name).all()
    return res

def fetchUserType(usertype):
    session = loadSession()
    res = session.query(Usertype).where(Usertype.userTypeName == usertype).first()
    return res

def fetchAllUserTypes():
    session = loadSession()
    res = session.query(Usertype).all()
    return res

# Add default usergroups
def insert_to_usergroup(name):
    session = loadSession()
    usergroup = Usergroup(groupName=name)
    session.add(usergroup)
    session.commit()


# # Add to usergroup_has_ingredient
# def insert_to_usergroup_has_ingredient(userGroup, ingredient, price, unit):
#     session = loadSession()
#     new_userGroupIngredient = UsergroupHasIngredient(userGroup_iduserGroup=userGroup,
#                                                      ingredient_idingredient=ingredient, price=price, unit=unit)
#     session.add(new_userGroupIngredient)
#     session.commit()


############
# Usertype #
############


# Add default usertypes
def insert_to_usertype():
    session = loadSession()
    usertype1 = Usertype(userTypeName="Admin")
    usertype2 = Usertype(userTypeName="Bruker")
    session.add_all([usertype1, usertype2])
    session.commit()

def usergroup_admin_update_usertypes(userid, usergroupid, usertypeid):
    session = loadSession()
    user = session.query(UserHasUsergroup).where(UserHasUsergroup.user_userId == userid, UserHasUsergroup.userGroup_iduserGroup == usergroupid).first()
    user.user_userId = usertypeid
    session.commit()