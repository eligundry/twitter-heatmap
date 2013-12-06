from flask import Flask, render_template
from flask_sockets import Sockets
from GDT import *
import json, yaml

app = Flask(__name__)
sockets = Sockets(app)
config = yaml.safe_load(open('config.yml', 'r'))
gdt = GDT(config['db']['connection'], config['db']['datatype'], [41.1367, -81.3893], [41.1616, -81.3413])

@app.route('/')
def root():
    return render_template('map.html')

@sockets.route('/tweets')
def send_tweets(ws):
    result = gdt.find()

    for item in result:
        ws.send(json.dumps(item))

if __name__ == '__main__':
    app.debug = True
    app.run()
