#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine
import requests

import json

SPOTIFY_API = 'https://api.spotify.com/v1'

class Track(mongoengine.Document):
    id = mongoengine.StringField(primary_key=True)
    name = mongoengine.StringField(required=True)
    artist = mongoengine.StringField(required=True)
    album = mongoengine.StringField(required=True)
    uri = mongoengine.StringField(required=True)
    preview_url = mongoengine.StringField(required=True)
    image = mongoengine.StringField(required=True)

    @staticmethod
    def get_from_spotify(query):
        request_url = '{}/search'.format(SPOTIFY_API)
        response = requests.get(request_url, params={'q': query, 'type': 'track'}).json()

        items = response['tracks']['items']
        if not items:
            return None
        raw_track_data = items[0]

        track_data = dict()
        for attr in ['id', 'name', 'uri', 'preview_url']:
            track_data[attr] = raw_track_data[attr]
        track_data['artist'] = raw_track_data['artists'][0]['name']
        track_data['album'] = raw_track_data['album']['name']
        track_data['image'] = raw_track_data['album']['images'][0]['url']

        return Track(**track_data)

class Photo(mongoengine.Document):
    file = mongoengine.FileField(required=True)

class Submission(mongoengine.Document):
    date = mongoengine.DateTimeField(default=datetime.now)
    photo = mongoengine.ReferenceField(Photo)
    track = mongoengine.ReferenceField(Track)

if __name__ == '__main__':
    db = mongoengine.connect('test_db')
    track = Track.get_from_spotify('maskinen krossa alla fönster')
    track.save()
    print track.__dict__