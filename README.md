# Twitter Heatmap

A Flask application that uses websockets to map Tweets in a geographic location
and produces a heatmap with it.

## Setup

1. Clone this repo
2. Setup a virtualenv
```shell
$ virtualenv --python=python2.7 --no-site-packages .venv
$ source .venv/bin/activate
```
3. Install the requirements
```shell
$ pip install -r requirements.txt
```
4. Save `config-sample.yml` as `config.yml` and add the values you want to use
5. Run the Tweet collector
```shell
$ python TweetStreamer.py
```
6. Run the webserver
```shell
$ gunicorn -k flask_sockets.worker application:app
```
