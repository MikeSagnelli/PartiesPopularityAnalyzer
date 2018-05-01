from __future__ import unicode_literals
import os
import tweepy

class TwitterAPI:
    def __init__(self):
        auth = tweepy.OAuthHandler(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))
        auth.set_access_token(os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET'))
        self.api = tweepy.API(auth)
        self.tweepy = tweepy