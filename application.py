from flask import Flask, render_template
from flask_sockets import Sockets
from TweetStreamer import *
from GDT import *

app = Flask(__name__)
sockets = Sockets(app)
gdt = GDT('sqlite:///tweets.db', 'tweets', [41.1367, -81.3893], [41.1616, -81.3413])

@app.route('/')
def root():
    return render_template('map.html')

@sockets.route('/tweets')
def send_tweets(ws):
    result = gdt.find()

    for item in result:
        ws.send(json.dumps(item))

    while ws.socket is not None:
        gevent.sleep(1)

if __name__ == '__main__':
    app.debug = True
    app.run()
