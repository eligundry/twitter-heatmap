from twython import Twython, TwythonStreamer
from dateutil import parser
from GDT import *
import json, yaml

config = yaml.safe_load(open('config.yml', 'r'))
gdt = GDT(config['db']['connection'], config['db']['datatype'])

def setup_twitter_stream():
    """ Sets up a streaming connection to the Twitter API """
    tc = config['twitter']
    return TweetStreamer(tc['app_key'], tc['app_secret'], tc['consumer_key'], tc['consumer_secret'])

def setup_twitter():
    """ Sets up a good ol' REST connection to the Twitter API """
    tc = config['twitter']
    return Twython(tc['app_key'], tc['app_secret'], tc['consumer_key'], tc['consumer_secret'])

class TweetStreamer(TwythonStreamer):
    def on_success(self, data):
        # If the tweet doesn't have geo data, we don't care
        if data['geo'] is None:
            return

        tweet = Tweet(data)
        gdt.insert(tweet.data)

        print tweet

    def on_error(self, status_code, error):
        print("%s: %s", status_code, error)
        self.disconnect()

class Tweet():
    def __init__(self, data):
        self.data = {
            'id': data['id'],
            'text': data['text'],
            'html': None,
            'latitude': data['geo']['coordinates'][0],
            'longitude': data['geo']['coordinates'][1],
            'user_id': data['user']['id'],
            'username': data['user']['screen_name'],
            'timestamp': parser.parse(data['created_at']).__str__()
        }

        self.get_oembed()

        print self

    def __str__(self):
        """ Return the Tweet's data in JSON by default """
        return json.dumps(self.data)

    def get_oembed(self):
        """ Gets the oEmbed HTML from the Twitter API """
        a = setup_twitter()
        html = a.get_oembed_tweet(id = str(self.data['id']), omit_script = True, lang = "en", maxwidth = 300)
        self.data['html'] = html['html']

# Run the script infinitely on the server
if __name__ == "__main__":
    a = setup_twitter_stream()
    a.statuses.filter(locations="-81.3893,41.1367,-81.3413,41.1616")
