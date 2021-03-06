from sqlalchemy import create_engine
from sqlalchemy_utils.functions.database import database_exists, create_database
from local_db.db_user_info import username, password

DB_NAME = "munchbase"

# Create database
engine = create_engine(f"mysql+pymysql://{username}:{password}@localhost/{DB_NAME}", pool_size=200, max_overflow=0)

database_exists: bool = database_exists(engine.url)
if not database_exists:
    create_database(engine.url)
print(f"Database {DB_NAME} already exists:", database_exists)
