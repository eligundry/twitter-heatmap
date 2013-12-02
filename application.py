from flask import Flask, render_template
from flask_sockets import Sockets
from TweetStreamer import *
from GDT import *

app = Flask(__name__)
sockets = Sockets(app)
gdt = GDT('sqlite:///tweets.db', 'tweets')

@app.route('/')
def root():
    return render_template('map.html')

@sockets.route('/tweets')
def get_tweets(ws):
    pass

if __name__ == '__main__':
    app.debug = True
    app.run()
