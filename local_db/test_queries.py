from flask import render_template
from sqlalchemy import inspect

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from flask_alchemy_db_creation.local_db_create import engine


def loadSession():
    metadata = Base.metadata  # Ikke sikker på hva denne brukes til enda, men den var med i eksempelet 😎
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

# Test queries
def return_email_from_name(name):
    session = loadSession()
    res = session.query(User).filter(User.firstname == name).all()
    return res
