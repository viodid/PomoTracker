"""Helper functions for the view's app"""
def saveSettings(form, user):
    """Save user settings to the database"""
    settings = user.settings
    if form['image']:
        delete_previous_image(settings)
        settings.image = form['image']
    if form['shortBreak']:
        settings.shortBreak = int(form['shortBreak'])
    if form['longBreak']:
        settings.longBreak = int(form['longBreak'])
    if form['theme']:
        settings.theme = form['theme']
        if form['theme'] == 'forest':
            settings.focusColor = '#EAE7B1'
        elif form['theme'] == 'aquamarine':
            settings.focusColor = '#6BAAAA'
        elif form['theme'] == 'default' or form['theme'] == 'white':
            settings.focusColor = '#f1c232'
        elif form['theme'] == 'garnet':
            settings.focusColor = '#9a1b18'
        elif form['theme'] == 'coral':
            settings.focusColor = '#FAD6A5'
    if form['startSound']:
        settings.startSound = form['startSound']
    if form['stopSound']:
        settings.stopSound = form['stopSound']
    if form['timezone']:
        settings.timezone = form['timezone']
    settings.save()


def delete_previous_image(settings):
    """Delete previous image from the server"""
    if settings.image.name != 'default.png':
        settings.image.delete(save=False)
