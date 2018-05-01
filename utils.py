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

class TweetsStreamer(tweepy.StreamListener):
    def on_connect(self):
        # Called once connected to streaming server
        print ('Connected to streamer')
        self.buffer_size = TWEET_BUFFER_SIZE
        self.buffer = []
        self.tweet_counter = 0

    def on_status(self, status):
        # Called when a new status arrives
        if not status.retweeted and 'RT @' not in status.text and status.lang == 'es':
            self.tweet_counter += 1
            print ('Tweet (' + str(self.tweet_counter) + ') by: @' + status.user.screen_name)
            self.buffer.append(status)
            if(len(self.buffer) == self.buffer_size):
                # save to db
                self.buffer = []