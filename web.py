from flask import Flask, render_template

import config

# Initializing the web app
app = Flask(__name__)

# Views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview/<template>')
def preview(template):
    return render_template(template)



if __name__ == '__main__':
    app.run(host=config.flask_host, port=config.flask_port, debug=config.flask_debug)