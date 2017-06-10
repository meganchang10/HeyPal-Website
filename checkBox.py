from datetime import datetime
from flask import flash

def checkTags(request):
    tag_free = request.form.get('tag_free')
    tag_sporty = request.form.get('tag_sporty')
    tag_outdoor = request.form.get('tag_outdoor')
    tag_special = request.form.get('tag_special')
    tag_learn = request.form.get('tag_learn')
    tag_date_night = request.form.get('tag_date_night')
    tag_over_21 = request.form.get('tag_over_21')
    tag_after_work = request.form.get('tag_after_work')

    return [tag_free, tag_sporty, tag_outdoor, tag_special, tag_learn,
            tag_date_night, tag_over_21, tag_after_work]


def checkDateTime(current, request):
    result = None
    print(1)
    if current.datetime:
        if current.datetime.month:
            print(2)
            month = current.datetime.month
        if current.datetime.strftime("%d"):
            day = int(current.datetime.strftime("%d"))
        if current.datetime.strftime("%Y"):
            year = int(current.datetime.strftime("%Y"))
        if current.datetime.strftime("%H"):
            hour = int(current.datetime.strftime("%H"))
        else:
            hour = 0
        if current.datetime.strftime("%M"):
            minute = int(current.datetime.strftime("%M"))
        else:
            minute = 0
    else:
        hour = 0
        minute = 0

    if request.form['date']:
        print(5)
        dateString = request.form['date'].split("/")
        month = int(dateString[0])
        day = int(dateString[1])
        if request.form['year']:
            year = request.form['year'][-2:]
            year = int("20" + year)
        else:
            year = 2017
        result = datetime(year, month, day)

    if request.form['time']:
        if request.form['date']:
            timeString = request.form['time'].split(":")
            hour = int(timeString[0])
            if request.form['AMorPM'] == "PM":
                hour += 12
            if len(timeString) == 2:
                minute = int(timeString[1])
                result = datetime(year, month, day, hour, minute)
        else:
            flash("Date required to set time.")

    return result
