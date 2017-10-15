import soco

class SonosWrapper(object):

    """ A wrapper around some SoCo calls to simplify things. """

    debug = False
    sonos = None

    def __init__(self, config=None):
        # TODO: Write later when we have access to the speakers...
        pass

    def toggle_debug(self):
        self.debug = not(self.debug)

    def get_current_track_info(self):
        if self.debug:
            return {
                'title': '99',
                'artist': 'Toto',
                'album': 'The Essential Toto',
                'album_art': 'http://127.0.0.1:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a4oz7fKT4bJ04KCaMM7Sp03%3fsid%3d9%26flags%3d8224%26sn%3d1',
                'position': '0:00:11',
                'playlist_position': '0',
                'duration': '0:05:12',
                'uri': 'x-sonos-spotify:spotify%3atrack%3a4oz7fKT4bJ04KCaMM7Sp03?sid=9&flags=8224&sn=1',
                'metadata': '<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/"><item id="-1" parentID="-1" restricted="true"><res protocolInfo="sonos.com-spotify:*:audio/x-spotify:*" duration="0:05:12">x-sonos-spotify:spotify%3atrack%3a4oz7fKT4bJ04KCaMM7Sp03?sid=9&amp;flags=8224&amp;sn=1</res><r:streamContent></r:streamContent><upnp:albumArtURI>/getaa?s=1&amp;u=x-sonos-spotify%3aspotify%253atrack%253a4oz7fKT4bJ04KCaMM7Sp03%3fsid%3d9%26flags%3d8224%26sn%3d1</upnp:albumArtURI><dc:title>99</dc:title><upnp:class>object.item.audioItem.musicTrack</upnp:class><dc:creator>Toto</dc:creator><upnp:album>The Essential Toto</upnp:album></item></DIDL-Lite>'
            }
        else:
            return self.sonos.get_current_track_info()
    
    def get_queue(self):
        songs = []
        if self.debug:
            songs.extend([
                {
                    'title': '99',
                    'artist': 'Toto',
                    'album': 'The Essential Toto',
                    'album_art': 'http://127.0.0.1:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a4oz7fKT4bJ04KCaMM7Sp03%3fsid%3d9%26flags%3d8224%26sn%3d1',
                    'position': '0:00:11',
                    'playlist_position': '0',
                    'duration': '0:05:12',
                    'uri': 'x-sonos-spotify:spotify%3atrack%3a4oz7fKT4bJ04KCaMM7Sp03?sid=9&flags=8224&sn=1',
                    'metadata': '<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/"><item id="-1" parentID="-1" restricted="true"><res protocolInfo="sonos.com-spotify:*:audio/x-spotify:*" duration="0:05:12">x-sonos-spotify:spotify%3atrack%3a4oz7fKT4bJ04KCaMM7Sp03?sid=9&amp;flags=8224&amp;sn=1</res><r:streamContent></r:streamContent><upnp:albumArtURI>/getaa?s=1&amp;u=x-sonos-spotify%3aspotify%253atrack%253a4oz7fKT4bJ04KCaMM7Sp03%3fsid%3d9%26flags%3d8224%26sn%3d1</upnp:albumArtURI><dc:title>99</dc:title><upnp:class>object.item.audioItem.musicTrack</upnp:class><dc:creator>Toto</dc:creator><upnp:album>The Essential Toto</upnp:album></item></DIDL-Lite>'
                },
                {
                    'title': 'Africa',
                    'artist': 'Toto',
                    'album': 'The Essential Toto',
                    'album_art': 'http://127.0.0.1:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a5ob66YV6bJ04KCaMM7Sp03%3fsid%3d9%26flags%3d8224%26sn%3d1',
                    'position': '0:00:11',
                    'playlist_position': '2',
                    'duration': '0:05:12',
                    'uri': 'x-sonos-spotify:spotify%3atrack%3a5ob66YV6bJ04KCaMM7Sp03?sid=9&flags=8224&sn=1',
                    'metadata': '<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/"><item id="-1" parentID="-1" restricted="true"><res protocolInfo="sonos.com-spotify:*:audio/x-spotify:*" duration="0:05:12">x-sonos-spotify:spotify%3atrack%3a4oz7fKT4bJ04KCaMM7Sp03?sid=9&amp;flags=8224&amp;sn=1</res><r:streamContent></r:streamContent><upnp:albumArtURI>/getaa?s=1&amp;u=x-sonos-spotify%3aspotify%253atrack%253a4oz7fKT4bJ04KCaMM7Sp03%3fsid%3d9%26flags%3d8224%26sn%3d1</upnp:albumArtURI><dc:title>99</dc:title><upnp:class>object.item.audioItem.musicTrack</upnp:class><dc:creator>Toto</dc:creator><upnp:album>The Essential Toto</upnp:album></item></DIDL-Lite>'
                }
            ])
        else:
            songs.extend(list(self.sonos.get_queue()))

        return songs

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            return getattr(self.sonos, name)(*args, **kwargs)

        return wrapper