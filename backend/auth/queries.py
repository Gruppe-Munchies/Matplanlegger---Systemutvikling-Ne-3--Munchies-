from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from flask_alchemy_db_creation.local_db_create import engine


def loadSession(): #denne bruker vi
    metadata = Base.metadata  # Ikke sikker på hva denne brukes til enda, men den var med i eksempelet 😎
    Session = sessionmaker(bind=engine)
    session = Session()
    return session



# Test quieries
session = loadSession()
res = session.query(User).all()
print(res[0].email)


def userGrouo():
    session = loadSession() # kobler til databasen
    res = session.query(Usergroup).all() #henter ut fra tabell Usergroup (via orm.py i local_db)
    return res #henter ut alle kolonnene i denne tabellen

