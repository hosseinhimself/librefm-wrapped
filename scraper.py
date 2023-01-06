from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
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


def collect_photo_of_artist(artist_name):
    artist_name = artist_name.replace(' ', "+")
    source = requests.get(f'https://www.google.com/search?q={artist_name}+spotify+photo')

    soup = bs.BeautifulSoup(source.text, 'html.parser')
    find_script = soup.find_all('a', {'class': 'BVG0Nb'})
    parse_list = re.findall(r"https\:\/\/www\.google\.com\/imgres\?imgurl\=(https?\:\/\/.*)\&imgrefurl.*",str(find_script[0]['href']))
    return parse_list[0]


def generate_photo(top_artists, top_tracks):
    img = Image.open('templates/librefm.jpg')
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype('font/Ubuntu-M.ttf', 35)

    # Writing Top five artists
    gg = 1040
    for i in top_artists:
        if len(i) > 20:
            i = i.replace(i[20:], '...')
        draw.text((150, gg + 46), i, (248, 215, 226), font=font)
        gg = gg + 56
    gg = 1040

    # Writing top 5 musics
    for i in top_tracks:
        if len(i) > 20:
            i = i.replace(i[20:], '...')
        draw.text((640, gg + 46), i, (248, 215, 226), font=font)
        gg = gg + 56

        # Add my Info here
        font3 = ImageFont.truetype('font/Ubuntu-M.ttf', 40)
        draw.text((400, 1870), "Libre.fm Wrapped, By Hossein M", (211, 12, 45), font=font3)

        # Insert Top artist Image
        import urllib.request
        urllib.request.urlretrieve(collect_photo_of_artist(top_artists[0]),"file_name")
        artist_image = Image.open("file_name")
        artist_image = artist_image.resize((600, 600))
        img.paste(artist_image, (245, 182))

    # saving the image
    img.save('librefm-Wrapped.jpg')
    print('Done!')


if __name__ == '__main__':
    target = take_info('hosseinhimself')
    a = top_tracks(target)
    b = top_artists(target)
    generate_photo(b, a)
