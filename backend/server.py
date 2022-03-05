from flask import Flask, render_template
from local_db.db_user_info import username, password, DB_NAME
from local_db.test_queries import return_email_from_name, insert_to_user
from local_db.db_testData import test_data

# Flask configuration
app = Flask(__name__, template_folder='C:/UiT/Python/Munchies/Matplanlegger---Systemutvikling-Ne-3--Munchies-/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@localhost/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # stops warning

@app.route('/testdata')
def testdata():
    test_data()

if __name__ == '__main__':
    app.run()
