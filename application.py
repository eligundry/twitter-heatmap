from flask import Flask, render_template
from flask_sockets import Sockets
from werkzeug.contrib.cache import SimpleCache
from twython import Twython, TwythonStreamer
import json

app = Flask(__name__)
sockets = Sockets(app)
cache = SimpleCache(default_timeout = 600)

# Twitter API constants
TA = {
    'ck': "HRhPFogV5kE23OnVY88Fw",
    'cs': "HUxEKIP51KJEfg6TVqzTcLT5mYjAkW9IV6XThrBDZM",
    'atk': "1965992269-onDizJpLZEcBBcPWbSGof0FnI0U2TlU9YI44n0K",
    'ats': "D5UK4AoB89AvbfrejZJYDMKvk94sdsiyIyUKBHBdfk"
}

CACHE_TIMEOUT = 6000

class TweetStreamer(TwythonStreamer):
    def on_success(self, data):
        if data.get('geo', False).get('coordinates', False):
            tweet_id = str(data['id'])

            tweet = {
                'id': tweet_id,
                'text': data['text'],
                'html': get_oembed(tweet_id),
                'geo': data['geo']['coordinates']
            }

            tweet = json.dumps(tweet)
            self.cache.set('tweet', tweet)
            self.websocket.send(tweet)

    def on_error(self, status_code, error):
        print("%s: %s", status_code, error)
        self.disconnect()

    def flush_tweets(self, cache, websocket):
        self.cache = cache
        self.websocket = websocket

def setup_twitter_stream(websocket, cache):
   t = TweetStreamer(TA['ck'], TA['cs'], TA['atk'], TA['ats'])
   t.flush_tweets(cache, websocket)
   return t

def setup_twitter():
    return Twython(TA['ck'], TA['cs'], TA['atk'], TA['ats'])

def get_oembed(tweet_id):
    a = setup_twitter()
    html = a.get_oembed_tweet(id = str(tweet_id), omit_script = True, lang = "en", maxwidth = 300)
    return html['html']

@app.route('/')
def root():
    return render_template('map.html')

@sockets.route('/tweets')
def get_tweets(ws):
    a = setup_twitter_stream(ws, cache)
    a.statuses.filter(locations="-81.3893,41.1367,-81.3413,41.1616")

if __name__ == "__main__":
    app.debug = True
    app.run()
