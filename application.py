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

class TweetStreamer(TwythonStreamer, websocket):
    self.ws = websocket

    def on_success(self, data):
        self.ws.send(data['text'])

    def on_error(self, status_code, error):
        print("%s: %s", status_code, error)
        self.disconnect()

def setup_twitter(websocket):
   return TweetStreamer(TA['ck'], TA['cs'], TA['atk'], TA['ats'], websocket)

@app.route('/')
def root():
    return render_template('map.html')

@sockets.route('/tweets')
def get_tweets(ws):
    query = {
        "locations": "-81.3893,41.1367,-81.3413,41.1616"
    }

    a = setup_twitter(ws)
    a.statuses.filter(locations="-81.3893,41.1367,-81.3413,41.1616")

if __name__ == "__main__":
    app.debug = True
    app.run()
