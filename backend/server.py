from flask import Flask
from local_db.orm import User, Ingredient, Recipe, RecipeHasIngredient, RecipeHasWeeklyMenu, RecipeAvailability, \
    Usergroup, Usertype, WeeklyMenu, Base, sessionmaker
from local_db.local_db_create import engine
from sqlalchemy.orm import session
from local_db.local_db_create import DB_NAME
from local_db.db_user_info import username, password

# Flask configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@localhost/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # stops warning


def loadSession():
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session




@app.route('/')
def hello_world():  # put application's code here
    return 'Hello Munchies!'


if __name__ == '__main__':

    #Test quieries
    session = loadSession()
    res = session.query(User).where('username', 'Melvin')
    print(res[0].email)

    app.run()
