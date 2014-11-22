import json

import mongoengine
from flask import Flask, render_template, send_file

import config
from models import Photo, Track

# Initializing the web app
app = Flask(__name__)
# Initializing the DB
db = mongoengine.connect(config.db_name)
# Utility function to dump objects to json
mongoengine.Document.to_dict = lambda d : json.loads(d.to_json())

# Views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview/<template>')
def preview(template):
    return render_template(template)

@app.route('/api/tracks')
def tracks():
    return json.dumps([track.to_dict() for track in Track.objects])

@app.route('/photo')
def serve_photo():
    photo = Photo.objects[0]
    return send_file(photo.file, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host=config.flask_host, port=config.flask_port, debug=config.flask_debug)