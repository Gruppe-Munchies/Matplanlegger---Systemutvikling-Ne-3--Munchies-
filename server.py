from flask import Flask, render_template
from flask_wtf import csrf


import backend.main.views as mainpage
import backend.auth.views as auth
import backend.ingredients.views as ingredients
from local_db.db_user_info import username, password, DB_NAME
from local_db.db_testData import test_data

# Flask configuration
app = Flask(__name__)
app.register_blueprint(mainpage.mainpage)
app.register_blueprint(auth.auth)
app.register_blueprint(ingredients.ingredient)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@localhost/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # stops warning
app.config['SECRET_KEY'] = "secretkey"
app.config['WTF_CSRF_SECRET_KEY'] = "secretkey"


@app.route('/')
def index():
    return "noe annet"


@app.route('/testdata')
def testdata():
    test_data()

@app.route('/oppskrift')
def oppskrift():
    return render_template('oppskrift.html')

@app.route('/ingredienser')
def ingredienser():
    return render_template('ingredienser.html')

@app.route('/handleliste')
def handleliste():
    return render_template('handleliste.html')

@app.route('/ukesmeny')
def ukesmeny():
    return render_template('ukesmeny.html')

@app.route('/legg-til-bruker')
def legg_til_bruker():
    return render_template('legg-til-bruker.html')

@app.route('/legg-til-rett')
def legg_til_rett():
    return render_template('legg-til-rett.html')

if __name__ == '__main__':
    app.run()
