from lyricsgenius import Genius
import os
import random

genius = Genius(os.getenv('GENIUS_TOKEN'), verbose=False)


def get_artist_id(artist):
    result = genius.search_artist(artist, max_songs=0, get_full_info=False)
    artist_id = result.id
    return artist_id


def get_albums(artist_id):
    result = genius.artist_albums(artist_id)
    albums = []
    for album in result['albums']:
        albums.append({'name': album['name'], 'id': album['id']})
    return albums


def get_tracks(album_id):
    result = genius.album_tracks(album_id)
    song_titles = []
    for track in result['tracks']:
        song_titles.append(track['song']['title'].strip(u'\u200b'))
    return song_titles


def lyrics(song_name, artist):
    result = genius.search_song(title=song_name, artist=artist,
                                get_full_info=False)
    return result.to_dict()['lyrics']


def game(artist):
    artist_name = artist
    albums = get_albums(get_artist_id(artist_name))

    print('Az előadó albumjai: ')
    album_index = 1
    for album in albums:
        print(f'{album_index}. {album["name"]}')
        album_index += 1

    chosen_album_index = int(input('Válassz egy albumot és add meg a számát! '))
    chosen_album = albums[chosen_album_index - 1]

    songs = get_tracks(chosen_album['id'])
    random_song = random.choice(songs)

    print('Az albumból egy random szám dalszövege: ')
    print(lyrics(random_song, artist_name))

    guess = input('Melyik ez a szám? ')
    if guess == str(random_song):
        print('Eltaláltad!')
    else:
        print(f'Sajnos nem jó. A szám a {random_song} volt.')


def main():
    artist = input('Add meg a kedvenc előadódat! ')
    game(artist)


main()
