from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usergroup, Usertype, WeeklyMenu, Base, sessionmaker
from local_db.local_db_create import engine


def loadSession():
    metadata = Base.metadata # Ikke sikker på hva denne brukes til enda, men den var med i eksempelet 😎
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# Test quieries
session = loadSession()
res = session.query(User).all()
print(res[0].email)
