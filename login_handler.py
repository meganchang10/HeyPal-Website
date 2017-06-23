from flask import session as login_session
from flask import request, make_response, flash
import httplib2
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, User

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import requests

from datetime import datetime

CLIENT_ID = json.loads(
    open('/var/www/HeyPal/heypal/client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('postgresql://heypal:PASSWORD@localhost/heypal')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    # Exchange client token for long-lived server-side token
    app_id = json.loads(open('/var/www/HeyPal/heypal/fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('/var/www/HeyPal/heypal/fb_client_secrets.json', 'r').read())['web']['app_secret']
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


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

