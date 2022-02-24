from local_db_create import engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

Base = automap_base()
Base.prepare(engine, reflect=True)

ingredient = Base.classes.ingredient
user = Base.classes.user
stm = select([ingredient])

session = Session(engine)
connection = engine.connect()
results = connection.execute(stm).fetchall()

for result in results:
    print(result)
