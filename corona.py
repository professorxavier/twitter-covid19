from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient
import time
from datetime import datetime

MONGO_HOST= 'mongodb://localhost/twitterdb' 

WORDS = ['covid', 'covid19', 'corona', 'covid-19', 'coronavs', 'coronavirus', 'covid19brasil', 'cloroquina', 'hidroxicloroquina', 'febre', 'tosse', 'falta de ar', 'coriza', 'azitromicina', 'ivermectina', 'isolamento' , 'quarentena' , 'mascara', 'atazanavir', 'remdesivir', 'lockdown']

CONSUMER_KEY = "your-key"
CONSUMER_SECRET = "your-consumer-secret"
ACCESS_TOKEN = "your-token"
ACCESS_TOKEN_SECRET = "your-token-secret"

client = MongoClient(MONGO_HOST)
db = client.twitterdb

class StreamListener(tweepy.StreamListener):

    def on_connect(self):
        print("You are now connected to the streaming API.")

    def on_exception(self, exception):
        time.sleep(5)
        return True

    def on_error(self, status_code):
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        try:
            t = datetime.now()
            colname = "corona"+str(t.year)+str(t.month)+str(t.day)
            datajson = json.loads(data)
            if 'text' in datajson:
                if ('RT @' not in datajson['text']):
                    db[colname].insert(datajson)
        except Exception as e:
            print(e)
            return True

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))

while True:
    try:
        streamer = tweepy.Stream(auth=auth, listener=listener)
        streamer.filter(track=WORDS, stall_warnings=True, languages=["pt"])
    except:
        print("incomplete...")
        continue

