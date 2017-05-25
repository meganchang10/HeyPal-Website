from database_setup import Base, Activity, MyActivity
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///heypal.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def activities(filter_results):
    if filter_results == "All Activities":
        activities = session.query(
            Activity).order_by(Activity.log_views.desc())
    elif filter_results == "Free Activities":
        activities = session.query(
            Activity).filter_by(tag_free="yes").order_by(
            Activity.log_views.desc()).all()
    elif filter_results == "Get Active":
        activities = session.query(
            Activity).filter_by(tag_sporty="yes").order_by(
            Activity.log_views.desc()).all()
    elif filter_results == "Get Outdoors":
        activities = session.query(
            Activity).filter_by(tag_outdoor="yes").order_by(
            Activity.log_views.desc()).all()
    elif filter_results == "Rainy Day":
        activities = session.query(
            Activity).filter_by(tag_outdoor="no").order_by(
            Activity.log_views.desc()).all()
    elif filter_results == "Special Occasions":
        activities = session.query(
            Activity).filter_by(tag_special="yes").order_by(
            Activity.log_views.desc()).all()
    elif filter_results == "Better Yourself":
        activities = session.query(
            Activity).filter_by(tag_learn="yes").order_by(
            Activity.log_views.desc()).all()
    elif filter_results == "Date Night":
        activities = session.query(
            Activity).filter_by(tag_date_night="yes").order_by(
            Activity.log_views.desc()).all()
    return activities


def myActivities(filter_results, user_id):
    if filter_results == "My Activities":
        myActivities = session.query(
            MyActivity).filter_by(user_id=user_id).all()
    elif filter_results == "Free Activities":
        myActivities = session.query(
            MyActivity).filter_by(tag_free="yes", user_id=user_id)
    elif filter_results == "Get Active":
        myActivities = session.query(
            MyActivity).filter_by(tag_sporty="yes", user_id=user_id)
    elif filter_results == "Get Outdoors":
        myActivities = session.query(
            MyActivity).filter_by(tag_outdoor="yes", user_id=user_id)
    elif filter_results == "Rainy Day":
        myActivities = session.query(
            MyActivity).filter_by(tag_outdoor="no", user_id=user_id)
    elif filter_results == "Special Occasions":
        myActivities = session.query(
            MyActivity).filter_by(tag_special="yes", user_id=user_id)
    elif filter_results == "Better Yourself":
        myActivities = session.query(
            MyActivity).filter_by(tag_learn="yes", user_id=user_id)
    elif filter_results == "Date Night":
        myActivities = session.query(
            MyActivity).filter_by(tag_date_night="yes", user_id=user_id)
    return myActivities
