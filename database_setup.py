from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250), default="http://donatered-asset.s3.amazonaws.com/assets/default/default_user-884fcb1a70325256218e78500533affb.jpg")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Activity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    image = Column(String)
    location = Column(String(250))
    fullName = Column(String)
    venue_id = Column(String)
    lat = Column(Float, default=34.40234809999999)
    lng = Column(Float, default=-119.69934519999998)
    log_views = Column(Integer, default=0)
    adds_to_myActivities = Column(Integer, default=0)
    datetime = Column(DateTime)

    creator = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # tags
    tag_free = Column(Boolean, default=False)
    tag_sporty = Column(Boolean, default=False)
    tag_outdoor = Column(Boolean, default=False)
    tag_special = Column(Boolean, default=False)
    tag_learn = Column(Boolean, default=False)
    tag_date_night = Column(Boolean, default=False)
    tag_over_21 = Column(Boolean, default=False)
    tag_after_work = Column(Boolean, default=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'fullName': self.fullName,
            'image': self.image,
            'location': self.location,
            'lat': self.lat,
            'lng': self.lng,
            'datetime': self.datetime,
            'log_views': self.log_views,
            'adds_to_myActivities': self.adds_to_myActivities,
            'creator': self.creator,
            'tag_free': self.tag_free,
            'tag_sporty': self.tag_sporty,
            'tag_outdoor': self.tag_outdoor,
            'tag_special': self.tag_special,
            'tag_learn': self.tag_learn,
            'tag_date_night': self.tag_date_night,
            'tag_over_21': self.tag_over_21,
            'tag_after_work': self.tag_after_work,
            'venue_id': self.venue_id
        }


class Pal(Base):
    __tablename__ = 'pal'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    pal_id = Column(Integer, ForeignKey('user.id'))
    image = Column(String(250))

    user = relationship(User, foreign_keys=[user_id])
    pal = relationship(User, foreign_keys=[pal_id])

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pal_id': self.pal_id,
            'name': self.name
        }


class Invite(Base):
    __tablename__ = 'invite'

    id = Column(Integer, primary_key=True)
    message = Column(String())
    invite_key = Column(String())

    host = Column(Integer, ForeignKey('user.id'))
    guest = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, foreign_keys=[host])
    pal = relationship(User, foreign_keys=[guest])

    name = Column(String(80), nullable=False)
    description = Column(String(250))
    image = Column(String)
    location = Column(String(250))
    datetime = Column(DateTime)

    # tags
    tag_free = Column(Boolean, default=False)
    tag_sporty = Column(Boolean, default=False)
    tag_outdoor = Column(Boolean, default=False)
    tag_special = Column(Boolean, default=False)
    tag_learn = Column(Boolean, default=False)
    tag_date_night = Column(Boolean, default=False)
    tag_over_21 = Column(Boolean, default=False)
    tag_after_work = Column(Boolean, default=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'host': self.host,
            'guest': self.guest,
            'invite_key': self.invite_key,
            'message': self.message,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'location': self.location,
            'datetime': self.datetime,
            'tag_free': self.tag_free,
            'tag_sporty': self.tag_sporty,
            'tag_outdoor': self.tag_outdoor,
            'tag_special': self.tag_special,
            'tag_learn': self.tag_learn,
            'tag_date_night': self.tag_date_night,
            'tag_over_21': self.tag_over_21,
            'tag_after_work': self.tag_after_work,
            }


# Connect to Database and create database session
# Originally used sqlite
# engine = create_engine('sqlite:///heypal.db')
# For the live website, use postgresql
# This line must be changed in 4 files: database_setup.py, project.py or __init__.py, lotsOfA.py and filterSearchResults.py and login_handler.py
engine = create_engine('postgresql://heypal:PASSWORD@localhost/heypal')

Base.metadata.create_all(engine)












