import bs4 as bs
import requests
import re


def take_info(username):
    source = requests.get(f'https://libre.fm/user/{username}/stats/')
    soup = bs.BeautifulSoup(source.text, 'html.parser')
    find_script = soup.find_all('script')
    return find_script[-2]


def top_tracks(text_target, count=5):
    parse_list = re.findall(r"tracks = \[(.*)\]", str(text_target))
    tracks_html = bs.BeautifulSoup(parse_list[0], 'html.parser').find_all('a')
    tracks_list = []
    for tracks in tracks_html:
        tracks_list.append(tracks.string)
    tracks_list.reverse()
    artists_l = []
    for track_flag in range(2 * 5):
        if track_flag % 2 == 0:
            artists_l.append(tracks_list[track_flag])
    return artists_l[:count]


def top_artists(text_target, count=5):
    parse_list = re.findall(r"artists = \[(.*)\]", str(text_target))
    artists_html = bs.BeautifulSoup(parse_list[0], 'html.parser').find_all('a')
    artists_list = []
    for artist in artists_html:
        artists_list.append(artist.string)
    artists_list.reverse()
    return artists_list[:count]


def generate_photo(top_artist, top_tracks):
    pass


if __name__ == '__main__':
    target = take_info('hosseinhimself')
    print(top_tracks(target))
    print(top_artists(target))