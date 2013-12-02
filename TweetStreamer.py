from twython import Twython, TwythonStreamer
from dateutil import parser
import json

# Twitter API constants
TA = {
    'ck': "HRhPFogV5kE23OnVY88Fw",
    'cs': "HUxEKIP51KJEfg6TVqzTcLT5mYjAkW9IV6XThrBDZM",
    'atk': "1965992269-onDizJpLZEcBBcPWbSGof0FnI0U2TlU9YI44n0K",
    'ats': "D5UK4AoB89AvbfrejZJYDMKvk94sdsiyIyUKBHBdfk"
}

class TweetStreamer(TwythonStreamer):
    def on_success(self, data):
        if data['geo'] is None:
            return

        tweet = Tweet(data)

    def on_error(self, status_code, error):
        print("%s: %s", status_code, error)
        self.disconnect()

class Tweet(data):
    def __init__(self, data):
        self.__data = {
            'id': data['id'],
            'text': data['text'],
            'html': get_oembed(data['id']),
            'latitude': data['geo']['coordinates'][1],
            'longitude': data['geo']['coordinates'][0],
            'user_id': data['user']['id'],
            'username': data['user']['screen_name'],
            'timestamp': parser.parse(data['created_at'])
        }

        return

    def __str__(self):
        """ Return the Tweet's data in JSON by default """
        return json.dumps(self.__data)

    def get_oembed(self):
        """ Gets the oembed html from the Twitter API """
        a = self.__setup_twiter()
        html = a.get_oembed_tweet(id = str(self.__data['id']), omit_script = True, lang = "en", maxwidth = 300)
        return html['html']

    def setup_twitter(self):
        return Twython(TA['ck'], TA['cs'], TA['atk'], TA['ats'])
