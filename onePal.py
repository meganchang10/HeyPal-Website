from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Activity, Base, Pal, User, MyActivity

engine = create_engine('sqlite:///heypal.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


Pal1 = Pal(user_id=5, pal_id=1, name = "Megan")
session.add(Pal1)
session.commit()

Pal1 = Pal(user_id=1, pal_id=5, name = "Megan")
session.add(Pal1)
session.commit()

