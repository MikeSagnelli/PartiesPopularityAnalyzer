from werkzeug import generate_password_hash, check_password_hash

class User():
    __collection__ = 'users'

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email.lower()
        self.set_password(password)
    
    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)

class Tweet():
    __collection__ = 'tweets'
    def __init__(self, raw_tweet, location, candidate):
        self.raw_tweet = raw_tweet
        self.location = location
        self.candidate = candidate

class ProcessedTweet():
    __collection__ = 'processed_tweets'

    def __init__(self, candidate, location, sentiment):
        self.candidate = candidate
        self.location = location
        self.sentiment = sentiment