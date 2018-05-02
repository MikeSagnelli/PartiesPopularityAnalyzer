# -*- coding: utf-8 -*-
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

class Queries:
    
    @staticmethod
    def get_queries():
        queries = [('AMLO', "amlo OR peje OR 'andres manuel lopez obrador' OR 'andrés manuel lópez obrador' OR 'lopez obrador' OR morena"),
        ('Anaya', "anaya OR 'ricardo anaya' OR 'ricardo anaya cortes' OR 'ricardo anaya cortés'"),
        ('Meade', "meade OR 'jose antonio meade kuribeña' OR 'josé antonio meade kuribeña' OR 'jose antonio meade' OR 'jose meade' OR pri"),
        ('Zavala', "zavala OR 'margarita zavala' OR 'margarita zavala gomez del campo' OR 'margarita zavala gómez del campo'"),
        ('Bronco', "'el bronco' OR 'jaime rodriguez' OR 'jaime rodríguez' OR 'jaime rodriguez calderon' OR 'jaime rodríguez calderon' OR 'jaime rodriguez calderón' OR 'jaime rodríguez calderón' OR 'jaime rodriguez el bronco'")
        ]
        return queries
