from local_db_create import engine
from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine, select

# Initialise Base with engine
Base = automap_base()
Base.prepare(engine, reflect=True)

# Add ORM for table user
user = Base.classes.user

# Query data from table user
malvin = user.query.filter_by(username="Malvin Khan").first()
print(malvin.email)
print(malvin.firstname)

# Automap approach hentet fra
# https://docs.sqlalchemy.org/en/14/orm/extensions/automap.html

# ingredient = Base.classes.ingredient
# stm = select([ingredient])
# session = Session(engine)
# connection = engine.connect()
# results = connection.execute(stm).fetchall()

# for result in results:
#     print(result)
