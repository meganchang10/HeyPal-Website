#!/usr/bin/python

from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Activity, Pal, User, MyActivity
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from functools import wraps

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Hey Pal"


# Connect to Database and create database session
engine = create_engine('sqlite:///heypal.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    # Exchange client token for long-lived server-side token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/v2.8/oauth/access_token?'
           'grant_type=fb_exchange_token&client_id=%s&client_secret=%s'
           '&fb_exchange_token=%s') % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    # Extract the access token from response
    token = "access_token=" + data["access_token"]

    # Use token to get user info from API
    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout, let's strip out the information before the equals sign in
    # our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = (
        'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height='
        '200&width=200') % (token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;
    border-radius: 150px;-webkit-border-radius: 150px;
    -moz-border-radius: 150px;"> '''

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = ('https://graph.facebook.com/%s/permissions?access_token=%s'
           % (facebook_id, access_token))
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 404)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 403)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 405)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('''Current user is already
            connected.'''), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' "style = "width: 300px; height: 300px;border-radius: 150px;
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("You are now logged in as %s" % login_session['username'])
    print "Done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
# BEGINNNING


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


def checkTags(request):
    tag_free = request.form.get('tag_free')
    tag_sporty = request.form.get('tag_sporty')
    tag_outdoor = request.form.get('tag_outdoor')
    tag_special = request.form.get('tag_special')
    tag_learn = request.form.get('tag_learn')
    tag_date_night = request.form.get('tag_date_night')

    # So we can filter for "Rainy Day" search
    if not tag_outdoor:
        tag_outdoor = "no"

    return [tag_free, tag_sporty, tag_outdoor, tag_special, tag_learn,
            tag_date_night]


def executeFilter_Activity(filter_results):
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


def executeFilter_myActivity(filter_results, user_id):
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
        activities = executeFilter_Activity(filter_results)
        return render_template(
            'activities.html', activities=activities, tags=tags,
            title=filter_results)

    else:
        if 'username' not in login_session or login_session['user_id'] != 1:
            return render_template(
                'publicActivities.html', activities=activities, tags=tags,
                title="All Activities")
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
    if 'username' not in login_session or login_session['user_id'] != 1:
        return render_template('publicActivity.html', current=activity)
    else:
        return render_template('activity.html', current=activity)


# Create a new activity
@app.route('/heypal/new', methods=["GET", "POST"])
@clearance_level_required
def newActivity():
    if request.method == "POST":

        # Check tags first
        [tag_free, tag_sporty, tag_outdoor, tag_special, tag_learn,
         tag_date_night] = checkTags(request)

        newActivity = Activity(
            name=request.form['name'],
            location=request.form['location'],
            image=request.form['image'],
            description=request.form['description'],
            log_views=0,
            adds_to_myActivities=0,
            user_id=login_session['user_id'],
            tag_free=tag_free,
            tag_sporty=tag_sporty,
            tag_outdoor=tag_outdoor,
            tag_special=tag_special,
            tag_learn=tag_learn,
            tag_date_night=tag_date_night,
            )

        session.add(newActivity)
        flash("New Activity Successfully Created: %s" % newActivity.name)
        session.commit()
        return redirect(url_for('showActivities', title="All Activities"))
    else:
        return render_template("newActivity.html")


@app.route('/heypal/<int:activity_id>/edit/', methods=["GET", "POST"])
@clearance_level_required
def editActivity(activity_id):
    editActivity = session.query(Activity).filter_by(id=activity_id).one()
    if request.method == "POST":

        if request.form['name']:
            editActivity.name = request.form['name']
        if request.form['image']:
            editActivity.image = request.form['image']
        if request.form['location']:
            editActivity.location = request.form['location']

        [tag_free, tag_sporty, tag_outdoor, tag_special, tag_learn,
         tag_date_night] = checkTags(request)

        editActivity.tag_free = tag_free
        editActivity.tag_sporty = tag_sporty
        editActivity.tag_outdoor = tag_outdoor
        editActivity.tag_special = tag_special
        editActivity.tag_learn = tag_learn
        editActivity.tag_date_night = tag_date_night

        session.add(editActivity)
        session.commit()
        flash("Activity Successfully Edited: %s" % editActivity.name)
        return redirect(url_for('showActivities', title="All Activities"))
    else:
        return render_template('editActivity.html', current=editActivity)


