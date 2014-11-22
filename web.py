import json

import mongoengine
from flask import Flask, render_template, send_file

import config
from models import Submission

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

@app.route('/submissions')
def submissions_view():
    return render_template('submissions.html', submissions=Submission.objects)

@app.route('/preview/<template>')
def preview(template):
    return render_template(template)

@app.route('/api/submissions')
def api_submissions():
    return json.dumps([dict(track=sub.track.to_dict(), id=str(sub.id)) for sub in Submission.objects])

@app.route('/api/submission/<submission_id>/photo')
def api_submission_photo(submission_id):
    photo = Submission.objects.get(id=submission_id).photo
    return send_file(photo.file, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host=config.flask_host, port=config.flask_port, debug=config.flask_debug)