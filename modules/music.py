from flask import Blueprint, render_template, redirect, url_for

music = Blueprint('music', __name__, template_folder='templates/music/')

@music.route("/index")
@music.route("/")
def index():
    import soco

    # TODO : Abstract this so that it can be mocked.
    sonos = soco.SoCo("10.203.70.157")

    tracks = sonos.get_queue()
    # 'title': '99', 'artist': 'Toto', 'album': 'The Essential Toto', 'album_art': 'http://10.203.70.157:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a4oz7fKT4bJ04KCaMM7Sp03%3fsid%3d9%26flags%3d8224%26sn%3d1', 'position': '0:00:11', 'playlist_position': '2', 'duration': '0:05:12', 'uri': 'x-sonos-spotify:spotify%3atrack%3a4oz7fKT4bJ04KCaMM7Sp03?sid=9&flags=8224&sn=1', 'metadata': '<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/"><item id="-1" parentID="-1" restricted="true"><res protocolInfo="sonos.com-spotify:*:audio/x-spotify:*" duration="0:05:12">x-sonos-spotify:spotify%3atrack%3a4oz7fKT4bJ04KCaMM7Sp03?sid=9&amp;flags=8224&amp;sn=1</res><r:streamContent></r:streamContent><upnp:albumArtURI>/getaa?s=1&amp;u=x-sonos-spotify%3aspotify%253atrack%253a4oz7fKT4bJ04KCaMM7Sp03%3fsid%3d9%26flags%3d8224%26sn%3d1</upnp:albumArtURI><dc:title>99</dc:title><upnp:class>object.item.audioItem.musicTrack</upnp:class><dc:creator>Toto</dc:creator><upnp:album>The Essential Toto</upnp:album></item></DIDL-Lite>'}
    current = sonos.get_current_track_info()

    index = int(current['playlist_position'])
    tracks = list(tracks)
    played = tracks[:index]
    future = tracks[index-1:]

    return render_template('hello.html', tracks=future + played, current=current)