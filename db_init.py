import os

import mongoengine

from models import Track, Photo, Submission
import config

db = mongoengine.connect(config.db_name)

PICTURES_FOLDER = 'example_pictures'

if __name__ == '__main__':

    for track_photo_name in os.listdir(PICTURES_FOLDER):
        path = os.path.join(PICTURES_FOLDER, track_photo_name)
        # Photo object
        photo = Photo()
        track_photo = open(path, 'rb')
        photo.file.put(track_photo)
        photo.save()

        # Track object
        artist, title = track_photo_name.split('.')[0].split('_')
        track = Track.get_from_spotify(artist, title)
        if track is None:
            print " !Couldn't get info for '{} - {}' ; skipping.".format(artist, title)
            continue
        track.save()

        # Submission
        submission = Submission(photo=photo, track=track)
        submission.save()
        print "* '{} - {}' saved in the db".format(artist, title)