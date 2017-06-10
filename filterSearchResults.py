from database_setup import Base, Activity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///heypal.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def activities(filter_results, user_id):
    if filter_results == "My Activities":
        activities = session.query(
            Activity).filter_by(creator=user_id).all()
    elif filter_results == "All Activities":
        activities = session.query(
            Activity).filter_by(creator=1).all()
    elif filter_results == "Free Activities":
        activities = session.query(
            Activity).filter_by(tag_free=True, creator=user_id)
    elif filter_results == "Get Active":
        activities = session.query(
            Activity).filter_by(tag_sporty=True, creator=user_id)
    elif filter_results == "Get Outdoors":
        activities = session.query(
            Activity).filter_by(tag_outdoor=True, creator=user_id)
    elif filter_results == "Rainy Day":
        activities = session.query(
            Activity).filter_by(tag_outdoor=False, creator=user_id)
    elif filter_results == "Special Occasions":
        activities = session.query(
            Activity).filter_by(tag_special=True, creator=user_id)
    elif filter_results == "Better Yourself":
        activities = session.query(
            Activity).filter_by(tag_learn=True, creator=user_id)
    elif filter_results == "Date Night":
        activities = session.query(
            Activity).filter_by(tag_date_night=True, creator=user_id)
    elif filter_results == "Over 21 Only":
        activities = session.query(
            Activity).filter_by(tag_over_21=True, creator=user_id)
    elif filter_results == "After Work":
        activities = session.query(
            Activity).filter_by(tag_after_work=True, creator=user_id)
    return activities
