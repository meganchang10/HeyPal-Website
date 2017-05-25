#!/usr/bin/python

from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Activity, Pal, User, MyActivity, Invite
from flask import session as login_session
import random
import string
import json
from functools import wraps
from datetime import datetime

import login_handler
import logout_handler
import activity_handler
import filterSearchResults
import checkBox


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Hey Pal"


# Connect to Database and create database session
engine = create_engine('sqlite:///heypal.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
session1 = session


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "username" not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return wrapper


def clearance_level_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "username" not in login_session:
            return redirect('/login')
        if login_session['user_id'] != 1:
            flash("Only Authorized Users Can Access That Page")
            return redirect("/")
        return f(*args, **kwargs)
    return wrapper


# Show all activities
@app.route('/')
@app.route('/activities')
@app.route('/heypal/activities/')
@app.route('/heypal/', methods=["GET", "POST"])
def showActivities():
    activities = session.query(
        Activity).order_by(Activity.log_views.desc()).all()
    tags = ["All Activities", "Free Activities", "Get Active", "Get Outdoors",
            "Rainy Day", "Special Occasions", "Better Yourself", "Date Night"]

    if request.method == "POST":
        # Check for filters
        filter_results = request.form.get('filter_results')
        activities = filterSearchResults.activities(filter_results)
        return render_template(
            'activities.html', activities=activities, tags=tags,
            title=filter_results)

    else:
        return render_template(
                'activities.html', activities=activities, tags=tags,
                title="All Activities")


@app.route('/heypal/<int:activity_id>/activity')
def showActivity(activity_id):
    activity = session.query(Activity).filter_by(id=activity_id).one()
    activity.log_views += 1
    session.add(activity)
    session.commit()
    return render_template('activity.html', current=activity)


# Create a new activity
@app.route('/heypal/new', methods=["GET", "POST"])
@clearance_level_required
def newActivity():
    if request.method == "POST":
        newActivity = activity_handler.createActivity(request)
        session.add(newActivity)
        session.commit()
        return redirect(url_for('showActivities', title="All Activities"))
    else:
        return render_template("newActivity.html")


@app.route('/heypal/<int:activity_id>/edit/', methods=["GET", "POST"])
@clearance_level_required
def editActivity(activity_id):
    editActivity = session.query(Activity).filter_by(id=activity_id).one()
    if request.method == "POST":
        editActivity = activity_handler.performEdit(request, editActivity)
        session.add(editActivity)
        session.commit()
        return redirect(url_for('showActivities', title="All Activities"))
    else:
        return render_template('editActivity.html', current=editActivity)


@app.route('/heypal/<int:activity_id>/delete/', methods=["GET", "POST"])
@clearance_level_required
def deleteActivity(activity_id):
    deleteActivity = session.query(Activity).filter_by(id=activity_id).one()
    if request.method == "POST":
        session.delete(deleteActivity)
        session.commit()
        flash("Activity Successfully Deleted: %s" % deleteActivity.name)
        return redirect(url_for('showActivities', title="All Activities"))
    else:
        return render_template("deleteActivity.html", current=deleteActivity)


###############################################################################
# My Activities

# I use a double redirect to view myActivities because it requires user_id
@app.route('/heypal/myActivities')
@login_required
def showMyActivitiesRedirect():
    user_id = login_session['user_id']
    return redirect(url_for(
        'showMyActivities', user_id=user_id, title="My Activities"))


@app.route('/heypal/<int:user_id>/myActivities', methods=["GET", "POST"])
@login_required
def showMyActivities(user_id):
    # Authorization required
    if login_session['user_id'] != user_id:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    myActivities = session.query(MyActivity).filter_by(user_id=user_id).all()
    tags = ["My Activities", "Free Activities", "Get Active", "Get Outdoors",
            "Rainy Day", "Special Occasions", "Better Yourself", "Date Night"]

    if request.method == "POST":
        filter_results = request.form.get('filter_results')
        myActivities = filterSearchResults.myActivities(filter_results, user_id)
        return render_template(
            "myActivities.html", myActivities=myActivities, tags=tags,
            user_id=user_id, title=filter_results)
    else:
        return render_template(
            "myActivities.html", myActivities=myActivities, tags=tags,
            user_id=user_id, title="My Activities")


@app.route('/heypal/<int:user_id>/<int:myActivity_id>/myActivity')
@login_required
def showMyActivity(myActivity_id, user_id):
    # Authorization required
    if login_session['user_id'] != user_id:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    activity = session.query(MyActivity).filter_by(id=myActivity_id).one()
    return render_template(
        'myActivity.html', user_id=user_id, current=activity)


@app.route(
    '/heypal/<int:activity_id>/addToMyActivities/', methods=["POST"])
@login_required
def addToMyActivities(activity_id):
    if request.method == "POST":
        activity = session.query(Activity).filter_by(id=activity_id).one()
        activity.adds_to_myActivities += 1
        session.add(activity)
        session.commit()

        myNewActivity = activity_handler.addToMy(activity)
        session.add(myNewActivity)
        session.commit()

        return redirect(url_for('showActivities', title="All Activities"))


@app.route('/heypal/<int:user_id>/new', methods=["GET", "POST"])
@login_required
def newMyActivity(user_id):
    # Authorization required
    if login_session['user_id'] != user_id:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    if request.method == "POST":
        newMyActivity = activity_handler.createActivity(request)
        session.add(newMyActivity)
        session.commit()
        return redirect(url_for(
            'showMyActivities', user_id=user_id, title="My Activities"))
    else:
        return render_template("newActivity.html")


@app.route(
    '/heypal/<int:user_id>/<int:myActivity_id>/edit/', methods=["GET", "POST"])
@login_required
def editMyActivity(myActivity_id, user_id):
    # Authorization required
    if login_session['user_id'] != user_id:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    editActivity = session.query(MyActivity).filter_by(
        id=myActivity_id).one()

    if request.method == "POST":
        editActivity = activity_handler.performEdit(request, editActivity)
        session.add(editActivity)
        session.commit()
        return redirect(url_for(
            'showMyActivities', user_id=user_id, title="My Activities"))
    else:
        return render_template(
            'editActivity.html', current=editActivity)


@app.route(
    '/heypal/<int:user_id>/<int:myActivity_id>/delete/',
    methods=["GET", "POST"])
def deleteMyActivity(myActivity_id, user_id):
    # Authorization required
    if login_session['user_id'] != user_id:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")

    deleteActivity = session.query(MyActivity).filter_by(
        id=myActivity_id).one()

    if request.method == "POST":
        session.delete(deleteActivity)
        session.commit()
        flash("Activity Successfully Deleted: %s" % deleteActivity.name)
        return redirect(url_for(
            'showMyActivities', user_id=user_id, title="My Activities"))
    else:
        return render_template(
            "deleteActivity.html", current=deleteActivity)


###############################################################################
###############################################################################
@app.route('/heypal/myInvites')
@login_required
def invitesRedirect():
    user_id = login_session['user_id']
    return redirect(url_for(
        'showMyInvites', user_id=user_id))


@app.route('/heypal/<int:user_id>/myInvites', methods=["GET", "POST"])
@login_required
def showMyInvites(user_id):
    myInvites = session.query(Invite).filter_by(guest=user_id).all()
    if request.method == "GET":
        return render_template(
            "myInvites.html", myInvites=myInvites)


@app.route('/heypal/<int:user_id>/<string:invite_key>/invite')
@login_required
def showMyInvite(invite_key, user_id):
    invites = session.query(Invite).filter_by(invite_key=invite_key).all()
    guest_IDs = []
    for invite in invites:
        guest_IDs.append(invite.guest)
    guests = session.query(User).filter(User.id.in_(guest_IDs))
    invite = session.query(Invite).filter_by(invite_key=invite_key).first()
    host = session.query(User).filter_by(id=invite.host).one()
    print(guests)
    return render_template('invite.html', current=invite, user_id=user_id, pals=guests, host=host)


@app.route(
    '/heypal/<int:user_id>/<int:myActivity_id>/sendInvite/',
    methods=["GET", "POST"])
def sendInvite(user_id, myActivity_id):
    activity = session.query(MyActivity).filter_by(id=myActivity_id).one()
    if request.method == "POST":
        pals = session.query(Pal).filter_by(user_id=user_id).all()
        invite_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for x in xrange(20))

        for pal in pals:
            ans = request.form.get(pal.name)
            if ans == "yes":
                createInvite(activity, request, pal.pal_id, invite_key, default_message)

        flash("Invitations have been sent!")
        return redirect(url_for(
            'showMyActivities', user_id=user_id, title="My Activities"))
    else:
        pals = session.query(Pal).filter_by(user_id=user_id).all()
        return render_template(
            'sendInvite.html', current=activity, user_id=user_id, pals=pals)


