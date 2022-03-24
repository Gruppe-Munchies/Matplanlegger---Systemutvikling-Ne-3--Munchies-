from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf import csrf

import backend.auth.queries
import backend.main.views as mainpage
import backend.auth.views as auth
import backend.recipes.views as recipes
import backend.ingredients.views as ingredients
from local_db.db_user_info import username, password, DB_NAME

# Flask configuration
app = Flask(__name__)
app.register_blueprint(mainpage.mainpage)
app.register_blueprint(auth.auth)
app.register_blueprint(recipes.recipes)
app.register_blueprint(ingredients.ingredient)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@localhost/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # stops warning
app.config['SECRET_KEY'] = "secretkey"
app.config['WTF_CSRF_SECRET_KEY'] = "secretkey"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ingredienser')
def ingredienser():
    return render_template('ingredienser.html')


@app.route('/handleliste')
def handleliste():
    return render_template('handleliste.html')


@app.route('/ukesmeny')
def ukesmeny():
    return render_template('ukesmeny.html')


@app.route('/user-administration')
def userAdministration():
    return render_template('user-administration.html')


@app.route('/legg-til-rett')
def legg_til_rett():
    return render_template('legg-til-rett.html')


if __name__ == '__main__':
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        res = backend.auth.queries.fetchUser(user_id)
        return res
        # return User.get(user_id)



    app.run()

# """
# class User(Usermixin, db.Model):
#     id = db.Columb(db.Integer, primary_key=True)
#     username = db.Colum(db.String(30)
#
# """