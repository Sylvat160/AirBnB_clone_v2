#!/usr/bin/python3
""" Starts a Flask web application
    - The web application must be listening on
    0.0.0.0 , port 5000
    Routes:
    - /states_list: display a HTML page: (inside the tag BODY)
"""

from models import storage  
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ Displays a HTML page with a list of all States """
    states = storage.all('State')
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """ Closes the database again at the end of the request """
    storage.close()