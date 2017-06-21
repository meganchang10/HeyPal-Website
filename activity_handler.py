from database_setup import Base, Activity
from flask import session as login_session
from flask import flash
import string
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Connect to Database and create database session

import checkBox


# General functions (can be used for activity and myActivity)
def performEdit(request, editActivity):
    if request.form['name']:
        editActivity.name = request.form['name']
    if request.form['image']:
        editActivity.image = request.form['image']
    if request.form['location']:
        editActivity.location = request.form['location']
    if request.form['venue_id']:
        editActivity.venue_id = request.form['venue_id']

    # datetime info
    datetime = checkBox.checkDateTime(editActivity, request)
    editActivity.datetime = datetime

    [tag_free, tag_sporty, tag_outdoor, tag_special, tag_learn,
     tag_date_night, tag_over_21, tag_after_work] = checkBox.checkTags(request)

    editActivity.tag_free = tag_free
    editActivity.tag_sporty = tag_sporty
    editActivity.tag_outdoor = tag_outdoor
    editActivity.tag_special = tag_special
    editActivity.tag_learn = tag_learn
    editActivity.tag_date_night = tag_date_night
    editActivity.tag_over_21 = tag_over_21
    editActivity.tag_after_work = tag_after_work

    flash("Activity Successfully Edited: %s" % editActivity.name)
    return editActivity


def createActivity(request, new_id):

    [tag_free, tag_sporty, tag_outdoor, tag_special, tag_learn,
     tag_date_night, tag_over_21, tag_after_work] = checkBox.checkTags(request)

    newActivity = Activity(
        id=new_id,
        name=request.form['name'],
        location=request.form['location'],
        venue_id=request.form['venue_id'],
        image=request.form['image'],
        description=request.form['description'],
        creator=login_session['user_id'],
        tag_free=tag_free,
        tag_sporty=tag_sporty,
        tag_outdoor=tag_outdoor,
        tag_special=tag_special,
        tag_learn=tag_learn,
        tag_date_night=tag_date_night,
        tag_over_21=tag_over_21,
        tag_after_work=tag_after_work,
        )

    datetime = checkBox.checkDateTime(newActivity, request)
    newActivity.datetime = datetime

    flash("New Activity Successfully Created: %s" % newActivity.name)
    return newActivity


def addToMy(activity, new_id):
    myNewActivity = Activity(
        id=new_id,
        name=activity.name,
        fullName=activity.fullName,
        location=activity.location,
        lat=activity.lat,
        lng=activity.lng,
        venue_id=activity.venue_id,
        datetime=activity.datetime,
        image=activity.image,
        description=activity.description,
        creator=login_session['user_id'],
        tag_free=activity.tag_free,
        tag_sporty=activity.tag_sporty,
        tag_outdoor=activity.tag_outdoor,
        tag_special=activity.tag_special,
        tag_learn=activity.tag_learn,
        tag_date_night=activity.tag_date_night,
        tag_over_21=activity.tag_over_21,
        tag_after_work=activity.tag_after_work,
        )

    flash("%s Successfully Added to My Activities" % myNewActivity.name)

    return myNewActivity
