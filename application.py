from flask import Flask, render_template, jsonify
from flask_sockets import Sockets
from twython import Twython, TwythonStreamer

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
        return data['text']

    def on_error(self, status_code, error):
        print("%s: %s", status_code, error)
        self.disconnect()

def setup_twitter():
   return TweetStreamer(TA['ck'], TA['cs'], TA['atk'], TA['ats'])

@app.route('/')
def root():
    return render_template('map.html')

@sockets.route('/tweets')
def get_tweets(ws):
    query = {
        "locations": "41.1367915,-81.389365,41.161646,-81.3413963"
    }

    a = setup_twitter()

    while True:
        ws.send(a.statuses.filter(locations = query["locations"]))

if __name__ == "__main__":
    app.debug = True
    app.run()
