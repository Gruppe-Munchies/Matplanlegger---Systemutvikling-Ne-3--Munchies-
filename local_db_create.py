from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from db_user_info import username, password
DB_NAME = "eplekake"

# Create database
engine = create_engine(f"mysql+pymysql://{username}:{password}@localhost/{DB_NAME}")
if not database_exists(engine.url):
    create_database(engine.url)
print(f"Database {DB_NAME} already exists:", database_exists(engine.url))
