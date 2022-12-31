# https://stackoverflow.com/questions/2223429/django-global-template-variables
import PomoTracker


def global_settings(request):
    return {
        'SITE_NAME': 'PomoTracker',
        'SITE_URL': 'https://pomotracker.app',
        'SITE_DESCRIPTION': 'Pomodoro Tracker',
        'SITE_KEYWORDS': 'pomodoro, tracker, productivity, time management',
        'SITE_AUTHOR': 'PomoTracker',
        'SITE_TWITTER': '@PomoTracker',
        'SITE_GITHUB': 'https://github.com/viodid/PomoTracker',
        'SITE_VERSION': PomoTracker.__version__
    }