def createInvite(activity, request, guest_id, invite_key, default_message):
    [tag_free, tag_sporty, tag_outdoor, tag_special, tag_learn,
     tag_date_night] = checkBox.checkTags(request)

    newInvite = Invite(
        host=login_session['user_id'],
        guest=guest_id,
        invite_key=invite_kemy,
        tag_free=tag_free,
        tag_sporty=tag_sporty,
        tag_outdoor=tag_outdoor,
        tag_special=tag_special,
        tag_learn=tag_learn,
        tag_date_night=tag_date_night,
        )

    newInvite.name = activity.name
    newInvite.image = activity.image
    newInvite.location = activity.location
    newInvite.description = activity.description

    newInvite.message = default_message

    if request.form['name']:
        newInvite.name = request.form['name']
    if request.form['image']:
        newInvite.image = request.form['image']
    if request.form['location']:
        newInvite.location = request.form['location']
    if request.form['message']:
        newInvite.message = request.form['message']
    if request.form['description']:
        newInvite.message = request.form['description']

    print("Invite Added!")
    session.add(newInvite)
    session.commit()
    return newInvite


def calendarify(request):
    year = request.form.get('year')
    month = request.form.get('month')
    day = request.form.get('day')
    hour = request.form.get('hour')
    minute = request.form.get('minute')
    second = request.form.get('second')

    result = datetime(year, month, day, hour, minute, second)



