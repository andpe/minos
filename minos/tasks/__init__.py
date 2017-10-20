from ..app import celery, create_app
from celery.schedules import crontab
from ..sonos import SonosWrapper

celery.conf.beat_schedule = {
    'sonos-queue-update': {
        'task': 'minos.tasks.sonos_queue_refresh',
        'schedule': 60,
        'args': (1, 2),
    },
}

app = create_app(True)
sonos = SonosWrapper()

@celery.task
def sonos_queue_refresh(a, b):
    from urllib.parse import unquote
    from flask import current_app

    #if current_app.debug and not sonos.debug:
    #    sonos.toggle_debug()

    wrapper = sonos
    tracks = wrapper.get_queue()
    current = wrapper.get_current_track_info()

    if len(tracks) > 0:
        current_app.cache.set('minos_tracklist', tracks)
        current_app.cache.set('minos_current_song', current)
    else:
        pass