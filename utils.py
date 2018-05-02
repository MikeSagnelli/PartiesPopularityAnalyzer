from __future__ import unicode_literals
import indicoio
import tweepy
import os

LANGUAGE = "es"
TWEET_BUFFER_SIZE = 10

class SentimentAnalyzer:
    def __init__(self):
        self.indicoio = indicoio
        self.indicoio.config.api_key = os.environ.get("INDICO_API_KEY")

    def analyze_sentiment(self, text):
        sentiment = self.indicoio.sentiment(text, language=LANGUAGE)
        return sentiment


class TwitterAPI:
    def __init__(self):
        auth = tweepy.OAuthHandler(os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))
        auth.set_access_token(os.environ.get('ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET'))
        self.api = tweepy.API(auth)
        self.tweepy = tweepy