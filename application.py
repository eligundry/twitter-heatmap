from flask import Flask, render_template
from flask_sockets import Sockets
from TweetStreamer import *

app = Flask(__name__)
sockets = Sockets(app)

def setup_twitter_stream(websocket, cache_file):
   t = TweetStreamer(TA['ck'], TA['cs'], TA['atk'], TA['ats'])
   t.flush_tweets(websocket, cache_file)
   return t

@app.route('/')
def root():
    return render_template('map.html')

@sockets.route('/tweets')
def get_tweets(ws):
    a = setup_twitter_stream(ws)
    a.statuses.filter(locations="-81.3893,41.1367,-81.3413,41.1616")

if __name__ == "__main__":
    app.debug = True
    app.run()
