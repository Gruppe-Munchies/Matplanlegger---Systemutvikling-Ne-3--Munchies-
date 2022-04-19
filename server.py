from flask import Flask, render_template, session
from flask_login import LoginManager, current_user

import backend.auth.queries
import backend.main.views as mainpage
import backend.weekly_menu.queries as weekly
import backend.auth.views as auth
import backend.recipes.views as recipes
import backend.ingredients.views as ingredients
import backend.weekly_menu.views as weekly_menu
#from backend import weekly_menu

import backend.weekly_menu.views
from backend import weekly_menu
from local_db.db_user_info import username, password, DB_NAME

# Flask configuration
app = Flask(__name__)
app.register_blueprint(mainpage.mainpage)
app.register_blueprint(auth.auth)
app.register_blueprint(recipes.recipes)
app.register_blueprint(ingredients.ingredient)
app.register_blueprint(weekly_menu.weeklyMenu)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@localhost/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # stops warning
app.config['SECRET_KEY'] = "secretkey"
app.config['WTF_CSRF_SECRET_KEY'] = "secretkey"


@app.route('/')
def index():
    session['group_to_use'] = 0
    session['groupname_to_use'] = ""
    if current_user:
        print("ja er en bruker ja")
    return render_template('index.html')


@app.route('/ingredienser')
def ingredienser():
    return render_template('ingredienser.html')


@app.route('/handleliste')
def handleliste():
    return render_template('handleliste.html')


@app.route('/leggtilmeny')
def nyUkesmeny():
    return render_template('newWeeklyMenu.html')



login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    res = backend.auth.queries.fetchUserById(user_id)
    return res


if __name__ == '__main__':

    app.run()
