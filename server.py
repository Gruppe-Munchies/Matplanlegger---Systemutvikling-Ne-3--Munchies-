from flask import Flask, render_template
from flask_wtf import csrf

import backend.main.views as mainpage
import backend.auth.views as auth
import backend.ingredients.views as ingredients
from local_db.db_user_info import username, password, DB_NAME
from local_db.insert_to_db import return_email_from_name, insert_to_user
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


if __name__ == '__main__':
    app.run()
