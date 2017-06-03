import checkBox
from database_setup import Invite
from flask import session as login_session


def createInvite(activity, request, guest_id, invite_key):
    [tag_free, tag_sporty, tag_outdoor, tag_special, tag_learn,
     tag_date_night] = checkBox.checkTags(request)

    newInvite = Invite(
        host=login_session['user_id'],
        guest=guest_id,
        invite_key=invite_key,
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
    newInvite.datetime = activity.datetime

    newInvite.message = "Hey Pals! Who is down for this awesome activity?"

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

    return newInvite
