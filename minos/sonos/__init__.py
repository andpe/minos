import soco
from collections import namedtuple

SonosTrack = namedtuple('SonosTrack', [
    'title', 'artist', 'album', 'album_art_uri', 'position',
    'playlist_position', 'duration', 'uri', 'resources', 'album_art',
    'metadata'
])

SonosTrack.__new__.__defaults__ = (None,) * len(SonosTrack._fields)

class Track(SonosTrack):

    def get_unique_id(self):
        from hashlib import sha256
        h = sha256()

        h.update(str(self.artist).encode('utf-8') + str(self.album).encode('utf-8') + str(self.title).encode('utf-8'))
        return h.hexdigest()

Resources = namedtuple('Resources', [
    'bitrate', 'bits_per_sample', 'color_depth', 'duration', 'import_uri', 
    'nr_audio_channels', 'protection', 'protocol_info', 'resolution', 
    'sample_frequency', 'size', 'uri'
])

Resources.__new__.__defaults__ = (None,) * len(Resources._fields)

class SonosWrapper(object):

    """ A wrapper around some SoCo calls to simplify things. """

    debug = False
    speakers = []
    sonos = None

    def __init__(self, config=None):
        # TODO: Write later when we have access to the speakers...
        #self.speakers = soco.discover()
        self.sonos = soco.SoCo("10.203.70.133")

    def toggle_debug(self):
        self.debug = not(self.debug)

    def get_current_track_info(self):
        if self.debug:
            return Track(**{
                'title': '99',
                'artist': 'Toto',
                'album': 'The Essential Toto',
                'album_art_uri': 'http://127.0.0.1:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a4oz7fKT4bJ04KCaMM7Sp03%3fsid%3d9%26flags%3d8224%26sn%3d1',
                'position': '0:00:11',
                'playlist_position': '0',
                'duration': '0:05:12',
                'resources': [Resources(uri='x-sonos-spotify:spotify%3atrack%3a4oz7fKT4bJ04KCaMM7Sp03?sid=9&flags=8224&sn=1')],
            })
        else:
            return Track(**self.sonos.get_current_track_info())
    
    def get_queue(self):
        songs = []
        if self.debug:
            songs.extend([
                Track(**{
                    'title': '99',
                    'artist': 'Toto',
                    'album': 'The Essential Toto',
                    'album_art_uri': 'http://127.0.0.1:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a4oz7fKT4bJ04KCaMM7Sp03%3fsid%3d9%26flags%3d8224%26sn%3d1',
                    'position': '0:00:11',
                    'playlist_position': '0',
                    'duration': '0:05:12',
                    'resources': [
                        Resources(uri='x-sonos-spotify:spotify%3atrack%3a4oz7fKT4bJ04KCaMM7Sp03?sid=9&flags=8224&sn=1')
                    ],
                }),
                Track(**{
                    'title': 'Africa',
                    'artist': 'Toto',
                    'album': 'The Essential Toto',
                    'album_art_uri': 'http://127.0.0.1:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a5ob66YV6bJ04KCaMM7Sp03%3fsid%3d9%26flags%3d8224%26sn%3d1',
                    'position': '0:00:11',
                    'playlist_position': '2',
                    'duration': '0:05:12',
                    'resources': [Resources(uri='x-sonos-spotify:spotify%3atrack%3a5ob66YV6bJ04KCaMM7Sp03?sid=9&flags=8224&sn=1')],
                })
            ])
        else:
            sonos_songs = list(self.sonos.get_queue())

            for song in sonos_songs:
                s = {
                    'title': song.title,
                    'artist': song.creator,
                    'album': song.album,
                    'album_art_uri': song.album_art_uri,
                    'resources': song.resources
                }

                songs.append(Track(**s))

        return songs

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            return getattr(self.sonos, name)(*args, **kwargs)

        return wrapper