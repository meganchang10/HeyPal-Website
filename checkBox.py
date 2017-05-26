

def checkTags(request):
    tag_free = request.form.get('tag_free')
    tag_sporty = request.form.get('tag_sporty')
    tag_outdoor = request.form.get('tag_outdoor')
    tag_special = request.form.get('tag_special')
    tag_learn = request.form.get('tag_learn')
    tag_date_night = request.form.get('tag_date_night')

    return [tag_free, tag_sporty, tag_outdoor, tag_special, tag_learn,
            tag_date_night]