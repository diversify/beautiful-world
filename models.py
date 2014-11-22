#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine
from pyechonest import config as echonest_config
from pyechonest import song as echonest_song
from pyechonest import artist as echonest_artist
import requests

import config

echonest_config.ECHO_NEST_API_KEY = config.echo_nest_api_key
SPOTIFY_API = 'https://api.spotify.com/v1'

class Track(mongoengine.Document):
    id = mongoengine.StringField(primary_key=True)
    name = mongoengine.StringField(required=True)
    artist_id = mongoengine.StringField(required=True)
    artist_name = mongoengine.StringField(required=True)
    album = mongoengine.StringField(required=True)
    uri = mongoengine.StringField(required=True)
    preview_url = mongoengine.StringField(required=True)
    image = mongoengine.StringField(required=True)
    genres = mongoengine.ListField(mongoengine.StringField())
    audio_summary = mongoengine.DictField()

    @staticmethod
    def get_from_spotify(artist, title):
        # Getting data from spotify
        request_url = '{}/search'.format(SPOTIFY_API)
        query = '{} {}'.format(artist, title)
        response = requests.get(request_url, params={'q': query, 'type': 'track'}).json()

        items = response['tracks']['items']
        if not items:
            print "Couldn't find '{} - {}' on Spotify".format(artist, title)
            return None
        raw_track_data = items[0]

        track_data = dict()
        for attr in ['id', 'name', 'uri', 'preview_url']:
            track_data[attr] = raw_track_data[attr]
        track_data['artist_name'] = raw_track_data['artists'][0]['name']
        track_data['artist_id'] = raw_track_data['artists'][0]['id']
        track_data['album'] = raw_track_data['album']['name']
        track_data['image'] = raw_track_data['album']['images'][0]['url']

        # EchoNest enrichement
        songs = echonest_song.search(artist=artist, title=title)
        if not songs:
            print "Couldn't find '{} - {}' on EchoNest".format(artist, title)
            return None
        song = songs[0]
        track_data['audio_summary'] = song.audio_summary
        artist = echonest_artist.search(name=song.artist_name)[0]
        track_data['genres'] = [t['name'] for t in artist.terms]

        return Track(**track_data)

class Photo(mongoengine.Document):
    file = mongoengine.FileField(required=True)

class Submission(mongoengine.Document):
    date = mongoengine.DateTimeField(default=datetime.now)
    photo = mongoengine.ReferenceField(Photo)
    track = mongoengine.ReferenceField(Track)

if __name__ == '__main__':
    db = mongoengine.connect('test_db')
    track = Track.get_from_spotify('maskinen', 'krossa alla fönster')
    track.save()
    print track.__dict__