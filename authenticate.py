#!/usr/bin/env python3

import twitter
import os
import ast


class Authenticate(object):
    """ Authenticates to the twitter API

    Attributes:
        # add keys to twitter_creds.txt for script to read from; alternatively, keys can be manually entered
        consumer_key: key to identify the client
        consumer_secret: client password used to authenticate with twitter oauth
        oauth_token: key to define privileges
        oauth_secret: key used with token as password
    """

    def __init__(self, consumer_key="", consumer_secret="", oauth_token="", oauth_secret=""):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token = oauth_token
        self.oauth_secret = oauth_secret
        self.auth = None
        self.twitter_api = None
        # self.parse_arg()
        if not self.consumer_key or not self.consumer_secret or not self.oauth_token or not oauth_secret:
            if self.get_input():
                self.twitter_authenticate()
                # self.get_trends()

    def get_input(self):
        prompt = ">>> "
        path_to_creds = input("Enter full path (i.e. /path/creds.txt) to your credentials file or press Enter to manually enter creds: \n" + prompt)
        try:
            if path_to_creds and os.path.exists(path_to_creds):
                with open(path_to_creds, 'r') as f:
                    creds = ast.literal_eval(f.read())
                    self.consumer_key = creds.get('CONSUMER_KEY')
                    self.consumer_secret = creds.get('CONSUMER_SECRET')
                    self.oauth_token = creds.get('OAUTH_TOKEN')
                    self.oauth_secret = creds.get('OAUTH_TOKEN_SECRET')
                    self.auth = twitter.oauth.OAuth(self.oauth_token, self.oauth_secret, self.consumer_key, self.consumer_secret)
            else:
                self.consumer_key = input('Enter the consumer key: \n' + prompt)
                self.consumer_secret = input('Enter the consumer secret key: \n' + prompt)
                self.oauth_token = input('Enter the oauth token: \n' + prompt)
                self.oauth_secret = input('Enter the oauth secret: \n' + prompt)
                self.auth = twitter.oauth.OAuth(self.oauth_token, self.oauth_secret, self.consumer_key, self.consumer_secret)
            return True


        except Exception as e:
            print('Exception in get_input: ' + str(e))
            return False

    def twitter_authenticate(self):
        self.twitter_api = twitter.Twitter(auth=self.auth)



