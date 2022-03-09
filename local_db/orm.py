from flask_alchemy_db_creation.local_db_create import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base(engine)

class User(Base):
    """"""
    __tablename__ = 'user'
    __table_args__ = {'autoload': True}
    """"""


class Ingredient(Base):
    """"""
    __tablename__ = 'ingredient'
    __table_args__ = {'autoload': True}
    """"""


class Recipe(Base):
    """"""
    __tablename__ = 'recipe'
    __table_args__ = {'autoload': True}
    """"""


class RecipeHasIngredient(Base):
    """"""
    __tablename__ = 'recipe_has_ingredient'
    __table_args__ = {'autoload': True}
    """"""


class RecipeHasWeeklyMenu(Base):
    """"""
    __tablename__ = 'recipe_has_weeklyMenu'
    __table_args__ = {'autoload': True}
    """"""


class RecipeAvailability(Base):
    """"""
    __tablename__ = 'recipeAvailability'
    __table_args__ = {'autoload': True}
    """"""


class Usergroup(Base):
    """"""
    __tablename__ = 'userGroup'
    __table_args__ = {'autoload': True}
    """"""


class UsergroupHasIngredient(Base):
    """"""
    __tablename__ = 'userGroup_has_ingredient'
    __table_args__ = {'autoload': True}
    """"""

class UserHasUsergroup(Base):
    """"""
    __tablename__ = 'user_has_userGroup'
    __table_args__ = {'autoload': True}
    """"""

class Usertype(Base):
    """"""
    __tablename__ = 'userType'
    __table_args__ = {'autoload': True}
    """"""


class WeeklyMenu(Base):
    """"""
    __tablename__ = 'weeklyMenu'
    __table_args__ = {'autoload': True}
    """"""




