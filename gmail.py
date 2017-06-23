# Create a new activity

#from __init__.py
@app.route('/heypal/new', methods=["GET", "POST"])
@login_required
@clearance_level_required
def newActivity():
    '''Authorized users can create new public activities for the main page'''
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


@app.route('/gconnect', methods=['POST'])
def googleLogin():
    '''Executes google login using login_handler'''
    output = login_handler.gconnect()
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def googleLogout():
    '''Logout of HeyPal if google was used to login'''
    output = logout_handler.gdisconnect()
    return output


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


# from disconnect python file
        if login_session['provider'] == 'google':
            logout_handler.gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']


# from login_handlers
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
        oauth_flow = flow_from_clientsecrets('/var/www/HeyPal/heypal/client_secrets.json', scope='')
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


# from logout_handlers
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