@app.route('/heypal/<int:activity_id>/delete/', methods=["GET", "POST"])
@clearance_level_required
def deleteActivity(activity_id):
    deleteActivity = session.query(Activity).filter_by(id=activity_id).one()
    if request.method == "POST":
        session.delete(deleteActivity)
        flash("Activity  Successfully Deleted: %s" % deleteActivity.name)
        session.commit()
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
        myActivities = executeFilter_myActivity(filter_results, user_id)
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
        'myActivity.html', current=activity, user_id=user_id)


@app.route(
    '/heypal/<int:activity_id>/addToMyActivities/', methods=["POST"])
@login_required
def addToMyActivities(activity_id):
    if request.method == "POST":
        activity = session.query(Activity).filter_by(id=activity_id).one()
        activity.adds_to_myActivities += 1
        session.add(activity)
        session.commit()

        myNewActivity = MyActivity(
            name=activity.name,
            location=activity.location,
            image=activity.image,
            description=activity.description,
            user_id=login_session['user_id'],
            tag_free=activity.tag_free,
            tag_sporty=activity.tag_sporty,
            tag_outdoor=activity.tag_outdoor,
            tag_special=activity.tag_special,
            tag_learn=activity.tag_learn,
            tag_date_night=activity.tag_date_night,
            )

        session.add(myNewActivity)
        session.commit()
        flash("%s Successfully Added to My Activities" % myNewActivity.name)
        return redirect(url_for('showActivities', title="All Activities"))


@app.route('/heypal/<int:user_id>/new', methods=["GET", "POST"])
@login_required
def newMyActivity(user_id):
    # Authorization required
    if login_session['user_id'] != user_id:
        flash("Only Authorized Users Can Access That Page")
        return redirect("/")
    if request.method == "POST":

        [tag_free, tag_sporty, tag_outdoor, tag_special, tag_learn,
         tag_date_night] = checkTags(request)

        newMyActivity = MyActivity(
            name=request.form['name'],
            location=request.form['location'],
            image=request.form['image'],
            description=request.form['description'],
            user_id=login_session['user_id'])

        session.add(newMyActivity)
        flash("New Activity Successfully Created: %s" % newMyActivity.name)
        session.commit()
        return redirect(url_for(
            'showMyActivities', user_id=user_id, title="My Activities"))
    else:
        return render_template("newMyActivity.html", user_id=user_id)


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
        if request.form['name']:
            editActivity.name = request.form['name']
        if request.form['image']:
            editActivity.image = request.form['image']
        if request.form['location']:
            editActivity.location = request.form['location']

        [tag_free, tag_sporty, tag_outdoor, tag_special, tag_learn,
         tag_date_night] = checkTags(request)

        editActivity.tag_free = tag_free
        editActivity.tag_sporty = tag_sporty
        editActivity.tag_outdoor = tag_outdoor
        editActivity.tag_special = tag_special
        editActivity.tag_learn = tag_learn
        editActivity.tag_date_night = tag_date_night

        session.add(editActivity)
        session.commit()
        flash("Activity Successfully Edited: %s" % editActivity.name)
        return redirect(url_for(
            'showMyActivities', user_id=user_id, title="My Activities"))
    else:
        return render_template(
            'editActivity.html', current=editActivity, user_id=user_id)


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
        flash("Activity Successfully Deleted: %s" % deleteActivity.name)
        session.delete(deleteActivity)
        session.commit()
        return redirect(url_for(
            'showMyActivities', user_id=user_id, title="My Activities"))
    else:
        return render_template(
            "deleteMyActivity.html", current=deleteActivity, user_id=user_id)


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


# ENDING #
###############################################################################
###############################################################################
###############################################################################
# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
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


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
