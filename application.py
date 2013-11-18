from flask import Flask, render_template
from flask_sockets import Sockets
from twython import Twython, TwythonStreamer
import json

app = Flask(__name__)
sockets = Sockets(app)

# Twitter API constants
TA = {
    'ck': "HRhPFogV5kE23OnVY88Fw",
    'cs': "HUxEKIP51KJEfg6TVqzTcLT5mYjAkW9IV6XThrBDZM",
    'atk': "1965992269-onDizJpLZEcBBcPWbSGof0FnI0U2TlU9YI44n0K",
    'ats': "D5UK4AoB89AvbfrejZJYDMKvk94sdsiyIyUKBHBdfk"
}

class TweetStreamer(TwythonStreamer):
    def on_success(self, data):
        self.websocket.send(json.dumps(data))

    def on_error(self, status_code, error):
        print("%s: %s", status_code, error)
        self.disconnect()

    def setup_websocket(self, websocket):
        self.websocket = websocket

def setup_twitter_stream(websocket):
   t = TweetStreamer(TA['ck'], TA['cs'], TA['atk'], TA['ats'])
   t.setup_websocket(websocket)
   return t

def setup_twitter():
    return Twython(TA['ck'], TA['cs'], TA['atk'], TA['ats'])

@app.route('/')
def root():
    return render_template('map.html')

@app.route('/oembed/<tweet_id>')
def get_oembed(tweet_id):
    options = {
        "id": str(tweet_id),
        "omit_script": True,
        "lang": "en"
    }

    a = setup_twitter()
    return json.dumps(a.get_oembed_tweet(options))

@sockets.route('/tweets')
def get_tweets(ws):
    a = setup_twitter_stream(ws)
    a.statuses.filter(locations="-81.3893,41.1367,-81.3413,41.1616")

if __name__ == "__main__":
    app.debug = True
    app.run()
