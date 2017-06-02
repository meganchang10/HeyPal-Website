def calendarify(request):
    year = request.form.get('year')
    month = request.form.get('month')
    day = request.form.get('day')
    hour = request.form.get('hour')
    minute = request.form.get('minute')
    second = request.form.get('second')

    result = datetime(year, month, day, hour, minute, second)

def generateNotifications():
    user_id = login_session['user_id']
    count = session.query(Invite).filter_by(guest=user_id).count()
    user = session.query(User).filter_by(id=user_id).one()
    notifications = count - user.invites
    print(notifications)
    return notifications


        else:
            notifications = generateNotifications()

        user.invites = count = session.query(Invite).filter_by(guest=user_id).count()

        print(user.invites)
        print(count)
        print(datetime.now())