import tweepy
from tweepy import OAuthHandler
from tweepy import AppAuthHandler
import os, pickle

def Authenticate():
    if  not os.path.exists('TwitterCredentials.pkl'):
        Twitter = {}
        Twitter['Consumer Key'] = ''
        Twitter['Consumer Secret'] = ''
        Twitter['Access Token'] = ''
        Twitter['Access Token Secret'] = ''
        with open('TwitterCredentials.pkl', 'wb') as f:
            pickle.dump(Twitter, f)
    else:
        Twitter = pickle.load(open('TwitterCredentials.pkl', 'rb'))

    try:
        auth1 = OAuthHandler(Twitter['Consumer Key'], Twitter['Consumer Secret'])
        auth1.set_access_token(Twitter['Access Token'], Twitter['Access Token Secret'])
        auth1.apply_auth()
        api = tweepy.API(auth1, wait_on_rate_limit=True)
    except tweepy.TweepError:
        print 'Error in Logging in :)'

    return api


