from local_db_create import engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

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
    __tablename__ = 'recipe'
    __table_args__ = {'autoload': True}
    """"""


class RecipeHasWeeklyMenu(Base):
    """"""
    __tablename__ = 'recipe_has_weeklymenu'
    __table_args__ = {'autoload': True}
    """"""


class RecipeAvailability(Base):
    """"""
    __tablename__ = 'recipeavailability'
    __table_args__ = {'autoload': True}
    """"""


class Usergroup(Base):
    """"""
    __tablename__ = 'usergroup'
    __table_args__ = {'autoload': True}
    """"""


class UsergroupHasIngredient(Base):
    """"""
    __tablename__ = 'usergroup_has_ingredient'
    __table_args__ = {'autoload': True}
    """"""


class Usertype(Base):
    """"""
    __tablename__ = 'usertype'
    __table_args__ = {'autoload': True}
    """"""


class WeeklyMenu(Base):
    """"""
    __tablename__ = 'weeklymenu'
    __table_args__ = {'autoload': True}
    """"""


def loadSession():
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == "__main__":
    session = loadSession()
    res = session.query(User).where('username', 'Melvin')
    print(res[0].email)
