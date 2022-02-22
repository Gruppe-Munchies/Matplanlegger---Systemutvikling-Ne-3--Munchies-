from flask import Flask
from local_db.local_db_create import DB_NAME
from local_db.db_user_info import username, password

# Flask configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@localhost/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # stops warning


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello Munchies!'
