import json
import pandas as pd
from login import Authenticate
import tweepy, re
import os


class Twitter(object):
    def __init__(self):
        self.api = Authenticate()

    def get_tweets(self, query ,location = 'world', since = '', result_type= 'mixed'):
        #Taking text of tweets
        #query -> string
        #location -> string
        #result_type -> string ['popular', 'recent', 'mixed']
        locID = self.get_LocID(location)[0]
        if locID == None:
            return None
        tweet = []
        x = tweepy.Cursor(self.api.search,q=query, location = locID, oount = 1000, lang = 'en',tweet_mode = 'extended', result_type = result_type).items(20000000)
        for i in x:
            print i.full_text.encode('UTF-8')
        return tweet

    def get_LocID(self, location):
        location = location.lower()
        loc = self.api.geo_search(location)
        locId = loc[0].id
        locName = loc[0].name
        return locId, locName

    def cleaner(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w +:\ / \ / \S +)", " ", tweet).split())

    def replaceTwoOrMore(self, s):
        # look for 2 or more repetitions of character and replace with the character itself
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", s)

    def get_tweet_json(self, query, location = None):
        '''
        locID = self.get_LocID(location)
        if (locID is None):
            return None
        print 'Collecting data from ' + (locID.name)
        query = 'place:'+ str(locID.id) + ' ' + query
        '''
        tweet_list = []
        print 'Searching for tweets!'
        count = 0
        for i in tweepy.Cursor(self.api.search,q=query, lang = 'en',count = 1000,tweet_mode = 'extended').items(50000):
            print str(count) + " is done!"
            tweet_list.append(i._json)
            count += 1

        return tweet_list

    def get_trend(self):
        print self.api.trends


    #Taking frame of the particular
    def get_frame(self, query):
            print "Initializing Frame!"
            tweets = self.get_tweet_json(query) #Taking JSON fromat list
            n = len(tweets) #length of tweets
            count = 1
            print n
            #df = pd.DataFrame([self.RefineData(tweets[0])])
            df = pd.DataFrame() #Creating dataframe
            for j in tweets:
                tweetVal = self.RefineData(j)
                df = df.append(tweetVal, ignore_index=True)
                count += 1
            df.to_csv('./TrumpData.csv', mode = 'a')  #Inserting data on Append Mode

    def RefineData(self, val):
        #print json.dumps(val, indent = 3)
        id = val['id']
        text = self.cleaner(val['full_text'].encode('UTF-8'))
        is_retweet = val['retweeted']
        retweet_count = val['retweet_count']
        user_id = val['user']['id']
        tweet_create = val['created_at']
        screen_name = val['user']['screen_name'].encode('UTF-8')
        if (val['place'] == None):
            value = val['user']['location'].encode('UTF-8')
            place_name = value
        else:
            place_name = val['place']['name'].encode('UTF-8')
        result_type = val['metadata']['result_type'].encode('UTF-8')
        dics = {'tweet_id': id,
                'full_text': text,
                'is_retweet': is_retweet,
                'retweet_count': retweet_count,
                'user_id': user_id,
                'screen_name': screen_name,
                'tweet_created': tweet_create,
                'place_name' : place_name,
                'result_type': result_type}
        return dics

api = Twitter()
api.get_frame('realDonaldTrump')
