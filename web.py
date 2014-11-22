import mongoengine
from flask import Flask, render_template, send_file

import config
from models import Photo

# Initializing the web app
app = Flask(__name__)
# Initializing the DB
db = mongoengine.connect(config.db_name)

# Views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/photo')
def serve_photo():
    photo = Photo.objects[0]
    return send_file(photo.file, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host=config.flask_host, port=config.flask_port, debug=config.flask_debug)