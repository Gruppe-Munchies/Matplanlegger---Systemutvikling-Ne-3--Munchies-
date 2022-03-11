from local_db.session import loadSession
from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup


#############
#    User   #
#############

# Fetch user from username
def fetchUser(user_name):
    session = loadSession()
    res = session.query(User).where(User.username == user_name).first()
    # res = session.query(User).filter_by(username=user_name).values(text("userId"))
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
    new_user = User(username=name, email=email, firstname=firstname, lastname=lastname, password=password)
    session.add(new_user)
    session.commit()


#############
# Usergroup #
#############

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


# Add default usergroups
def insert_to_usergroup(name):
    session = loadSession()
    usergroup = Usergroup(groupName=name)
    session.add(usergroup)
    session.commit()


# Add to usergroup_has_ingredient
def insert_to_usergroup_has_ingredient(userGroup, ingredient, price, unit):
    session = loadSession()
    new_userGroupIngredient = UsergroupHasIngredient(userGroup_iduserGroup=userGroup,
                                                     ingredient_idingredient=ingredient, price=price, unit=unit)
    session.add(new_userGroupIngredient)
    session.commit()


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
