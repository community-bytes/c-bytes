from flask import (Flask, request, flash, render_template, redirect, url_for, 
                   session, make_response, jsonify)
import requests
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
API_KEY = config['DEFAULT']['API_KEY']

app = Flask(__name__)
app.config['SECRET_KEY'] = "someSecret123"


@app.route('/')
def render_home():

    return render_template('home.html')




if __name__ == "__main__":
    app.run()
