

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