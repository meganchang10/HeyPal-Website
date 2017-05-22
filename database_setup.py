from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Activity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    image = Column(String)
    location = Column(String(250))
    log_views = Column(Integer)
    adds_to_myActivities = Column(Integer)
    # date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # tags
    tag_free = Column(String(3))
    tag_sporty = Column(String(3))
    tag_outdoor = Column(String(3))
    tag_special = Column(String(3))
    tag_learn = Column(String(3))
    tag_date_night = Column(String(3))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'location': self.location,
            'log_views': self.log_views,
            'adds_to_myActivities': self.adds_to_myActivities,
            'user_id': self.user_id,
            'tag_free': self.tag_free,
            'tag_sporty': self.tag_sporty,
            'tag_outdoor': self.tag_outdoor,
            'tag_special': self.tag_special,
            'tag_learn': self.tag_learn,
            'tag_date_night': self.tag_date_night,
        }


class MyActivity(Base):
    __tablename__ = 'myActivity'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    image = Column(String)
    location = Column(String(250))
    # TODO date = Column(DateTime, default=datetime.datetime.utcnow)
    adds_to_myActivities = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # tags
    tag_free = Column(String(3))
    tag_sporty = Column(String(3))
    tag_outdoor = Column(String(3))
    tag_special = Column(String(3))
    tag_learn = Column(String(3))
    tag_date_night = Column(String(3))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'location': self.location,
            'adds_to_myActivities': self.adds_to_myActivities,
            'user_id': self.user_id,
            'tag_free': self.tag_free,
            'tag_sporty': self.tag_sporty,
            'tag_outdoor': self.tag_outdoor,
            'tag_special': self.tag_special,
            'tag_learn': self.tag_learn,
            'tag_date_night': self.tag_date_night,
            }


class Pal(Base):
    __tablename__ = 'pal'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    myActivity_id = Column(Integer, ForeignKey('myActivity.id'))
    myActivity = relationship(MyActivity)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


engine = create_engine('sqlite:///heypal.db')
Base.metadata.create_all(engine)
