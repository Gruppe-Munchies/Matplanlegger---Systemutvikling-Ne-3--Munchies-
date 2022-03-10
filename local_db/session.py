from flask import render_template
from sqlalchemy import inspect

from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usertype, Usergroup, UsergroupHasIngredient, WeeklyMenu, Base, UserHasUsergroup
from sqlalchemy.orm import Session, declarative_base, sessionmaker, column_property
from flask_alchemy_db_creation.local_db_create import engine


def loadSession():
    metadata = Base.metadata  # Ikke sikker på hva denne brukes til enda, men den var med i eksempelet 😎
    Session = sessionmaker(bind=engine)
    session = Session()
    return session