from ..app import celery, create_app
from celery.schedules import crontab
from ..sonos import SonosWrapper

celery.conf.beat_schedule = {
    'sonos-queue-update': {
        'task': 'minos.tasks.sonos_queue_refresh',
        'schedule': 10,
        'args': (1, 2),
    },
}

app = create_app(True)

@celery.task
def sonos_queue_refresh(a, b):
    from urllib.parse import unquote
    from flask import current_app
    from ..database import SonosConfig, db
    from flask import current_app
    import soco
    from hashlib import sha256

    speakers = {}
    with current_app.app_context():
        speakers = db.session.query(SonosConfig).filter(
            SonosConfig.key == 'speakers'
        ).first()

        if speakers:
            from json import loads
            speakers = loads(speakers.value)
            speakers = {x: soco.SoCo(x) for x in speakers}
        else:
            speakers = {
                '10.203.70.133': soco.SoCo('10.203.70.133')
            }

    sonos = SonosWrapper(speakers)

    if current_app.debug and not sonos.debug:
        sonos.toggle_debug()

    for ip, so in sonos.get_speakers().items():
        tracks = sonos.get_queue(ip)
        current = sonos.get_current_track_info(ip)

        if len(tracks) > 0:
            sha = sha256()
            sha.update(ip.encode('utf-8'))
            current_app.cache.set('minos_tracklist_' + sha.hexdigest(), tracks)
            current_app.cache.set('minos_current_song_' + sha.hexdigest(), current)
        else:
            pass