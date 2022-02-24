from flask import Flask
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usergroup, Usertype, WeeklyMenu, Base, sessionmaker
from local_db.local_db_create import engine


def loadSession():
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# Test quieries
session = loadSession()
res = session.query(User).where('username', 'Melvin')
print(res[0].email)
