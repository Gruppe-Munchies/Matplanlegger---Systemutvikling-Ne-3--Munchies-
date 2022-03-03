from flask import Flask, render_template
from local_db.db_user_info import username, password, DB_NAME
from local_db.test_queries import return_email_from_name, insert_to_user

# Flask configuration
app = Flask(__name__, template_folder='C:/UiT/Python/Munchies/Matplanlegger---Systemutvikling-Ne-3--Munchies-/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@localhost/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # stops warning


@app.route('/test')
def hello_world():  # put application's code here
    email = return_email_from_name("Jan Erik")
    return render_template('test2.html', result=email)

@app.route('/insert')
def insert():
    insert_to_user("brukernavn", "epost", "fornavn", "etternavn", "passord", "1", "1")

if __name__ == '__main__':
    app.run()
