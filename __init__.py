#!/usr/bin/python

from flask import Flask, render_template, request, redirect, jsonify, json
from flask import url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from database_setup import Base, Activity, Pal, User, Invite
from flask import session as login_session
import random
import string
import json
from functools import wraps
from datetime import datetime

import login_handler
import logout_handler
import activity_handler
import invite_handler
import filterSearchResults


app = Flask(__name__)

# Must use relative path for LIVE website
# This change must be implemented in 2 files: project.py or __init__.py and login_handler
# Original format:
#CLIENT_ID = json.loads(
#    open('client_secrets.json', 'r').read())['web']['client_id']

CLIENT_ID = json.loads(
    open('/var/www/HeyPal/heypal/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Hey Pal"


# Connect to Database and create database session
engine = create_engine('postgresql://heypal:PASSWORD@localhost/heypal')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
session1 = session

# These wrapper functions allow us to quickly check the authentication of users
def login_required(f):
    '''Wrapper function to redirect users to login page if necessary'''
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "username" not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return wrapper


def clearance_level_required(f):
    '''Wrapper function to alert users if they are trying to access restricted
     area'''
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
@app.route('/', methods=["GET", "POST"])
@app.route('/heypal/', methods=["GET", "POST"])
def showActivities():
    '''Performs a search query that returns all available public activities
    (ones created by user 1)'''

    activities = session.query(
        Activity).filter_by(creator=1).order_by(
        Activity.log_views.desc()).all()

    # These tags allow users to perform searches that filter results based on
    # what sort of activity they are looking for
    tags = ["All Activities", "Free Activities", "Get Active", "Get Outdoors",
            "Rainy Day", "Special Occasions", "Better Yourself", "Date Night",
            "Over 21 Only", "After Work"]

    if request.method == "POST":
        # Check for filters
        filter_results = request.form.get('filter_results')
        activities = filterSearchResults.activities(
            filter_results, user_id=1)
        return render_template(
            'publicActivities.html', activities=activities, tags=tags,
            title=filter_results)
    else:
        if "username" in login_session and login_session['user_id'] == 1:
            return render_template(
                'activities.html', activities=activities, tags=tags,
                title="All Activities")
        else:
            return render_template(
                'publicActivities.html', activities=activities, tags=tags,
                title="All Activities")


@app.route('/heypal/<int:activity_id>/activity')
def showActivity(activity_id):
    '''Users can view a single activity entry to get more information'''
    activity = session.query(Activity).filter_by(id=activity_id).one()
    activity.log_views += 1
    session.add(activity)
    session.commit()
    if "username" in login_session and login_session['user_id'] == 1:
        return render_template('activity.html', current=activity)
    else:
        return render_template('publicActivity.html', current=activity)


# Create a new activity
@app.route('/heypal/new', methods=["GET", "POST"])
@login_required
@clearance_level_required
def newActivity():
    '''Authorized users can create new public activities for the main page'''
    if request.method == "POST":
        new_id = session.query(func.max(Activity.id)) + 1
        newActivity = activity_handler.createActivity(request, new_id)
        session.add(newActivity)
        session.commit()
        return redirect(url_for('showActivities', title="All Activities"))
    else:
        return render_template("newActivity.html")


@app.route('/heypal/<int:activity_id>/edit/', methods=["GET", "POST"])
@clearance_level_required
def editActivity(activity_id):
    '''Authorized users can edit public activities to update the title,
    location, image, description, etc.'''
    editActivity = session.query(Activity).filter_by(id=activity_id).one()
    creator = editActivity.creator
    if login_session['user_id'] != creator:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
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
    '''Authorized users can delete public activity entries on the main page'''
    deleteActivity = session.query(Activity).filter_by(id=activity_id).one()
    if request.method == "POST":
        session.delete(deleteActivity)
        session.commit()
        flash("Activity Successfully Deleted: %s" % deleteActivity.name)
        return redirect(url_for('showActivities', title="All Activities"))
    else:
        return render_template("deleteActivity.html", current=deleteActivity)


###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################

# My Activities
@app.route('/heypal/myActivities')
@login_required
def showMyActivitiesRedirect():
    '''Redirect to My Activities page'''
    user_id = login_session['user_id']
    return redirect(url_for(
        'showMyActivities', creator=user_id, title="My Activities"))


@app.route('/heypal/<int:creator>/myActivities', methods=["GET", "POST"])
@login_required
def showMyActivities(creator):
    '''Users can see the activities they added. They can review a catalog of
    all the activities they showed interest in'''
    # Authorization required
    if login_session['user_id'] != creator:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    myActivities = session.query(Activity).filter_by(creator=creator).all()
    tags = ["My Activities", "Free Activities", "Get Active", "Get Outdoors",
            "Rainy Day", "Special Occasions", "Better Yourself", "Date Night",
            "Over 21 Only", "After Work"]

    if request.method == "POST":
        filter_results = request.form.get('filter_results')
        myActivities = filterSearchResults.activities(filter_results, creator)
        return render_template(
            "myActivities.html", myActivities=myActivities, tags=tags,
            creator=creator, title=filter_results)
    else:
        return render_template(
            "myActivities.html", myActivities=myActivities, tags=tags,
            creator=creator, title="My Activities")


@app.route('/heypal/<int:creator>/<int:myActivity_id>/myActivity')
@login_required
def showMyActivity(myActivity_id, creator):
    '''Users can gain access to an invidual My Activity entry'''
    # Authorization required
    if login_session['user_id'] != creator:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    activity = session.query(Activity).filter_by(id=myActivity_id).one()
    return render_template(
        'myActivity.html', creator=creator, current=activity)


@app.route(
    '/heypal/<int:activity_id>/addToMyActivities/', methods=["POST"])
@login_required
def addToMyActivities(activity_id):
    '''Users can push a public activity to their private My Activities page,
    if they want to add it to their activity ideas'''
    if request.method == "POST":
        activity = session.query(Activity).filter_by(id=activity_id).one()
        activity.adds_to_myActivities += 1
        session.add(activity)
        session.commit()

        new_id = session.query(func.max(Activity.id)) + 1
        myNewActivity = activity_handler.addToMy(activity, new_id)
        session.add(myNewActivity)
        session.commit()

        return redirect(url_for('showActivities', title="All Activities"))


@app.route('/heypal/<int:creator>/new', methods=["GET", "POST"])
@login_required
def newMyActivity(creator):
    '''Users can create their own My Activity from scratch'''
    # Authorization required
    if login_session['user_id'] != creator:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    if request.method == "POST":
        new_id = session.query(func.max(Activity.id)) + 1
        newMyActivity = activity_handler.createActivity(request, new_id)
        session.add(newMyActivity)
        session.commit()
        return redirect(url_for(
            'showMyActivities', creator=creator, title="My Activities"))
    else:
        return render_template("newActivity.html")


@app.route(
    '/heypal/<int:creator>/<int:myActivity_id>/edit/', methods=["GET", "POST"])
@login_required
def editMyActivity(myActivity_id, creator):
    '''Users can edit an activity they created or activity they pushed from the
    public page with a different location, title, tags, etc.'''
    # Authorization required
    if login_session['user_id'] != creator:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    editActivity = session.query(Activity).filter_by(
        id=myActivity_id).one()

    if request.method == "POST":
        editActivity = activity_handler.performEdit(request, editActivity)
        session.add(editActivity)
        session.commit()
        return redirect(url_for(
            'showMyActivities', creator=creator, title="My Activities"))
    else:
        return render_template(
            'editActivity.html', current=editActivity)


@app.route(
    '/heypal/<int:creator>/<int:myActivity_id>/delete/',
    methods=["GET", "POST"])
def deleteMyActivity(myActivity_id, creator):
    '''Users can remove an activity from their My Activity page'''
    # Authorization required
    if login_session['user_id'] != creator:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")

    deleteActivity = session.query(Activity).filter_by(
        id=myActivity_id).one()

    if request.method == "POST":
        session.delete(deleteActivity)
        session.commit()
        flash("Activity Successfully Deleted: %s" % deleteActivity.name)
        return redirect(url_for(
            'showMyActivities', creator=creator, title="My Activities"))
    else:
        return render_template(
            "deleteActivity.html", current=deleteActivity)


# INVITES
###############################################################################
@app.route('/heypal/myInvites')
@login_required
def invitesRedirect():
    '''Redirects to the Invites Page'''
    user_id = login_session['user_id']
    return redirect(url_for(
        'showMyInvites', user_id=user_id))


@app.route('/heypal/<int:user_id>/myInvites', methods=["GET", "POST"])
@login_required
def showMyInvites(user_id):
    '''Users can view all the events they have been invited to or invited
    others to'''
    if login_session['user_id'] != user_id:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    myInvites = session.query(Invite).filter_by(guest=user_id).all()
    if request.method == "GET":
        return render_template(
            "myInvites.html", myInvites=myInvites, user_id=user_id)


@app.route('/heypal/<int:user_id>/<string:invite_key>/invite')
@login_required
def showMyInvite(invite_key, user_id):
    '''Users can view a single invite entry which displays information on the
    activity as well as the guest list and a message from the creator'''
    if login_session['user_id'] != user_id:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    invites = session.query(Invite).filter_by(invite_key=invite_key).all()
    guest_IDs = []
    for invite in invites:
        guest_IDs.append(invite.guest)
    guests = session.query(User).filter(User.id.in_(guest_IDs))
    invite = session.query(Invite).filter_by(invite_key=invite_key).first()
    host = session.query(User).filter_by(id=invite.host).one()
    return render_template(
        'invite.html', current=invite, user_id=user_id, pals=guests, host=host)


@app.route(
    '/heypal/<int:creator>/<int:myActivity_id>/sendInvite/',
    methods=["GET", "POST"])
def sendInvite(creator, myActivity_id):
    '''Users can send invites to their pals'''
    if login_session['user_id'] != creator:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    activity = session.query(Activity).filter_by(id=myActivity_id).one()
    if request.method == "POST":
        pals = session.query(Pal).filter_by(user_id=creator).all()
        invite_key = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for x in xrange(20))

        for pal in pals:
            if request.form.get(pal.name) == True:
                newInvite = invite_handler.createInvite(
                    activity, request, pal.pal_id, invite_key)
                session.add(newInvite)
                session.commit()

        newInvite = invite_handler.createInvite(
            activity, request, creator, invite_key)
        session.add(newInvite)
        session.commit()

        flash("Invitations have been sent!")
        return redirect(url_for(
            'showMyActivities', creator=creator, title="My Activities"))
    else:
        pals = session.query(Pal).filter_by(user_id=creator).all()
        return render_template(
            'sendInvite.html', current=activity, pals=pals)



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


@app.route('/heypal/publicActivities/JSON')
def publicActivitiesJSON():
    activities = session.query(Activity).filter_by(creator=1).all()
    return jsonify(All_Activities=[a.serialize for a in activities])


@app.route('/heypal/pals/JSON')
def palsJSON():
    pals = session.query(Pal).all()
    return jsonify(All_Pals=[a.serialize for a in pals])


@app.route('/heypal/suggestedPals/JSON')
def suggestedPalsJSON():
    user_id = login_session['user_id']
    pal_user_IDs = [user_id]
    for pal in myPals:
        pal_user_IDs.append(pal.pal_id)

    notMyPals = session.query(User).filter(~User.id.in_(pal_user_IDs)).all()
    return jsonify(Suggested_Pals=[a.serialize for a in notMyPals])


@app.route('/heypal/invites/JSON')
def invitesJSON():
    invites = session.query(Invite).all()
    return jsonify(All_Invites=[a.serialize for a in invites])


@app.route('/heypal/users/JSON')
def usersJSON():
    users = session.query(User).all()
    user = session.query(User).first()
    user.last_login = datetime.now
    return jsonify(All_Users=[a.serialize for a in users])



# Pals
###############################################################################

@app.route('/heypal/myPals')
@login_required
def palsRedirect():
    '''Redirects to Pals Page'''
    user_id = login_session['user_id']
    return redirect(url_for(
        'showMyPals', user_id=user_id))


@app.route('/heypal/<int:user_id>/myPals', methods=["GET", "POST"])
@login_required
def showMyPals(user_id):
    '''Users can view their pals and add more pals to their network'''
    if login_session['user_id'] != user_id:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    myPals = session.query(Pal).filter_by(user_id=user_id).all()

    #myPals = session.query(User).filter(User.id.in_(pal_user_IDs))
    if request.method == "GET":
        return render_template(
            "myPals.html", myPals=myPals, user_id=user_id)


@app.route('/heypal/<int:user_id>/<int:pal_id>/pal')
@login_required
def showMyFriendship(pal_id, user_id):
    '''Users can view a friendship which will include photos and information
    on HeyPal activities done together!'''
    if login_session['user_id'] != user_id:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    myPal = session.query(Pal).filter_by(id=pal_id).one()
    return render_template(
        'pal.html', current=myPal, user_id=user_id)


@app.route('/heypal/<int:user_id>/suggestedPals', methods=["GET", "POST"])
@login_required
def showSuggestedPals(user_id):
    '''Users can view their pals and add more pals to their network'''
    if login_session['user_id'] != user_id:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    myPals = session.query(Pal).filter_by(user_id=user_id).all()

    pal_user_IDs = [user_id]
    for pal in myPals:
        pal_user_IDs.append(pal.pal_id)

    notMyPals = session.query(User).filter(~User.id.in_(pal_user_IDs)).all()

    #myPals = session.query(User).filter(User.id.in_(pal_user_IDs))
    if request.method == "GET":
        return render_template(
            "suggestedPals.html", notMyPals=notMyPals, user_id=user_id)


@app.route(
    '/heypal/<int:user_id>/<int:pal_id>/addPal/', methods=["POST"])
@login_required
def addPal(user_id, pal_id):
    '''Add pal so you can invite them to activities!'''
    if request.method == "POST":
        pal = session.query(User).filter_by(id=pal_id).one()

        newPal = Pal(
            name=pal.name,
            user_id=user_id,
            pal_id=pal.id,
            image=pal.picture
            )

        session.add(newPal)
        session.commit()

        return redirect(url_for('showMyPals', user_id=user_id))


# Google Maps API integration
@app.route('/heypal/maps')
def openMaps():
    return render_template('maps.html')


# Login/Logout functions
###############################################################################
# Create anti-forgery state token
@app.route('/login')
def showLogin():
    '''View the login page'''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbLogin():
    '''Executes FB login using login_handler'''
    output = login_handler.fbconnect()
    return output


@app.route('/gconnect', methods=['POST'])
def googleLogin():
    '''Executes google login using login_handler'''
    output = login_handler.gconnect()
    return output


@app.route('/disconnect')
def disconnect():
    '''Disconnects a user based on provide (FB or google)'''
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
    '''Logout of HeyPal if FB was used to login'''
    output = logout_handler.fbdisconnect()
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def googleLogout():
    '''Logout of HeyPal if google was used to login'''
    output = logout_handler.gdisconnect()
    return output


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
