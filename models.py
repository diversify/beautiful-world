from datetime import datetime

import mongoengine

class Track(mongoengine.Document):
    id = mongoengine.StringField(primary_key=True)
    title = mongoengine.StringField(required=True)
    artist = mongoengine.StringField(required=True)
    album = mongoengine.StringField(required=True)
    genre = mongoengine.StringField(required=True)
    uri = mongoengine.StringField(required=True)
    preview_url = mongoengine.StringField(required=True)
    image = mongoengine.StringField(required=True)

class Photo(mongoengine.Document):
    file = mongoengine.FileField(required=True)

class Submission(mongoengine.Document):
    date = mongoengine.DateTimeField(default=datetime.now)
    photo = mongoengine.ReferenceField(Photo)
    track = mongoengine.ReferenceField(Track)

if __name__ == '__main__':
    track = Track(id='myid', title='My title', artist='Artist', album='Album', genre='Genre', uri='Uri', preview_url='Preview_Url', image='Image URL')
    print track.__dict__

    submission = Submission(track=track, photo=None)
    print submission.__dict__