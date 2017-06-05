from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Activity, Base, Pal, User

engine = create_engine('sqlite:///heypal.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Megan Chang", email="meganchang10@gmail.com",id = 1)
session.add(User1)
session.commit()


User1 = User(name="Christa Heinrich", email="changsta5@gmail.com", id=2, picture= "/static/img/Christa_Heinrich.jpg")
session.add(User1)
session.commit()

User1 = User(name="David Childs", email="david@gmail.com", id=3, picture= "/static/img/David_Childs.jpg")
session.add(User1)
session.commit()

User1 = User(name="Sam Close", email="sam@gmail.com", id=4, picture= "/static/img/Sam_Close.jpg")
session.add(User1)
session.commit()

User1 = User(name="Sam Delker", email="samd@gmail.com", id=5, picture= "/static/img/Sam_Delker.jpg")
session.add(User1)
session.commit()

User1 = User(name="Sam Little", email="saml@gmail.com", id=6, picture= "/static/img/Sam_Little.jpg")
session.add(User1)
session.commit()

User1 = User(name="Remster", email="remi@gmail.com", id=7, picture= "/static/img/Remster.jpg")
session.add(User1)
session.commit()


# Christa Heinrich
Pal1 = Pal(name="Christa Heinrich", id=1, user_id=1, pal_id=2, image= "/static/img/Christa_Heinrich_pal.jpg")
session.add(Pal1)
session.commit()

# David Childs
Pal1 = Pal(name = "David Childs", id=2, user_id=1, pal_id=3, image= "/static/img/David_Childs_pal.jpg")
session.add(Pal1)
session.commit()

# Sam Close
Pal1 = Pal(name = "Sam Close", id=3, user_id=1, pal_id=4, image= "/static/img/Sam_Close_pal.jpg")
session.add(Pal1)
session.commit()

# Sam Delker
Pal1 = Pal(name = "Sam Delker", id=4, user_id=1, pal_id=5, image= "/static/img/Sam_Delker_pal.jpg")
session.add(Pal1)
session.commit()

# Sam Little
Pal1 = Pal(name = "Sam Little", id=5, user_id=1, pal_id=6, image= "/static/img/Sam_Little_pal.jpg")
session.add(Pal1)
session.commit()

# Remi
Pal1 = Pal(name = "Remster", id=6, user_id=1, pal_id=7, image= "/static/img/Remster_pal.jpg")
session.add(Pal1)
session.commit()


#Pal1 = Pal(user_id=1, pal_id=5, name = "Megan(FB)")
#Pal1 = Pal(user_id=1, pal_id=5, name = "Megan Chang")
#session.add(Pal1)
#session.commit()


# New person will have pals immediately!

#Pal1 = Pal(user_id=5, pal_id=1, name = "Megan(gmail)")
#Pal1 = Pal(user_id=5, pal_id=1, name = "Megan Chang")
#session.add(Pal1)
#session.commit()




count = 1
Activity1 = Activity(name = "Volleyball", location = "Leadbetter Beach", lat = "34.40234809999999", lng = "-119.69934519999998", fullName= 'Volleyball @ Leadbetter Beach', image = "http://www.smart-magazine.com/content/uploads/2015/08/Beachvolleyball-Berlin-Smart-Magazine-8.jpg", id =count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = "yes", tag_free = "yes", tag_outdoor = "yes", tag_special = "no", tag_learn = "no", tag_date_night = "no")
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Bowl", location = "Zodo's", lat = "34.4406028", lng = "-119.82875519999999", fullName = "Bowl @ Zodo's", image = "http://baligo.co/wp-content/uploads/2015/02/edited3strike.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = "yes", tag_free = "no", tag_outdoor = "no", tag_special = "no", tag_learn = "no", tag_date_night = "yes")
count += 1;
session.add(Activity1)
session.commit()


Activity1 = Activity(name = "Cooking Class", lat = "34.420132", lng = "-119.700534", location = "Tab La Sur", fullName = "Cooking Class @ Tab La Sur", image = "https://thoughtsfromajoy.files.wordpress.com/2012/05/slaytor_j_01.jpg", description = "This week, we are making Paella!", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = "no", tag_free = "no", tag_outdoor = "no", tag_special = "no", tag_learn = "yes", tag_date_night = "yes")
count += 1;
session.add(Activity1)
session.commit()


Activity1 = Activity(name = "Watch a Movie", lat = "34.4245789", lng = "-119.70656459999998", location = "Arlington Theater", fullName = "Watch a Movie @ Arlington Theater", image = "https://pbs.twimg.com/media/CGXAx_KWwAEnDqV.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = "no", tag_free = "no", tag_outdoor = "no", tag_special = "no", tag_learn = "no", tag_date_night = "yes")
count += 1;
session.add(Activity1)
session.commit()