# JSON functions
###############################################################################

@app.route('/heypal/activity/<int:activity_id>/JSON')
def activityJSON(activity_id):
    activity = session.query(Activity).filter_by(id=activity_id).one()
    return jsonify(Activity=activity.serialize)


@app.route('/heypal/activities/JSON')
def activitiesJSON():
    activities = session.query(Activity).all()
    return jsonify(All_Activities=[a.serialize for a in activities])


@app.route('/heypal/myActivity/<int:myActivity_id>/JSON')
def myActivityJSON(myActivity_id):
    myActivity = session.query(MyActivity).filter_by(id=myActivity_id).one()
    return jsonify(Activity=myActivity.serialize)


@app.route('/heypal/myActivities/JSON')
def myActivitiesJSON():
    myActivities = session.query(MyActivity).all()
    return jsonify(All_My_Activities=[a.serialize for a in myActivities])


@app.route('/heypal/pals/JSON')
def palsJSON():
    pals = session.query(Pal).all()
    return jsonify(All_Pals=[a.serialize for a in pals])


@app.route('/heypal/invites/JSON')
def invitesJSON():
    invites = session.query(Invite).all()
    return jsonify(All_Invites=[a.serialize for a in invites])



# Login/Logout functions
###############################################################################

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbLogin():
    output = login_handler.fbconnect()
    return output


@app.route('/gconnect', methods=['POST'])
def googleLogin():
    output = login_handler.gconnect()
    return output


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            logout_handler.gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            logout_handler.fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showActivities', title="All Activities"))
    else:
        flash("You were not logged in")
        return redirect(url_for('showActivities', title="All Activities"))


@app.route('/fbdisconnect')
def fbLogout():
    output = logout_handler.fbdisconnect()
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def googleLogout():
    output = logout_handler.gdisconnect()
    return output


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
