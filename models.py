#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine
import numpy as np
from pyechonest import config as echonest_config
from pyechonest import song as echonest_song
from pyechonest import artist as echonest_artist
import requests
#from sklearn.metrics.pairwise import cosine_similarity

import config

echonest_config.ECHO_NEST_API_KEY = config.echo_nest_api_key
SPOTIFY_API = 'https://api.spotify.com/v1'
FEATURES_KEYS = {'energy', 'liveness', 'tempo', 'speechiness', 'acousticness', 'danceability', 'instrumentalness'}

class Track(mongoengine.Document):
    id = mongoengine.StringField(primary_key=True, unique=True)
    name = mongoengine.StringField(required=True)
    artist_id = mongoengine.StringField(required=True)
    artist_name = mongoengine.StringField(required=True)
    album = mongoengine.StringField(required=True)
    uri = mongoengine.StringField(required=True)
    preview_url = mongoengine.StringField(required=True)
    image = mongoengine.StringField(required=True)
    genres = mongoengine.ListField(mongoengine.StringField())
    audio_summary = mongoengine.DictField()

    @property
    def features_vector(self):
        return np.array([self.audio_summary[attr] for attr in FEATURES_KEYS])

    @property
    def similar_tracks(self, n=5):
        tracks = Track.objects()
        features = self.features_vector
        tracks = sorted(tracks, key=lambda t: cosine_similarity(features, t.features_vector))
        return [(t, cosine_similarity(features, t.features_vector)) for t in tracks]

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

    def get_similar_tracks(self):
        similar_tracks = []
        for track in Track.objects():
            if any(genre in self.genres for genre in track.genres) and track != self:
                similar_tracks.append(track)
        return similar_tracks

class Photo(mongoengine.Document):
    file = mongoengine.FileField(required=True)

class Submission(mongoengine.Document):
    date = mongoengine.DateTimeField(default=datetime.now)
    photo = mongoengine.ReferenceField(Photo)
    track = mongoengine.ReferenceField(Track)

if __name__ == '__main__':
    db = mongoengine.connect(config.db_name)
    track = Track.get_from_spotify('maskinen', 'krossa alla fönster')
    track.save()
    print track.__dict__