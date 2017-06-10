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
Activity1 = Activity(name = "Volleyball", location = "Leadbetter Beach", image = "http://www.smart-magazine.com/content/uploads/2015/08/Beachvolleyball-Berlin-Smart-Magazine-8.jpg", id =count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()


Activity1 = Activity(name = "Color Run", location = "State Street", image = "http://www.thecolorvibe.com/images/color-run-780x400-2A.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = False, tag_outdoor = True, tag_special = True, tag_learn = False, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Board Game Night", location = "Home", image = "http://thefederalist.com/wp-content/uploads/2013/12/boardgame.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = False, tag_special = False, tag_learn = False, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Bowl", location = "Zodo's", image = "http://baligo.co/wp-content/uploads/2015/02/edited3strike.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = False, tag_outdoor = False, tag_special = False, tag_learn = False, tag_date_night = True)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Hike", location = "Seven Falls", image = "http://www.mountainsidenorthstar.com/wp-content/uploads/2015/10/hiking-featured.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = True)
count += 1;
session.add(Activity1)
session.commit()

year = 2017
month = 7
day = 1
just_date = datetime(year, month, day)

hour = 18
minute = 30
second = 0

Activity1 = Activity(name = "Book Club", datetime = datetime(year, month, day, hour, minute, second), location = "Barnes and Noble", image = "http://www.carnegielibrary.org/wp-content/uploads/2017/01/SQH-Cookbook-Club_feature-image.jpg", description = "This month, we will be reading Seabiscuit by Laura Hillenbrand!", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = False, tag_special = False, tag_learn = True, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()


Activity1 = Activity(name = "Cooking Class", location = "Tab Le Sur", image = "https://thoughtsfromajoy.files.wordpress.com/2012/05/slaytor_j_01.jpg", description = "This week, we are making Paella!", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = False, tag_outdoor = False, tag_special = False, tag_learn = True, tag_date_night = True)
count += 1;
session.add(Activity1)
session.commit()


Activity1 = Activity(name = "Watch a Movie", location = "Arlington Theater", image = "https://pbs.twimg.com/media/CGXAx_KWwAEnDqV.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = False, tag_outdoor = False, tag_special = False, tag_learn = False, tag_date_night = True)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Trivia Night", location = "Woodstocks", image = "http://cdn.funcheap.com/wp-content/uploads/2014/03/736672_490143327691271_935167735_o1.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = False, tag_special = False, tag_learn = False, tag_date_night = True)
count += 1;
session.add(Activity1)
session.commit()


Activity1 = Activity(name = "Ice Skating", location = "Ice in Paradise", image = "https://img.grouponcdn.com/deal/2BemYPCAHjBjvHTpBpGV/2u-2048x1229/v1/c700x420.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = False, tag_outdoor = False, tag_special = False, tag_learn = False, tag_date_night = True)
count += 1;
session.add(Activity1)
session.commit()


Activity1 = Activity(name = "Sample Run", location = "Costco", image = "https://theamericangenius.com/wp-content/uploads/2014/10/costco-samples.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0,        tag_sporty = False, tag_free = True, tag_outdoor = False, tag_special = False, tag_learn = False, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()



Activity1 = Activity(name = "Tennis", location = "Rec Cen Courts", image = "http://i.telegraph.co.uk/multimedia/archive/03077/serena_venus_3077422b.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = True, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()


Activity1 = Activity(name = "Bike", location = "Padaro Beach", image = "https://peloponnese.events/wp-content/uploads/2016/02/Bike-ride-photo.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()


##############

Activity1 = Activity(name = "Beach Day", location = "Padaro Beach", image = "http://cdn.hercampus.com/s3fs-public/2015/05/02/beach-friends2.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "BBQ", location = "Leadbetter Park", image = "http://www.improvementscatalog.com/RoomForImprovements/wp-content/uploads/2015/05/bbq_party.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = False, tag_outdoor = True, tag_special = True, tag_learn = False, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Farmer's Market", location = "State Street", image = "http://l7.alamy.com/zooms/4203bfb0eea1484583544999dbf79f11/people-shopping-at-the-santa-barbara-farmers-market-eaw2y8.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = True)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Play Pool", location = "Dargan's", image = "http://mccluresmagazine.com/wp-content/uploads/2015/05/the-game-bangkok-pool-table-tourists-sportsbar.png", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = False, tag_special = False, tag_learn = True, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Diving Competition", location = "UCSB Rec Cen", image = "http://image1.masterfile.com/getImage/NjIzLTAyMjg3NzkwZW4uMDAwMDAwMDA=AH-KAI/623-02287790en_Masterfile.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Sunset stroll", location = "SB Pier", image = "http://patricksmithphotography.com/blog/wp-content/uploads/2015/05/101230-6559-OceansideSurf.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = True)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Bonfire", location = "Sands Beach", image = "http://www.myabundantlife.org/wp-content/uploads/2016/09/bonfire-marshmallows.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = True, tag_learn = False, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Jump on Rocks", location = "Lizard's Mouth", image = "http://images.summitpost.org/original/578604.JPG", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Be a Tourist", location = "SB Courthouse", image = "http://santabarbaragreetingcards.com/wp-content/uploads/2015/09/sunkengarden2b-ricepapervig-cetrspotnormal-web2.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = True, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Look", location = "Coronado Butterfly Reserve", image = "https://fthmb.tqn.com/ghXwRdOx1ah3hEVa4ycaBUeTILY=/2122x1415/filters:fill(auto,1)/about/GettyImages-513055973-573ba3a05f9b58723dd73854.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = True)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Explore", location = "SB Mission", image = "http://www.travelingwithmj.com/wp-content/uploads/2010/11/Mission-Santa-Barbara-also-known-as-Queen-of-the-Missions-for-its-graceful-beauty..jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = True, tag_date_night = True)
count += 1;
session.add(Activity1)
session.commit()

Activity1 = Activity(name = "Feed Giant Birds", location = "Ostrich Land", image = "http://californiathroughmylens.com/wp-content/uploads/2011/10/Ostriches-next-to-bite-sign.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = True, tag_learn = False, tag_date_night = True)
count += 1;
session.add(Activity1)
session.commit()


Activity1 = Activity(name = "Jump off the Pier", location = "Goleta Beach", image = "http://hanaleiholiday.com/wp-content/uploads/2014/02/boys-pier-jump.jpg", id = count, creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = True, tag_learn = False, tag_date_night = False)
count += 1;
session.add(Activity1)
session.commit()



print "added lots of cool activities!"
