from twython import Twython, TwythonStreamer
from dateutil import parser
from GDT import *
import json

# Twitter API constants
TA = {
    'ck': "HRhPFogV5kE23OnVY88Fw",
    'cs': "HUxEKIP51KJEfg6TVqzTcLT5mYjAkW9IV6XThrBDZM",
    'atk': "1965992269-onDizJpLZEcBBcPWbSGof0FnI0U2TlU9YI44n0K",
    'ats': "D5UK4AoB89AvbfrejZJYDMKvk94sdsiyIyUKBHBdfk"
}

gdt = GDT('sqlite:///tweets.db', 'tweets')

def setup_twitter_stream():
    """ Sets up a streaming connection to the Twitter API """
    return TweetStreamer(TA['ck'], TA['cs'], TA['atk'], TA['ats'])

def setup_twitter():
    """ Sets up a good ol' REST connection to the Twitter API """
    return Twython(TA['ck'], TA['cs'], TA['atk'], TA['ats'])

class TweetStreamer(TwythonStreamer):
    def on_success(self, data):
        # If the tweet doesn't have geo data, we don't care
        if data['geo'] is None:
            return

        tweet = Tweet(data)
        gdt.insert(tweet.data)

    def on_error(self, status_code, error):
        print("%s: %s", status_code, error)
        self.disconnect()

class Tweet():
    def __init__(self, data):
        self.data = {
            'id': data['id'],
            'text': data['text'],
            'html': None,
            'latitude': data['geo']['coordinates'][1],
            'longitude': data['geo']['coordinates'][0],
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
        """ Gets the OEmbed HTML from the Twitter API """
        a = setup_twitter()
        html = a.get_oembed_tweet(id = str(self.data['id']), omit_script = True, lang = "en", maxwidth = 300)
        self.data['html'] = html['html']

# Run the script infinitely on the server
if __name__ == "__main__":
    a = setup_twitter_stream()
    a.statuses.filter(locations="-81.3893,41.1367,-81.3413,41.1616")
