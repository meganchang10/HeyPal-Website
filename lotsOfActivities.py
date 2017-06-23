from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Activity, Base, Pal, User

engine = create_engine('postgresql://heypal:PASSWORD@localhost/heypal')
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
#User1 = User(name="Megan Chang", email="meganchang10@gmail.com")
#session.add(User1)
#session.commit()

lat = "34.40234809999999"
lng = "-119.69934519999998"
venue_id = "4b12f540f964a5209d9123e3"
Activity1 = Activity(fullName = "Volleyball @ Leadbetter Beach", name = "Volleyball", location = "Leadbetter Beach", lat = lat, lng = lng, venue_id = venue_id, image = "http://www.smart-magazine.com/content/uploads/2015/08/Beachvolleyball-Berlin-Smart-Magazine-8.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = False, tag_over_21= False, tag_after_work = False)
session.add(Activity1)
session.commit()


lat = "34.434987"
lng = "-119.720438"
venue_id = "4c30fa2e3896e21ea05de690"
year = 2017
month = 7
day = 1
hour = 10
minute = 30
Activity1 = Activity(fullName = "Color Run @ State Street", name = "Color Run", location = "State Street", lat = lat, lng = lng, venue_id = venue_id, image = "http://www.thecolorvibe.com/images/color-run-780x400-2A.jpg", datetime = datetime(year, month, day, hour, minute), creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = False, tag_outdoor = True, tag_special = True, tag_learn = False, tag_date_night = False, tag_over_21= False, tag_after_work = False)
session.add(Activity1)
session.commit()


Activity1 = Activity(fullName = "Board Game Night @ Home", name = "Board Game Night", location = "Home", lat = lat, lng = lng, venue_id = venue_id, image = "http://thefederalist.com/wp-content/uploads/2013/12/boardgame.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = False, tag_special = False, tag_learn = False, tag_date_night = False, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "34.4406028"
lng = "-119.82875519999999"
venue_id = "4b19d3ebf964a520f3e423e3"
Activity1 = Activity(fullName = "Bowl @ Zodo's", name = "Bowl", location = "Zodo's", lat = lat, lng = lng, venue_id = venue_id, image = "http://baligo.co/wp-content/uploads/2015/02/edited3strike.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = False, tag_outdoor = False, tag_special = False, tag_learn = False, tag_date_night = True, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "38.782089"
lng = "-104.880013"
venue_id = "4ba65abcf964a5209a4939e3"
Activity1 = Activity(fullName = "Hike @ Seven Falls", name = "Hike", location = "Seven Falls", lat = lat, lng = lng, venue_id = venue_id, image = "http://www.mountainsidenorthstar.com/wp-content/uploads/2015/10/hiking-featured.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = True, tag_over_21= False, tag_after_work = False)
session.add(Activity1)
session.commit()

year = 2017
month = 7
day = 1
just_date = datetime(year, month, day)

hour = 18
minute = 30
second = 0


Activity1 = Activity(fullName = "Book Club @ Barnes & Noble", name = "Book Club", datetime = datetime(year, month, day, hour, minute, second), location = "Barnes and Noble", lat = lat, lng = lng, venue_id = venue_id, image = "http://www.carnegielibrary.org/wp-content/uploads/2017/01/SQH-Cookbook-Club_feature-image.jpg", description = "This month, we will be reading Seabiscuit by Laura Hillenbrand!", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = False, tag_special = False, tag_learn = True, tag_date_night = False, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "34.420132"
lng = "-119.700534"
venue_id = "4b12f540f964a5209d9123e3"
Activity1 = Activity(fullName = "Cooking Class @ Tab La Sur", name = "Cooking Class", location = "Tab La Sur", lat = lat, lng = lng, venue_id = venue_id, image = "https://thoughtsfromajoy.files.wordpress.com/2012/05/slaytor_j_01.jpg", description = "This week, we are making Paella!", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = False, tag_outdoor = False, tag_special = False, tag_learn = True, tag_date_night = True, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "34.4245789"
lng = "-119.70656459999998"
venue_id = "4b368cb0f964a520c43725e3"
Activity1 = Activity(fullName = "Watch Movie @ Arlington Theater", name = "Watch a Movie", location = "Arlington Theater", lat = lat, lng = lng, venue_id = venue_id, image = "https://pbs.twimg.com/media/CGXAx_KWwAEnDqV.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = False, tag_outdoor = False, tag_special = False, tag_learn = False, tag_date_night = True, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "34.412320"
lng = "-119.855228"
venue_id = venue_id
Activity1 = Activity(fullName = "Trivia Night @ Woodstocks", name = "Trivia Night", location = "Woodstocks", lat = lat, lng = lng, venue_id = venue_id, image = "http://cdn.funcheap.com/wp-content/uploads/2014/03/736672_490143327691271_935167735_o1.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = False, tag_special = False, tag_learn = False, tag_date_night = True, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "34.427788"
lng = "-119.874786"
venue_id = "4b09cf4ff964a520011e23e3"
Activity1 = Activity(fullName = "Sample Run @ Costco", name = "Sample Run", location = "Costco", lat = lat, lng = lng, venue_id = venue_id, image = "https://theamericangenius.com/wp-content/uploads/2014/10/costco-samples.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = False, tag_special = False, tag_learn = False, tag_date_night = False, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "34.406830"
lng = "-119.548594"
venue_id = "4ba7e90af964a520ebbd39e3"
Activity1 = Activity(fullName = "Bike @ Padaro Beach", name = "Bike", location = "Padaro Beach", lat = lat, lng = lng, venue_id = venue_id, image = "https://peloponnese.events/wp-content/uploads/2016/02/Bike-ride-photo.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = False, tag_over_21= False, tag_after_work = False)
session.add(Activity1)
session.commit()


##############

lat = "34.406830"
lng = "-119.548594"
venue_id = "4ba7e90af964a520ebbd39e3"
Activity1 = Activity(fullName = "Beach Day @ Padaro Beach",name = "Beach Day", location = "Padaro Beach", lat = lat, lng = lng, venue_id = venue_id, image = "http://cdn.hercampus.com/s3fs-public/2015/05/02/beach-friends2.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = False, tag_over_21= False, tag_after_work = False)
session.add(Activity1)
session.commit()


lat = "34.40234809999999"
lng = "-119.69934519999998"
venue_id = "4b12f540f964a5209d9123e3"
Activity1 = Activity(fullName = "BBQ @ Leadbetter Park", name = "BBQ", location = "Leadbetter Park", lat = lat, lng = lng, venue_id = venue_id, image = "http://www.improvementscatalog.com/RoomForImprovements/wp-content/uploads/2015/05/bbq_party.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = False, tag_outdoor = True, tag_special = True, tag_learn = False, tag_date_night = False, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "34.434987"
lng = "-119.720438"
venue_id = "4c30fa2e3896e21ea05de690"
Activity1 = Activity(fullName = "Farmer's Market @ State Street", name = "Farmer's Market", location = "State Street", lat = lat, lng = lng, venue_id = venue_id, image = "http://l7.alamy.com/zooms/4203bfb0eea1484583544999dbf79f11/people-shopping-at-the-santa-barbara-farmers-market-eaw2y8.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = True, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "34.419097"
lng = "-119.697454"
venue_id = "4af1284bf964a520cae021e3"
Activity1 = Activity(fullName = "Play Pool @ Dargan's", name = "Play Pool", location = "Dargan's", lat = lat, lng = lng, venue_id = venue_id, image = "http://mccluresmagazine.com/wp-content/uploads/2015/05/the-game-bangkok-pool-table-tourists-sportsbar.png", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = False, tag_special = False, tag_learn = True, tag_date_night = False, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "34.409981"
lng = "-119.685586"
venue_id = "4aac6892f964a520dd5d20e3"
Activity1 = Activity(fullName = "Sunset Stroll @ SB Pier", name = "Sunset stroll", location = "SB Pier", lat = lat, lng = lng, venue_id = venue_id, image = "http://patricksmithphotography.com/blog/wp-content/uploads/2015/05/101230-6559-OceansideSurf.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = True, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "34.407901"
lng = "-119.878953"
venue_id = "4aedf7c9f964a520bdd021e3"
Activity1 = Activity(fullName = "Bonfire @ Sands Beach", name = "Bonfire", location = "Sands Beach", lat = lat, lng = lng, venue_id = venue_id, image = "http://www.myabundantlife.org/wp-content/uploads/2016/09/bonfire-marshmallows.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = True, tag_learn = False, tag_date_night = False, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lng = "-119.864723"
venue_id = "4bf851fcb182c9b63c4c775a"
Activity1 = Activity(fullName = "Jump on Rocks @ Lizard's Mouth", name = "Jump on Rocks", location = "Lizard's Mouth", lat = lat, lng = lng, venue_id = venue_id, image = "http://images.summitpost.org/original/578604.JPG", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = False, tag_over_21= False, tag_after_work = False)
session.add(Activity1)
session.commit()


lat = "34.424003"
lng = "-119.702085"
venue_id = "4b3fc68bf964a5207bae25e3"
Activity1 = Activity(fullName = "Be a Tourist @ SB Courthouse", name = "Be a Tourist", location = "SB Courthouse", lat = lat, lng = lng, venue_id = venue_id, image = "http://santabarbaragreetingcards.com/wp-content/uploads/2015/09/sunkengarden2b-ricepapervig-cetrspotnormal-web2.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = True, tag_date_night = False, tag_over_21= False, tag_after_work = False)
session.add(Activity1)
session.commit()


lat = "34.423657"
lng = "-119.889897"
venue_id = "4ea5e5a19a524accd15aea0d"
Activity1 = Activity(fullName = "Look @ Coronado Butterfly Reserve", name = "Look", location = "Coronado Butterfly Reserve", lat = lat, lng = lng, venue_id = venue_id, image = "https://fthmb.tqn.com/ghXwRdOx1ah3hEVa4ycaBUeTILY=/2122x1415/filters:fill(auto,1)/about/GettyImages-513055973-573ba3a05f9b58723dd73854.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = True, tag_over_21= False, tag_after_work = False)
session.add(Activity1)
session.commit()


lng = "-119.714059"
venue_id = "4b2548c3f964a520556f24e3"
Activity1 = Activity(fullName = "Explore @ SB Mission", name = "Explore", location = "SB Mission", lat = lat, lng = lng, venue_id = venue_id, image = "http://www.travelingwithmj.com/wp-content/uploads/2010/11/Mission-Santa-Barbara-also-known-as-Queen-of-the-Missions-for-its-graceful-beauty..jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = True, tag_date_night = True, tag_over_21= False, tag_after_work = False)
session.add(Activity1)
session.commit()


lat = "34.606235"
lng = "-120.176565"
venue_id = "4b2d65def964a520c9d524e3"
Activity1 = Activity(fullName = "Feed Giant Birds @ Ostrich Land", name = "Feed Giant Birds", location = "Ostrich Land", lat = lat, lng = lng, venue_id = venue_id, image = "http://californiathroughmylens.com/wp-content/uploads/2011/10/Ostriches-next-to-bite-sign.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = True, tag_learn = False, tag_date_night = True, tag_over_21= False, tag_after_work = False)
session.add(Activity1)
session.commit()


lat = "34.416834"
lng = "-119.832210"
venue_id = "4a8851dff964a520de0520e3"
Activity1 = Activity(fullName = "Jump off the Pier @ Goleta Beach", name = "Jump off the Pier", location = "Goleta Beach", lat = lat, lng = lng, venue_id = venue_id, image = "http://hanaleiholiday.com/wp-content/uploads/2014/02/boys-pier-jump.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = True, tag_outdoor = True, tag_special = True, tag_learn = False, tag_date_night = False, tag_over_21= False, tag_after_work = False)
session.add(Activity1)
session.commit()


lat = "34.418266"
lng = "-119.848966"
venue_id = "4aeccdc5f964a52059cb21e3"
Activity1 = Activity(fullName = "Tennis @ Rec Cen Courts", name = "Tennis", location = "Rec Cen Courts", lat = lat, lng = lng, venue_id = venue_id, image = "http://i.telegraph.co.uk/multimedia/archive/03077/serena_venus_3077422b.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = True, tag_date_night = False, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "34.418266"
lng = "-119.848966"
venue_id = "4aeccdc5f964a52059cb21e3"
Activity1 = Activity(fullName = "Diving Comp @ UCSB Rec Cen", name = "Diving Comp", location = "UCSB Rec Cen", lat = lat, lng = lng, venue_id = venue_id, image = "https://cdn-s3.si.com/s3fs-public/si/dam/assets/13/07/30/130730105748-belly-flop-ap04031704055-single-image-cut.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = True, tag_free = True, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = False, tag_over_21= False, tag_after_work = False)
session.add(Activity1)
session.commit()


lat = "34.4099896"
lng = "-119.6855694999"
venue_id = "4e220b75fa761d671082ff1b"
Activity1 = Activity(fullName = "Wine Tasting @ Deep Sea Tasting Room", name = "Wine Tasting", location = "Deep Sea", lat = lat, lng = lng, venue_id = venue_id, image = "https://media-cdn.tripadvisor.com/media/photo-s/07/8b/79/e7/another-great-shot.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = False, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = True, tag_over_21= True, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "34.4225655999"
lng = "-119.7054617999"
venue_id = "4b51496af964a520d64927e3"
Activity1 = Activity(fullName = "Appetizers @ Milk & Honey", name = "Appetizers", location = "Milk & Honey", lat = lat, lng = lng, venue_id = venue_id, image = "http://urbandiningguide.com/wp-content/uploads/2015/11/milkhoneysantabarbara.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = False, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = True, tag_over_21= False, tag_after_work = True)
session.add(Activity1)
session.commit()


lat = "34.4099896"
lng = "-119.6855694999"
venue_id = "4e220b75fa761d671082ff1b"
Activity1 = Activity(fullName = "Dancing @ O'Malley's", name = "Dancing", location = "O'Malley's", lat = lat, lng = lng, venue_id = venue_id, image = "http://www.retale.com/blog/shared/content/uploads/2016/02/dive-bar-3.jpg", creator =1, log_views = 0, adds_to_myActivities = 0, tag_sporty = False, tag_free = False, tag_outdoor = True, tag_special = False, tag_learn = False, tag_date_night = True, tag_over_21= True, tag_after_work = True)
session.add(Activity1)
session.commit()


print "added lots of cool activities!"
