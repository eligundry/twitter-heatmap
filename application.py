from flask import Flask, render_template
from flask_sockets import Sockets
from GDT import *
import json, yaml

app = Flask(__name__)
sockets = Sockets(app)
config = yaml.safe_load(open('config.yml', 'r'))
gdt = GDT(config['db']['connection'], config['db']['datatype'],
        config['coordinates']['sw'], config['coordinates']['ne'])

@app.route('/')
def root():
    return render_template('map.html')

@sockets.route('/tweets')
def send_tweets(ws):
    result = gdt._table.all()

    for item in result:
        item['timestamp'] = str(item['timestamp'])
        print item
        ws.send(json.dumps(item))

if __name__ == '__main__':
    app.debug = True
    app.run()
