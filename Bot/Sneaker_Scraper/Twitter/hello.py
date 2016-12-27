import tweepy
from config import TWITTER_CONSUMER_TOKEN, TWITTER_CONSUMER_SECRET

#tut from http://tweepy.readthedocs.io/en/v3.5.0/auth_tutorial.html#auth-tutorial

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_TOKEN, TWITTER_CONSUMER_SECRET)

try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print 'Error! Failed to get request token.'

api = tweepy.API(auth)
api.update_status('tweepy + oauth!')
