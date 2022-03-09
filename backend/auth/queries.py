from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from flask_alchemy_db_creation.local_db_create import engine
from sqlalchemy.sql import text

def loadSession(): #denne bruker vi
    metadata = Base.metadata  # Ikke sikker på hva denne brukes til enda, men den var med i eksempelet 😎
    Session = sessionmaker(bind=engine)
    session = Session()
    return session



# Test quieries
#session = loadSession()
#res = session.query(User).all()
#print(res[0].email)


def fetchAllUserGroups():
    session = loadSession() # kobler til databasen
    res = session.query(Usergroup).all() #henter ut fra tabell Usergroup (via orm.py i local_db)
    return res #henter ut alle kolonnene i denne tabellen

def fetchUser(user_name):
    session = loadSession()
    res = session.query(User).where(User.username == user_name).first()
    #res = session.query(User).filter_by(username=user_name).values(text("userId"))
    return res

def fetchUserGroup(group_name):
    session = loadSession()
    res = session.query(Usergroup).where(Usergroup.groupName == group_name).first()
    #res = session.query(Usergroup).filter_by(groupName=group_name).values(text("iduserGroup"))
    return res

